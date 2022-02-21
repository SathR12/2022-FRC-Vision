import cv2 as cv
import numpy as np

images = ["F:\sathya\hub3.jpeg", "F:\sathya\hub2.jpeg", "F:\sathya\hub1.jpeg", "F:\sathya\hub4.jpeg"]



def createMask(frame):
    global mask
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array([7, 44, 101])
    upper = np.array([37, 134, 255])
    mask = cv.inRange(hsv, lower, upper)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, (7,7))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, (3,3))
    
   
    return mask



def getContours(mask):
    global contours
    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 2:
        contours = contours[0]
       
    else:
        contours = contours[1]
   
    return contours

def drawHub(frame, contours):
    largestContour = max(contours, key = cv.contourArea)
    approx = cv.approxPolyDP(largestContour, 0.01 * cv.arcLength(largestContour, True), True)
    x, y, w, h = cv.boundingRect(largestContour)
    aspect_ratio = w/h
    if len(approx) > 15 and 1 >= aspect_ratio >= .6:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

for i in images:
    frame = cv.imread(i)
    frame = cv.GaussianBlur(frame, (7, 7), 0)
    map(drawHub(frame, getContours(createMask(frame))), i)
    cv.imshow("frame", frame)
    cv.imshow("mask", mask)
    cv.waitKey(0)
    cv.destroyAllWindows()


   
   

