import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

import math
import cv2
import threading

camWidth = 1.5
viewAngle = 0.50
imageWidth = 320

angle = 0
speed = 0

# Enable camera
cap1 = cv2.VideoCapture(0)
cap1.set(3, imageWidth)
cap1.set(4, 210)
cap2 = cv2.VideoCapture(2)
cap2.set(3, imageWidth)
cap2.set(4, 210)

# import cascade file for facial recognition
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def camera():
    while True:
        motors()
        success, img1 = cap1.read()
        imgGray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        faces1 = faceCascade.detectMultiScale(imgGray, 1.3, 5) 
        for (x, y, w, h) in faces1:
            img = cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.imshow('cam1', img1)

        success, img2 = cap2.read()
        imgGray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # Getting corners around the face
        faces2 = faceCascade.detectMultiScale(imgGray, 1.3, 4)  # 1.3 = scale factor, 5 = minimum neighbor
        # drawing bounding box around face
        for (x, y, w, h) in faces2:
            img = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.imshow('cam2', img2)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        getDists(faces1,faces2);

    cap.release()
    cv2.destroyWindow('face_detect')

def getDists(f1,f2):
    global angle
    global speed
    dists = []
    if(len(f1) and len(f1) == len(f2)):
        f1 = list(f1)
        f2 = list(f2)
        f1.sort(key = lambda x: x[2])
        f2.sort(key = lambda x: x[2])
        for (face1,face2) in zip(f1,f2):
            print(getDist(getAngle(face1)+1.5708,-getAngle(face2)+1.5708))
    else:
        angle = 0
        speed = 0


def getAngle(face):
    angPerPix = viewAngle / imageWidth
    pixel = (face[0] + face[2]/2)-imageWidth/2
    return pixel * angPerPix

def getDist(ang1,ang2):
    global angle
    global speed
    angle = ang1*180/3.14152-90
    speed = (camWidth*math.sin(ang1)*math.sin(ang2))/math.sin(ang1+ang2)
    if speed>100:
        speed = 25
    return (camWidth*math.sin(ang1)*math.sin(ang2))/math.sin(ang1+ang2)

class Motor:
    def __init__(self, pin, lowerLimit, upperLimit, lowerValLimit, upperValLimit, offSet=0,  invert=False):
        gpio.setup(pin, gpio.OUT)
        self.motor = gpio.PWM(pin, 50)
        self.motor.start(0)

        self.offSet = offSet
        self.inverted = invert
        self.pin = pin
        self.ll = lowerLimit
        self.ul = upperLimit
        self.lvl = lowerValLimit
        self.uvl = upperValLimit

    def set(self, val):
        ret = val
        if self.inverted:
            half = (self.uvl - self.lvl)/2 + self.lvl
            val = half-val+half
        if self.lvl<=val<=self.uvl:
            scale = 100/(self.ul-self.ll)
            duty = (((val/scale)+(self.ll+self.ul)/2)+self.offSet)/10+2
            gpio.output(self.pin, gpio.HIGH)
            self.motor.ChangeDutyCycle(duty)
        return ret

    def setPower(self, val):
        if 0<=val<=100:
            gpio.output(self.pin, gpio.HIGH)
            self.motor.ChangeDutyCycle(val)


class DriveMotor:
    def __init__(self, forward, reverse, forwardLimit, reverseLimit,):
        self.forward = forward
        self.reverse = reverse
        self.forwardLimit = forwardLimit
        self.reverseLimit = reverseLimit

    def set(self, val):
        if self.reverseLimit<=val<=self.forwardLimit:
            if val < 0:
                print("\tforward")
                self.forward.setPower(0)
                print("\treverse")
                self.reverse.setPower(-val)
            else:
                print("\treverse")
                self.reverse.setPower(0)
                print("\tforward")
                self.forward.setPower(val)

steer = Motor(12, 35, 65, -50, 50, 3)
forward = Motor(32, 0, 100, 0, 100)
reverse = Motor(35, 0, 100, 0, 100)
drive = DriveMotor(forward, reverse, 100, -100)

def motors():
    global angle
    global speed
    steer.set(int(angle*4))
    drive.set(speed*4)
    print("angle: ", angle*4)
    print("speed: ", speed*4)

tCam = threading.Thread(target=camera)

tCam.start()

