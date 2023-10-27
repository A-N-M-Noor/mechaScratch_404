import cv2
import numpy as np
import json

threshold = 15
frst = True

def on_trackbar(val):
    pass

def clamp(_num, min_value = 0, max_value = 255):
    return max(min(_num, max_value), min_value)

def saveVal(_rng):
    nameC = input("Name of the color: ")
    if(len(nameC) > 0):
        with open('Data/colors.json', 'r+') as f:
            clrs = json.load(f)
            clrs[nameC] = _rng

            blr = cv2.getTrackbarPos('Blur', 'range')
            blr2 = blr if(blr%2 == 1) else blr+1
            clrs["blur"] = blr2
            clrs["areaMin"] = cv2.getTrackbarPos('Minimum Area', 'range')

            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(clrs, f)

def loadVal():
    with open('Data/colors.json', 'r') as f:
        clrs = json.load(f)
        print(f"Available Colors: {list(clrs.keys())}")
        nameC = input("Name of the color: ")
        if(nameC in list(clrs.keys())):
            rng = clrs[nameC]
            cv2.setTrackbarPos('H min', 'range', rng[0][0])
            cv2.setTrackbarPos('H max', 'range', rng[1][0])
            cv2.setTrackbarPos('S min', 'range', rng[0][1])
            cv2.setTrackbarPos('S max', 'range', rng[1][1])
            cv2.setTrackbarPos('V min', 'range', rng[0][2])
            cv2.setTrackbarPos('V max', 'range', rng[1][2])


def setSliders(rng, thr):
    cv2.setTrackbarPos('H min', 'range', clamp(rng[0][0] - thr, 0, 179))
    cv2.setTrackbarPos('H max', 'range', clamp(rng[1][0] + thr, 0, 179))
    cv2.setTrackbarPos('S min', 'range', clamp(rng[0][1] - thr, 0, 255))
    cv2.setTrackbarPos('S max', 'range', clamp(rng[1][1] + thr, 0, 255))
    cv2.setTrackbarPos('V min', 'range', clamp(rng[0][2] - thr, 0, 255))
    cv2.setTrackbarPos('V max', 'range', clamp(rng[1][2] + thr, 0, 255))


def on_mouse_click(event, x, y, flags, param):
    global frst, threshold
    if event == cv2.EVENT_LBUTTONUP:
        # Get pixel value at (x, y)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = hsv[y, x, :]
        
        _min = [min(h, cv2.getTrackbarPos('H min', 'range')), min(s, cv2.getTrackbarPos('S min', 'range')), min(v, cv2.getTrackbarPos('V min', 'range'))]
        _max = [max(h, cv2.getTrackbarPos('H max', 'range')), max(s, cv2.getTrackbarPos('S max', 'range')), max(v, cv2.getTrackbarPos('V max', 'range'))]

        if frst:
            _min = [h, s - threshold*6, v - threshold*6]
            _max = [h, s + threshold*6, v + threshold*6]
            frst = False
        setSliders([_min,_max], threshold)
