#Uses PyVision Library to detect bumper

import cv2 as cv
import numpy as np
import pytesseract
import sys

sys.path.append("/Users/cassini/Desktop/PyVision-main/src/models")
sys.path.append("/Users/cassini/Desktop/PyVision-main/src/util")
sys.path.append("/Users/cassini/Desktop/PyVision-main/src/OCR")
sys.path.append("/Users/cassini/Desktop/PyVision-main/src/tessexc")

import text_extraction
import contour_features
import detect_colors
import edit
import object_info

#image
frame = cv.imread(r"/Users/cassini/Desktop/blue_rect.jpeg")

#tesseract path differs for each operating system
text_extraction.setPath(r'/Usr/local/bin/tesseract')

#HSV Values for Blue Bumper 
LOWER_1 = [100, 150, 0]
LOWER_2 = [94,80,2]
UPPER_1 = [140,255,255]
UPPER_2 = [120,255,255]

#HSV Values for Red Bumper
LOW_1 = [0, 100, 100]
LOW_2 = [160, 100, 100]
UP_1 = [10, 255, 255]
UP_2 = [179, 255, 255]



def detectBlueBumper(frame):
    global mask_blue
    mask_blue = detect_colors.createDoubleMask(frame, LOWER_1, UPPER_1, LOWER_2, UPPER_2)
    mask_blue = cv.morphologyEx(mask_blue, cv.MORPH_CLOSE, (7,7))
    mask_blue = cv.morphologyEx(mask_blue, cv.MORPH_OPEN, (7,7))
    contours = contour_features.getContours(mask_blue)
    digits = text_extraction.extractText(mask_blue)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if cv.contourArea(contour) > 1000 and 4 >= w/h >= 1.9 and len(digits) >= 2:
            contour_features.drawBoundingRect(frame, contour)
            cv.putText(frame, "Blue Bumper", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(digits)
            
def detectRedBumper(frame):
    global mask_red
    mask_red = detect_colors.createDoubleMask(frame, LOW_1, UP_1, LOW_2, UP_2)
    mask_red = cv.morphologyEx(mask_red, cv.MORPH_CLOSE, (7,7))
    mask_red = cv.morphologyEx(mask_red, cv.MORPH_OPEN, (7,7))
    contours = contour_features.getContours(mask_red)
    digits = text_extraction.extractText(mask_red)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if cv.contourArea(contour) > 1000 and 4 >= w/h >= 1.9 and len(digits) >= 2:
            contour_features.drawBoundingRect(frame, contour)
            cv.putText(frame, "Red Bumper", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(digits)
    
    
    
    


detectBlueBumper(frame)
detectRedBumper(frame)
   

cv.imshow('frame', frame)
cv.imshow('red mask', mask_red)
key = cv.waitKey(0)







