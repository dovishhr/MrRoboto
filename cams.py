import math
import cv2
import threading
from time import sleep

camWidth = 2.6
viewAngle = 0.82
bugeye = 0.01
imageWidth = 320

angle = 0
speed = 0

# Enable camera
cap1 = cv2.VideoCapture(0)
cap1.set(3, imageWidth)
cap1.set(4, 210)
cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap2 = cv2.VideoCapture(2)
cap2.set(3, imageWidth)
cap2.set(4, 210)
cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# import cascade file for facial recognition
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def getPositions():
    success, img1 = cap1.read()
    imgGray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    faces1 = faceCascade.detectMultiScale(imgGray, 1.3, 5) 
    for (x, y, w, h) in faces1:
        img = cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #cv2.imshow('cam1', img1)

    success, img2 = cap2.read()
    imgGray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # Getting corners around the face
    faces2 = faceCascade.detectMultiScale(imgGray, 1.3, 4)  # 1.3 = scale factor, 5 = minimum neighbor
    # drawing bounding box around face
    for (x, y, w, h) in faces2:
        img = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #cv2.imshow('cam2', img2)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        pass
    dists = getDists(faces1,faces2);
    headings = getHeadings(faces1,faces2);
    positions = []
    for (dist, heading) in zip(dists, headings):
        positions.append((dist, heading))
    return positions


def getHeadings(f1,f2):
    headings = []
    if(len(f1) and len(f1) == len(f2)):
        f1 = list(f1)
        f2 = list(f2)
        f1.sort(key = lambda x: x[2])
        f2.sort(key = lambda x: x[2])
        a1 = convertToAngles(f1)
        a2 = convertToAngles(f2)
        for (angle1,angle2) in zip(a1,a2):
            headings.append(getHeading(angle1,angle2))
    return headings

def getHeading(ang1,ang2):
    ang1 += bugeye
    ang2 -= bugeye
    angle1 = ang1*180/3.14152-90
    angle2 = ang2*180/3.14152-91
    return (angle1+angle2)


def getDists(f1,f2):
    dists = []
    if(len(f1) and len(f1) == len(f2)):
        f1 = list(f1)
        f2 = list(f2)
        f1.sort(key = lambda x: x[2])
        f2.sort(key = lambda x: x[2])
        a1 = convertToAngles(f1)
        a2 = convertToAngles(f2)
        for (angle1,angle2) in zip(a1,a2):
            dists.append(getDist(angle1,-angle2))
    return dists

def convertToAngles(faces):
    angles = []
    for face in faces:
        angles.append(getAngle(face)+1.5708)
    return angles

def getAngle(face):
    angPerPix = viewAngle / imageWidth
    pixel = (face[0] + face[2]/2)-imageWidth/2
    return pixel * angPerPix

def getDist(ang1,ang2):
    ang1 += bugeye
    ang2 -= bugeye
    angle1 = ang1*180/3.14152-90
    angle2 = ang2*180/3.14152-90
    #print(angle1, angle2)
    return (camWidth*math.sin(ang1)*math.sin(ang2))/math.sin(ang1+ang2)


#while True:
#    print(set(getPositions()))
#    sleep(0.01)

