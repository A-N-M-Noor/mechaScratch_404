import json
import math
import time
from threading import Thread

import cv2
import numpy as np
import serial
from serial.tools import list_ports


class vStream:
    def __init__(self,src,width=640,height=480, Type=False, blr = 5):
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
        return cv2.GaussianBlur(self.frame2, (blr,blr), cv2.BORDER_DEFAULT)


flip=0
dispW=640
dispH=480
camSet='nvarguscamerasrc wbmode=0 !  video/x-raw(memory:NVMM), width='+str(dispW*2)+', height='+str(dispH*2)+', format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW*2)+', height='+str(dispH*2)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam2=vStream(0, Type=cv2.CAP_V4L)
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
    with open('Data/colors.json', 'r') as f:
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
    cnt, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    
    lines = []
    for cont in cnt:
        rect = cv2.minAreaRect(cont)
        lineL = max(rect[1][0], rect[1][1])
        vx,vy,x,y = cv2.fitLine(cont, cv2.DIST_L2,0,0.01,0.01)
        
        x1, y1, x2, y2 = int(x - vx*lineL/2),int(y - vy*lineL/2), int(x + vx*lineL/2),int(y + vy*lineL/2)
        ang = math.degrees( math.atan2(vy, vx) )
        if(lineL > minL and max(y1,y2) > 240): lines.append([(x1, y1), (x2, y2), lineL, ang, (x,y)]) 
    lines.sort(key = lambda l: l[2], reverse=True)
    
    return lines, mask

def showLines(_frame, _lines):
    for ln in _lines:
        cv2.line(_frame, ln[0], ln[1], (255, 255, 0), 3)
        cv2.circle(_frame, ln[1], 7, (0,255,255), -1)
        cv2.putText(_frame, str(int(ln[3])), (ln[0]), font, 0.5, (255,0,255))



vals = loadVal()
rngBlue = vals["blue2"]
rngOrng = vals["orange2"]
blr = vals["blur"]

def sendDat(_sPrt, key, val):
    if(not sPrt):
        return

    v = key
    _sPrt.write(v.to_bytes(1, 'little'))
    v = val
    _sPrt.write(v.to_bytes(1, 'little'))

turnCount = 0
firstLine = "-" # O means Orange, B means Blue
lineTime = 1.6
lineTimer = -lineTime
gotLine = True
lineAng = 0
trackDir = 0

def serialComm():
    global turnCount
    global firstLine
    global trackDir
    global gotLine
    while True:
        try:
            if(sPrt.in_waiting > 0):
                rd = sPrt.read().decode()
                if(rd == 'D'):
                    sendDat(sPrt, 8, turnCount+50)
                    sendDat(sPrt, 9, lineAng+150)
                    sendDat(sPrt, 10, trackDir+150)
                if(rd == 'S'):
                    turnCount = 0
                    firstLine = "-"
                    trackDir = 0
                    gotLine = True
                print(rd)
        except Exception as e:
            print(e)
                

commThread=Thread(target=serialComm,args=())
commThread.daemon=True
commThread.start()

while True:
    try:
        frameB=cam2.getFrame()
        hsvB = cv2.cvtColor(frameB, cv2.COLOR_BGR2HSV)

        borderMask = np.zeros(frameB.shape[:2], dtype="uint8")
        cv2.rectangle(borderMask, (50, 50), (frameB.shape[:2][1]-50, frameB.shape[:2][0]-50), (255), -1)

        linesOrng, mskO = getLines(hsvB, borderMask, rngOrng)
        linesBlue, mskB = getLines(hsvB, borderMask, rngBlue)

        _frameB = frameB.copy()
        showLines(_frameB, linesBlue + linesOrng)

        if(firstLine == "-"):
            if(len(linesOrng) > 0 and len(linesBlue) > 0):
                print(linesBlue)
                print(linesOrng)
                if(linesBlue[0][4][1] < linesOrng[0][4][1]):
                    firstLine = "B"
                    trackDir = 1
                else: 
                    firstLine = "O"
                    trackDir = -1
            
            elif(len(linesOrng) > 0):
                firstLine = "O"
            elif(len(linesBlue) > 0):
                firstLine = "B"

        lineAng = 0
        if(len(linesOrng) > 0 or len(linesBlue) > 0):
            if(time.time() - lineTimer > lineTime and gotLine == False):
                if(len(linesOrng) > 0 and firstLine == "B"):
                    turnCount = turnCount + 1
                    lineTimer = time.time()
                    gotLine = True
                if(len(linesBlue) > 0 and firstLine == "O"):
                    turnCount = turnCount + 1
                    lineTimer = time.time()
                    gotLine = True
        else:
            gotLine = False
            
        cv2.rectangle(_frameB,(0,0),(140,40),(0,0,255),-1)
        cv2.putText(_frameB,firstLine + "  " + str(int(turnCount)),(10,25),font,.75,(0,255,255),2)
        cv2.imshow('Frame',_frameB)
        cv2.imshow('mskB',mskB)
        

    except KeyboardInterrupt:
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break

    except Exception as e:
        print('frame not available')
        print(e)
        time.sleep(1)
        
    if cv2.waitKey(1)==ord('q'):
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break
