import cv2 as cv
import numpy as np

camera = cv.VideoCapture(0, cv.CAP_DSHOW)

# runPipeline() is called every frame by Limelight's backend.
def isCircle(contour):
    global contour_area, radius, center
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    center = (int(coord_x), int(coord_y))
    
    contour_area = cv.contourArea(contour) 
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h
    new_circle = 1.0 >= contour_area / (radius**2 * 3.14) >= .7
    old_circle = (3.14 * cv.minEnclosingCircle(contour)[1] ** 2 - cv.contourArea(contour) < (3.14 * cv.minEnclosingCircle(contour)[1] ** 2) * (1 - 0.69))
    ratio = 1.1 >= aspect_ratio >= .9 and contour_area > 700
    if old_circle and new_circle and ratio and len(approx) > 8: 
        return True
    
    return False

def getContours(mask):
    global contours
    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 2:
        contours = contours[0]
        
    else:
        contours = contours[1]
    
    return contours

def createMask(frame):
    frame = cv.GaussianBlur(frame, (3, 3), None)
    frame = cv.morphologyEx(frame, cv.MORPH_CLOSE, (7,7))
    frame = cv.morphologyEx(frame, cv.MORPH_OPEN, (3,3))
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_blue = np.array([86,77,25])
    upper_blue = np.array([114,255,255])
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    return mask_blue

def runPipeline(frame):
    # initialize an empty array of values to send back to the robot
    llpython = [0,0,0,0,0,0,0,0]
    # convert the input image to the HSV color space
    largestContour = np.array([[]])
    for contour in getContours(createMask(frame)):
        if isCircle(contour):
            largestContour = max(contours, key=cv.contourArea)
            if cv.contourArea(contour) == cv.contourArea(largestContour):
                x, y, w, h = cv.boundingRect(contour)
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                llpython = [1,x,y,w,h,9,8,7]
        
            
            
        
    
    # if contours have been detected, draw them
    #return the largest contour for the LL crosshair, the modified image, and custom robot data
    return largestContour, frame, llpython
    
while True:
    ret, frame = camera.read()
    runPipeline(frame)
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == 27:
        break

runPipeline()    
camera.release()
cv.destroyAllWindows()