#[75, 15, 111] [96, 255, 223]
# Create window and trackbars
cv2.namedWindow('range', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Blur', 'range', 0, 10, on_trackbar)
cv2.createTrackbar('H min', 'range', 0, 179, on_trackbar)
cv2.createTrackbar('H max', 'range', 0, 179, on_trackbar)
cv2.createTrackbar('S min', 'range', 0, 255, on_trackbar)
cv2.createTrackbar('S max', 'range', 0, 255, on_trackbar)
cv2.createTrackbar('V min', 'range', 0, 255, on_trackbar)
cv2.createTrackbar('V max', 'range', 0, 255, on_trackbar)
cv2.createTrackbar('Minimum Area', 'range', 50, 1000, on_trackbar)
cv2.createTrackbar('Threshold', 'range', 0, 128, on_trackbar)
cv2.setTrackbarPos('Threshold', 'range', threshold)
cv2.setTrackbarPos('Blur', 'range', 5)
cv2.setTrackbarPos('Minimum Area', 'range', 500)

flip=0
dispW=640
dispH=480
camSet='nvarguscamerasrc wbmode=0 !  video/x-raw(memory:NVMM), width='+str(dispW*2)+', height='+str(dispH*2)+', format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW*2)+', height='+str(dispH*2)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
#cap = cv2.VideoCapture(camSet)

font=cv2.FONT_HERSHEY_SIMPLEX

def makeMask(_hsv, rngMin, rngMax):
    lower_range = np.array(rngMin)
    upper_range = np.array(rngMax)

    mask = None
    if(rngMin[0] < rngMax[0]):
        mask = cv2.inRange(_hsv, lower_range, upper_range)
    else:
        mask = cv2.inRange(_hsv, np.array([0, rngMin[1], rngMin[2]]), upper_range)
        mask2 = cv2.inRange(_hsv, lower_range, np.array([180, rngMax[1], rngMax[2]]))

        mask = mask + mask2

    cnt, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    return cnt, mask

def getObjs(_frame, _cnt, colName, areaThr):
    objList = []

    for cont in _cnt:
        if( cv2.contourArea(cont) > areaThr ):
            x,y,w,h = cv2.boundingRect(cont)
            rct = cv2.minAreaRect(cont)
            rBnd = np.int0(cv2.boxPoints(rct))
            cv2.rectangle(_frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.drawContours(_frame, [rBnd], -1, (255,0,0),2)

            pX, pY, sWA, sWB = int(rct[0][0]), int(rct[0][1]), int(rct[1][0]), int(rct[1][1])

            sW = min(sWA, sWB)
            if( (w*h)/(sWA*sWB) < 1.25 ):
                sW = w
            cv2.circle(_frame, (int(rct[0][0]), int(rct[0][1])), 5, (255, 0, 0), -1)

            cv2.putText(_frame,f"{pX} | {sW} | {rct[2]}",(pX, pY), font, .5,(255,0,0),2)

            objList.append({
                "color": colName,
                "pos": pX,
                "dist": 2141 / sW
            })
    
    objList.sort(key=lambda d:d["dist"])

    return objList

while True:
    # Read frame from camera
    ret, frame = cap.read()
    frame = cv2.resize(frame, (dispW, dispH))
    blr = cv2.getTrackbarPos('Blur', 'range')
    blr2 = blr if(blr%2 == 1) else blr+1
    if(blr > 0): frame = cv2.GaussianBlur(frame, (blr2,blr2), cv2.BORDER_DEFAULT)
    # Get trackbar values
    h_min = cv2.getTrackbarPos('H min', 'range')
    h_max = cv2.getTrackbarPos('H max', 'range')
    s_min = cv2.getTrackbarPos('S min', 'range')
    s_max = cv2.getTrackbarPos('S max', 'range')
    v_min = cv2.getTrackbarPos('V min', 'range')
    v_max = cv2.getTrackbarPos('V max', 'range')
    threshold = cv2.getTrackbarPos('Threshold', 'range')
    
    # Convert frame to HSL
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cnt, mask = makeMask(hsv, [h_min, s_min, v_min], [h_max, s_max, v_max])

    # Apply mask to original frame
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.drawContours(masked_frame, cnt, -1, (0,255,255),2)
    
    objectS = getObjs(frame, cnt, "R", cv2.getTrackbarPos('Minimum Area', 'range'))
    print(objectS)
   
    # Display mask and masked frame
    cv2.imshow('original', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('masked frame', masked_frame)
    
    # Set mouse callback
    cv2.setMouseCallback('original', on_mouse_click)

    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey ==  ord('s'):
        print(f"lower = [{h_min}, {s_min}, {v_min}]")
        print(f"upper = [{h_max}, {s_max}, {v_max}]")
        rng = [[h_min, s_min, v_min], [h_max, s_max, v_max]]
        saveVal(rng)
    if pressedKey ==  ord('l'):
        loadVal()
    # Exit on key press
    if pressedKey ==  ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
