import cv2 as cv
import numpy as np

camera = cv.VideoCapture(0)

def getDistance(focal_length, real_width, width_in_frame):
    distance = (real_width * focal_length) / width_in_frame
    
    return distance

def createOutline(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)
    canny = cv.Canny(gray, 30, 150, 10)
    canny = cv.dilate(canny, None, iterations = 1)
    canny = cv.morphologyEx(canny, cv.MORPH_CLOSE, (7,7))
    canny = cv.morphologyEx(canny, cv.MORPH_OPEN, (7,7))
    
    return canny

def getContours(img):
    contours = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 2:
        contours = contours[0]
       
    else:
        contours = contours[1]
   
    return contours

def detectCircles(img, contour):
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    contour_area = cv.contourArea(contour)
    center = (int(coord_x), int(coord_y))
    
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h
    circle_check = (3.14 * cv.minEnclosingCircle(contour)[1] ** 2 - contour_area < (3.14 * cv.minEnclosingCircle(contour)[1] ** 2) * (1 - 0.7))
    if len(approx) > 8 and contour_area > 400 and circle_check and 1.1 >= aspect_ratio > .8:
        distance = getDistance(630, 24.13, int(w))
        distance = format((int(distance) * 1.1) / 100, '.2f')
        cv.circle(img, center, int(radius), (0, 255, 0), 3)
        cv.putText(img, "Circle Detected " + str(distance) + " M", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        

while True:
    ret, frame = camera.read()
    copy_frame = frame.copy()
    for contour in getContours(createOutline(copy_frame)):
        detectCircles(frame, contour)
    
    cv.imshow("frame", frame)
    cv.imshow("canny", createOutline(copy_frame))
    key = cv.waitKey(1)
    if key == 27:
        break

camera.release()
cv.destroyAllWindows()
