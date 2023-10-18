import cv2
import numpy as np
import json

threshold = 15
frst = True

def on_trackbar(val):
    pass

def clamp(_num, min_value = 0, max_value = 255):
    return max(min(_num, max_value), min_value)

def setSliders(rng, thr):
    print(rng)
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
cv2.createTrackbar('Threshold', 'range', 0, 128, on_trackbar)
cv2.setTrackbarPos('Threshold', 'range', threshold)
cv2.setTrackbarPos('Blur', 'range', 3)

# Open default camera
cap = cv2.VideoCapture(1, cv2.CAP_V4L)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
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

    # Define range of colors to mask
    lower_range = np.array([h_min, s_min, v_min])
    upper_range = np.array([h_max, s_max, v_max])

    # Create mask using color range
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    cnt, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    # Apply mask to original frame
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.drawContours(masked_frame, cnt, -1, (0,255,255),2)

    for cont in cnt:
        if( cv2.contourArea(cont) > 500 ):
            x,y,w,h = cv2.boundingRect(cont)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.circle(frame, (int(x + w/2), int(y + h/2)), 5, (0, 255, 255), -1)

   
    # Display mask and masked frame
    cv2.imshow('original', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('masked frame', masked_frame)
    
    # Set mouse callback
    cv2.setMouseCallback('original', on_mouse_click)

    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey ==  ord('s'):
        print(f"lower = [{cv2.getTrackbarPos('H min', 'range')}, {cv2.getTrackbarPos('S min', 'range')}, {cv2.getTrackbarPos('V min', 'range')}]")
        print(f"upper = [{cv2.getTrackbarPos('H max', 'range')}, {cv2.getTrackbarPos('S max', 'range')}, {cv2.getTrackbarPos('V max', 'range')}]")
    # Exit on key press
    if pressedKey ==  ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
