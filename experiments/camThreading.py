from threading import Thread
import cv2
import time
import numpy as np

class vStream:
    def __init__(self,src,width=640,height=480, Type=False):
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
flip=0
dispW=640
dispH=480
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width='+str(dispW*2)+', height='+str(dispH*2)+', format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam1=vStream(1, Type=cv2.CAP_V4L)
cam2=vStream(camSet)
font=cv2.FONT_HERSHEY_SIMPLEX
startTime=time.time()
dtav=0
while True:
    try:
        myFrame1=cam1.getFrame()
        myFrame2=cam2.getFrame()
        myFrame3=np.hstack((myFrame1,myFrame2))
        dt=time.time()-startTime
        startTime=time.time()
        dtav=.9*dtav+.1*dt
        fps=1/dtav
        cv2.rectangle(myFrame3,(0,0),(140,40),(0,0,255),-1)
        cv2.putText(myFrame3,str(round(cam1.fps,1))+' fps',(0,25),font,.75,(0,255,255),2)

        cv2.rectangle(myFrame3,(dispW,0),(dispW+140,40),(0,0,255),-1)
        cv2.putText(myFrame3,str(round(cam2.fps,1))+' fps',(dispW,25),font,.75,(0,255,255),2)

        cv2.imshow('ComboCam',myFrame3)
        cv2.moveWindow('ComboCam',0,0)



    except:
        print('frame not available')
        
    if cv2.waitKey(1)==ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break
