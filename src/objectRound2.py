import os
import json
import math
import time
from threading import Thread

import cv2
import numpy as np
import serial
from serial.tools import list_ports


class vStream:
    def __init__(self,src,width=860,height=480, Type=False, blr = 5):
        self.width=width
        self.height=height
        if(Type):
            self.capture=cv2.VideoCapture(src, Type)
        else:
            self.capture=cv2.VideoCapture(src)
        
        self.startTime=time.time()
        self.dtav=0
        self.fps = 0

        self.thread=Thread(target=self.update,args=())
        self.thread.daemon=True
        self.thread.start()

    def update(self):
        while True:
            _,self.frame=self.capture.read()
            self.frame2=cv2.resize(self.frame,(self.width,self.height))

            self.dt=time.time()-self.startTime
            self.startTime=time.time()
            self.dtav=.9*self.dtav+.1*self.dt
            self.fps=1/self.dtav
    def getFrame(self):
        return self.frame2


def clamp(val, mini, maxi):
    tMin = mini
    tMax = maxi
    if (mini > maxi):
        tMin = maxi
        tMax = mini

    if (val < tMin):
        return tMin

    if (val > tMax):
        return tMax
    return val

def mapF(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def mapFC(x, in_min, in_max, out_min, out_max):
    return clamp( mapF(x, in_min, in_max, out_min, out_max), out_min, out_max)


def lerpF(a, b, t):
    return a + t * (b - a)



flip=0
dispW=860
dispH=480
#camSet='nvarguscamerasrc wbmode=0 !  video/x-raw(memory:NVMM), width='+str(dispW*2)+', height='+str(dispH*2)+', format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW*2)+', height='+str(dispH*2)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam2=vStream(0, Type=cv2.CAP_V4L, blr=3)
font=cv2.FONT_HERSHEY_SIMPLEX

ports = serial.tools.list_ports.comports()
for p in ports:
    print(p.device, type(p.device))
print(len(ports), 'ports found')

sPrt = False
while True:
    try:
        sPrt = serial.Serial('/dev/ttyUSB0', 115200)
    except Exception as e:
        print(e)
        time.sleep(0.5)
    finally:
        break

print("Successfully onnected to /dev/ttyUSB0")


def loadVal():
    print("LOADING...")
    pth = "/home/mecha-scratch/Codes/Data/colors.json"
    print(pth)
    with open(pth, 'r') as f:
        clrs = json.load(f)
        return clrs


def getLines(_hsv, _borderMask, rng, minL = 100):
    lower_range = np.array(rng[0])
    upper_range = np.array(rng[1])
    
    mask = None
    if(rng[0][0] < rng[1][0]):
        mask = cv2.inRange(_hsv, lower_range, upper_range)
    else:
        mask = cv2.inRange(_hsv, np.array([0, rng[0][1], rng[0][2]]), upper_range)
        mask2 = cv2.inRange(_hsv, lower_range, np.array([180, rng[1][1], rng[1][2]]))

        mask = mask + mask2
    mask = cv2.bitwise_and(mask, _borderMask)
    
    ret, thresh = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)

    cnt, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    
    lines = []
    linesOut = []
    for cont in cnt:
        rect = cv2.minAreaRect(cont)
        rBnd = np.int0(cv2.boxPoints(rect))

        lineL = max(rect[1][0], rect[1][1])
        lineW = min(rect[1][0], rect[1][1])
        vx,vy,x,y = cv2.fitLine(rBnd, cv2.DIST_L2,0,0.01,0.01)
        
        x1, y1, x2, y2 = int(x - vx*lineL/2),int(y - vy*lineL/2), int(x + vx*lineL/2),int(y + vy*lineL/2)
        ang = math.degrees( math.atan2(vy, vx) )
        if(lineL > minL and lineW < 30): 
            if(max(y1,y2) > 200):
                lines.append([(x1, y1), (x2, y2), lineL, ang, (x,y)]) 
            else:
                linesOut.append([(x1, y1), (x2, y2), lineL, ang, (x,y)]) 
    lines.sort(key = lambda l: l[2], reverse=True)
    return lines, linesOut, mask

def showLines(_frame, _lines, _oLines):
    for ln in _lines:
        cv2.line(_frame, ln[0], ln[1], (255, 0, 255), 3)
        cv2.circle(_frame, ln[1], 7, (0,255,255), -1)
        cv2.putText(_frame, str(int(ln[3])), (ln[0]), font, 0.5, (255,0,255))

    for ln in _oLines:
        cv2.line(_frame, ln[0], ln[1], (255, 255, 0), 3)
        cv2.circle(_frame, ln[1], 7, (0,255,255), -1)
        cv2.putText(_frame, str(int(ln[3])), (ln[0]), font, 0.5, (255,255,0))



vals = loadVal()
rngBlue = vals["blue2"]
rngOrng = vals["orange2"]
blr = vals["blur"]

