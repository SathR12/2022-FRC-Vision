import cv2 as cv
import numpy as np
import time

camera = cv.VideoCapture(0, cv.CAP_DSHOW)

#create trackbar
cv.namedWindow('Display')
cv.resizeWindow('Display', 500, 500)

def testing(x):
    pass

#HSV values
cv.createTrackbar("Hue Low", 'Display', 0, 255, testing)
cv.createTrackbar("Hue High", 'Display', 255, 255, testing)
cv.createTrackbar("Sat Low", 'Display', 0, 255, testing)
cv.createTrackbar("Sat High",'Display', 255, 255, testing)
cv.createTrackbar("Val Low", 'Display', 0, 255, testing)
cv.createTrackbar("Val High", 'Display', 255, 255, testing)

#Circle check and aspect ratio
cv.createTrackbar("Min Circle Check", 'Display', 0, 10, testing)
cv.createTrackbar("Max Circle Check", 'Display', 10, 10, testing)
cv.createTrackbar("Min Aspect Ratio", 'Display', 0, 10, testing)
cv.createTrackbar("Max Aspect Ratio", 'Display', 10, 10, testing)
cv.createTrackbar("Single Target", 'Display', 0, 1, testing)


def getDistance(focal_length, real_width, width_in_frame):
    distance = (real_width * focal_length) / width_in_frame
    
    return distance
 
def detectCargo(img, contour):
    min_circ_check = cv.getTrackbarPos("Min Circle Check",'Display') / 10
    max_circ_check = cv.getTrackbarPos("Max Circle Check", 'Display') / 10
    min_aspect = cv.getTrackbarPos("Min Aspect Ratio",'Display') / 10
    max_aspect = cv.getTrackbarPos("Max Aspect Ratio",'Display') / 10
    single_detect =  cv.getTrackbarPos("Single Target",'Display')
    
    if isCircle(contour, min_circ_check, max_circ_check, max_aspect, min_aspect):
        distance = getDistance(635, 24, int(w))
        distance = int(distance)
        quick_sort = sorted(contours, key = cv.contourArea, reverse = True)
        biggest_contour = cv.contourArea(quick_sort[0])
        
        if single_detect == 1 and contour_area == biggest_contour:
            cv.circle(img, center, int(radius), (0, 255, 0), 3)
            cv.circle(img, center, 2, (0, 255, 0) , 3) 
            cv.putText(img, "BALL " + str(distance) + " CM", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        elif single_detect == 0:
            cv.circle(img, center, int(radius), (0, 255, 0), 3)
            cv.circle(img, center, 2, (0, 255, 0) , 3) 
            cv.putText(img, "BALL " + str(distance) + " CM", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
            
def isCircle(contour, min_circ_check, max_circ_check, max_aspect, min_aspect):
    global contour_area, radius, center, w
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    center = (int(coord_x), int(coord_y))
    
    contour_area = cv.contourArea(contour) 
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h
    new_circle = max_circ_check >= contour_area / (radius**2 * 3.14) >= min_circ_check
    old_circle = (3.14 * cv.minEnclosingCircle(contour)[1] ** 2 - cv.contourArea(contour) < (3.14 * cv.minEnclosingCircle(contour)[1] ** 2) * (1 - 0.69))
    ratio = max_aspect >= aspect_ratio >= min_aspect and contour_area > 700
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
    global mask, res
    #blue values 
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    hue_low = cv.getTrackbarPos("Hue Low", 'Display')
    saturation_low = cv.getTrackbarPos("Sat Low", 'Display')
    value_low = cv.getTrackbarPos("Val Low", 'Display')
    
    hue_high = cv.getTrackbarPos("Hue High", 'Display')
    saturation_high = cv.getTrackbarPos("Sat High", 'Display')
    value_high = cv.getTrackbarPos("Val High", 'Display')
    

    lower = np.array([hue_low, saturation_low, value_low])
    upper = np.array([hue_high, saturation_high, value_high])
    mask = cv.inRange(hsv, lower, upper)
    res = cv.bitwise_and(frame, frame, mask = mask)
    
    return mask

while True:
    ret, frame = camera.read()
    for contour in getContours(createMask(frame)):
        detectCargo(frame, contour)
   
    
    concat = np.hstack((frame, res))
    cv.imshow('Display', concat)
    
    key = cv.waitKey(1)
    if key == 27:
        break
    
camera.release()
cv.destroyAllWindows()
