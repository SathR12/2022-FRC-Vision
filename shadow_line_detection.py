#Code belongs to cchen6479 and Nlin004

from turtle import pensize
import numpy as np
import math
import cv2 as cv 
import json

# from find_parallel_lines import find_parallel_lines
source = 0 #0 is native, 1 is external webcam
camera = cv.VideoCapture(source, cv.CAP_DSHOW)

MIN_AREA = 500

def sobel_edge(frame):
    depth = cv.CV_16S
    scale = 1
    delta = 0

    frame = cv.GaussianBlur(frame, (3,3), 0)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    grad_x = cv.Sobel(gray, depth, 1,0,ksize=3, scale = scale, delta = delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(gray, depth, 0, 1, ksize=3, scale = scale, delta = delta, borderType=cv.BORDER_DEFAULT)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad

def laplace_edge(frame):
    ddepth = cv.CV_16S
    kernel_size = 3
    src = cv.GaussianBlur(frame, (3,3), 0)
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # dst = cv.adaptiveThreshold(src_gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    # dst  = cv.Canny(src_gray, 50, 150, apertureSize=3)
    dst = cv.Laplacian(src_gray, ddepth, ksize=kernel_size)
    abs_dst = cv.convertScaleAbs(dst)
    return abs_dst

def isRect(cnt, approx, ar):
    return len(approx) == 4  and cv.contourArea(cnt) > MIN_AREA and  (0.3 <= ar <= 1.7)

def maskColor(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5,5), 3)
    ret, thresh = cv.threshold(blurred, 45, 255, cv.THRESH_BINARY_INV)
    thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, (13,13))
    # thresh = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
    return thresh

def findRect(frame, output):

    contours, _ = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    angles = []
    
    for(index, contour) in enumerate(contours):
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.01 * peri, True)
        x,y,w,h = cv.boundingRect(approx)
        aspect_ratio = w / h
        
        if isRect(contour, approx, aspect_ratio):
            rect = cv.minAreaRect(contour)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            # cv.drawContours(output, [box], 0, (0, 255, 0), 2)
            p1, p2 = get_longest_line(box)
            cv.line(output, p1, p2, (255, 255, 255), 3)
            ang = get_angle(p1, p2)
            angles.append(ang)
            cv.putText(output, f"{str(ang)} degrees", (int(x), int(y-10)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255,255))

def get_longest_line(box):
    midpoints = [get_midpoint(box[i], box[(i + 1) % 4]) for i in range(4)]
    d1 = get_distance(midpoints[3], midpoints[1])
    d2 = get_distance(midpoints[0], midpoints[2])

    if d1 > d2:
        return (midpoints[3], midpoints[1])
    else:
        return (midpoints[0], midpoints[2])
    

def get_midpoint(p1, p2):
    x = (p1[0] + p2[0])/2
    y = (p1[1] + p2[1])/2
    return(int(x), int(y))

def get_distance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

def get_angle(p1,p2):
    dy = (p1[0] - p2[0])
    if dy != 0:
        m = (p1[1] - p2[1])/dy
    else:
        m = 0
    return format(math.atan(m) * -180 / math.pi, '.0f')    

         

def detect_line(frame, get_data = False):
    masked_frame = maskColor(frame)

    angles = findRect(masked_frame, frame)

    if get_data:
        print(angles)
        return angles
    else:
        return frame


if __name__ == "__main__":
    while True:
        _, frame = camera.read()
        output = detect_line(frame)
        cv.imshow("frame", output)
        key = cv.waitKey(1)
        if key == 27:
             break
            
camera.release()
cv.destroyAllWindows()