rngGreen = vals["green"]
rngRed = vals["red"]
areaMin = vals["areaMin"]

def sendDat(_sPrt, key, val):
    if(not sPrt):
        return
    print((key, val-50))
    v = int(key)
    _sPrt.write(v.to_bytes(1, 'little'))
    v = int(val)
    _sPrt.write(v.to_bytes(1, 'little'))

turnCount = 0
firstLine = "-" # O means Orange, B means Blue
lineTime = 2
lineTimer = -lineTime
gotLine = False
lineAng = 0
trackDir = 0
outLine = False

objType = 'N'
objPos = 0
objDist = 400

objTypeF = 'N'
objPosF = 0
objDistF = 400
futureObjTimer = 0
futureObjTime = 3

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
    ret, thresh = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)
    cnt, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    return cnt, mask

def getObjs(_frame, _cnt, colName, areaThr):
    objList = []

    for cont in _cnt:
        cArea = cv2.contourArea(cont)
        bArea = cv2.contourArea( cv2.convexHull(cont) )
        solidity = 0
        if(cArea > 0 and bArea > 0):
            solidity = cArea/bArea
        if( cArea > areaThr and solidity > 0.75):
            x,y,w,h = cv2.boundingRect(cont)
            rct = cv2.minAreaRect(cont)
            rBnd = np.int0(cv2.boxPoints(rct))
            pX, pY, sWA, sWB = int(rct[0][0]), int(rct[0][1]), int(rct[1][0]), int(rct[1][1])

            sW = min(sWA, sWB)
            sH = max(sWA, sWB)
            if( (w*h)/(sWA*sWB) < 1.25 ):
                sW = w
                sH = h
            cv2.circle(_frame, (int(rct[0][0]), int(rct[0][1])), 5, (255, 0, 0), -1)
            posX = pX-sW/2 if(colName=="G") else pX+sW/2
            _obj = {
                "color": colName,
                "pos": int(mapFC(posX, 0, dispW, 0, 200)),
                "dist": int(3462 / sW)-7,
                "coord": (pX, pY)
            }
            if(sW/sH < 1.25 and sW/sH > 0.25):
                objList.append(_obj)
                cv2.rectangle(_frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                cv2.drawContours(_frame, [rBnd], -1, (255,0,0),2)
                cv2.putText(_frame,f"{_obj['color']} | {_obj['pos']} | {_obj['dist']}({sW})",(pX, pY), font, .5,(0,255,255),2)

    return objList

def serialComm():
    global turnCount
    global firstLine
    global trackDir
    global gotLine
    global outLine
    global lineTimer

    while True:
        try:
            if(sPrt.in_waiting > 0):
                rd = sPrt.read().decode()
                if(rd == 'D'):
                    """if(objTypeF == "R"): sendDat(sPrt, 2, 51)
                    if(objTypeF == "N"): sendDat(sPrt, 2, 52)
                    if(objTypeF == "G"): sendDat(sPrt, 2, 53)
                    
                    sendDat(sPrt, 3, objPos+50)
                    sendDat(sPrt, 4, objDist+50)"""

                    if(objType == "R"): sendDat(sPrt, 5, 51)
                    if(objType == "N"): sendDat(sPrt, 5, 52)
                    if(objType == "G"): sendDat(sPrt, 5, 53)
                    
                    sendDat(sPrt, 6, objPos+50)
                    sendDat(sPrt, 7, objDist+50)

                    sendDat(sPrt, 8, turnCount+50)
                    #sendDat(sPrt, 9, lineAng+150)
                    sendDat(sPrt, 10, trackDir+150)
                    if(outLine):
                        sendDat(sPrt, 11, 60)
                    else:
                        sendDat(sPrt, 11, 51)
                if(rd == 'U'):
                    trackDir = trackDir * -1
                    turnCount = 0
                    gotLine = False
                    if(firstLine == 'O'): 
                        firstLine = 'B'
                    if(firstLine == 'B'): 
                        firstLine = 'O'
                    sendDat(sPrt, 8, turnCount+50)
                
                if(rd == "<"):
                    vl = sPrt.read_until(b">").decode()
                    try:
                        lineTimer = lineTimer - (int(vl[:-1]) / 1000.0)
                    except Exception as e:
                        print(e)
                
                if(rd == 'S'):
                    turnCount = 0
                    firstLine = "-"
                    trackDir = 0
                    gotLine = True
                    lineTimer = -lineTime
                print(rd)
        except Exception as e:
            print(e)

linesOrng = []
outLineO = []
linesBlue = []
outLineB = []

def linesD():
    global turnCount
    global firstLine
    global trackDir
    global gotLine
    global outLine

    global lineTimer
    global linesOrng
    global outLineO
    global linesBlue
    global outLineB

    _startTime=time.time()
    _dtav=0

    while True:
        try:
            frameB=cam2.getFrame().copy()

            frameBlr = cv2.GaussianBlur(frameB, (3,3), cv2.BORDER_DEFAULT)
            hsvB = cv2.cvtColor(frameBlr, cv2.COLOR_BGR2HSV)

            borderMask = np.zeros(frameB.shape[:2], dtype="uint8")
            cv2.rectangle(borderMask, (50, 50), (frameB.shape[:2][1]-50, frameB.shape[:2][0]-50), (255), -1)

            if(firstLine == "-" or turnCount == 12):
                linesOrng, outLineO, mskO = getLines(hsvB, borderMask, rngOrng)
                linesBlue, outLineB, mskB = getLines(hsvB, borderMask, rngBlue)
            else:
                if(firstLine == "B"):
                    linesBlue, outLineB, mskB = getLines(hsvB, borderMask, rngBlue)
                    linesOrng, outLineO = [], []
                else:
                    linesOrng, outLineO, mskO = getLines(hsvB, borderMask, rngOrng)
                    linesBlue, outLineB = [], []

            #showLines(frameB, linesBlue + linesOrng, outLineO + outLineB)

            oLine = True if (len(linesOrng) > 0) else False
            bLine = True if (len(linesBlue) > 0) else False

            if(firstLine == "-"):
                if(oLine and bLine):
                    print(linesBlue)
                    print(linesOrng)
                    if(linesBlue[0][4][1] < linesOrng[0][4][1]):
                        firstLine = "B"
                        trackDir = 1
                    else: 
                        firstLine = "O"
                        trackDir = -1
                
                elif(oLine):
                    firstLine = "O"
                    trackDir = -1
                elif(bLine):
                    firstLine = "B"
                    trackDir = 1

            lineAng = 0
            if(oLine or bLine):
                if(time.time() - lineTimer > lineTime and gotLine == False):
                    if(oLine and firstLine == "O"):
                        turnCount = turnCount + 1
                        lineTimer = time.time()
                        gotLine = True
                    if(bLine and firstLine == "B"):
                        turnCount = turnCount + 1
                        lineTimer = time.time()
                        gotLine = True
            else:
                gotLine = False
            
            outLine = False
            if(len(outLineB) > 0 or len(outLineO) > 0):
                if(firstLine == "B" and len(outLineB) > 0):
                    outLine = True
                if(firstLine == "O" and len(outLineO) > 0):
                    outLine = True
            #print(trackDir)

        except Exception as e:
            print('frame not available A')
            print(e)
            time.sleep(1)


commThread=Thread(target=serialComm,args=())
commThread.daemon=True
commThread.start()

linesThread=Thread(target=linesD,args=())
linesThread.daemon=True
linesThread.start()

startTime=time.time()
dtav=0

while True:
    try:
        frame = cam2.getFrame().copy()
        OframeBlr = cv2.GaussianBlur(frame, (blr,blr), cv2.BORDER_DEFAULT)
        hsvF = cv2.cvtColor(OframeBlr, cv2.COLOR_BGR2HSV)
        cntG, maskG = makeMask(hsvF, rngGreen[0], rngGreen[1])
        cntR, maskR = makeMask(hsvF, rngRed[0], rngRed[1])
        
        showLines(frame, linesBlue + linesOrng, outLineO + outLineB)

        objectsG = getObjs(frame, cntG, "G", areaMin)
        objectsR = getObjs(frame, cntR, "R", areaMin)

        objList = objectsG + objectsR
        objType = "N"
        objPos = 0
        objDist = 200
        objList.sort(key=lambda obj:obj["dist"])

        if(len(objList) > 0):
            objType = objList[0]["color"]
            objPos = int(objList[0]["pos"])
            objDist = int(clamp(objList[0]["dist"], 0, 200))

        if(len(objList) > 1):
            objTypeF = objList[1]["color"]
            objPosF = int(objList[1]["pos"])
            objDistF = int(clamp(objList[1]["dist"], 0, 200))
            futureObjTimer = time.time()
        elif(time.time() - futureObjTimer > futureObjTime):
            objTypeF = "N"
            objPosF = 0
            objDistF = 200

        dt=time.time()-startTime
        startTime=time.time()
        dtav=.9*dtav+.1*dt
        fps=1/dtav
        cv2.rectangle(frame,(0,0),(140,40),(0,0,255),-1)
        cv2.putText(frame,str(round(fps, 1))+' fps',(0,25),font,.75,(0,255,255),2)
        cv2.rectangle(frame,(0,50),(140,90),(0,0,255),-1)
        cv2.putText(frame,firstLine + "  " + str(int(turnCount)),(10,75),font,.75,(0,255,255),2)

        cv2.imshow('Objects',frame)

    except KeyboardInterrupt:
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break

    except Exception as e:
        print('frame not available B')
        print(e)
        time.sleep(1)
        
    if cv2.waitKey(1)==ord('q'):
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break


