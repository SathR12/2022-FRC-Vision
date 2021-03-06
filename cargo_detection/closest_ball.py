import cv2 as cv
import numpy as np
import json

f = open("vision_data.json")
data = json.load(f)

#Image Path
camera = cv.VideoCapture(0)

#Distance function
def getDistance(focal_length, real_width, width_in_frame):
    distance = (real_width * focal_length) / width_in_frame
    
    return distance
    
#Draw circle if contour is a circle
def isCircle(img, contour, color):
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    center = (int(coord_x), int(coord_y))
    
    contour_area = cv.contourArea(contour) 
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h
      
    if  1.0 >= contour_area / (radius**2 * 3.14) >= .7 and 1.1 >= aspect_ratio >= .8 and contour_area > 700:
        distance = getDistance(200, 24, int(w))
        distance = int(distance)
        quick_sort = sorted(contours, key = cv.contourArea, reverse = True)
        biggest_contour = cv.contourArea(quick_sort[0])
        color_bound = tuple(data["bounding_colors"]["detected_balls"])
        
        
        if contour_area == biggest_contour:
            color_bound = tuple(data["bounding_colors"]["closest_ball"])
            
    
            
        cv.circle(img, center, int(radius), color_bound , 3)
        cv.circle(img, center, 2, color_bound , 3)
        cv.putText(img, color.upper() + " BALL " + str(distance) + " CM", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    
        
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
    
    

def createBlueMask(img):
    global mask_blue
    #blue values 
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_blue_1 = np.array(data["hsv_blue"]["lower_1"])
    upper_blue_1 = np.array(data["hsv_blue"]["upper_1"])
    mask_blue_1 = cv.inRange(hsv, lower_blue_1, upper_blue_1)
    
    lower_blue_2 = np.array(data["hsv_blue"]["lower_2"])
    upper_blue_2 = np.array(data["hsv_blue"]["upper_2"])
    mask_blue_2 = cv.inRange(hsv, lower_blue_2, upper_blue_2)
    
    mask_blue = mask_blue_1 + mask_blue_2
    
    
    return mask_blue
        

def createRedMask(img):
    global mask_red
    #red values
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    lower_red_1 = np.array(data["hsv_red"]["lower_1"])
    upper_red_1 = np.array(data["hsv_red"]["upper_1"])
    mask_red_1 = cv.inRange(hsv, lower_red_1, upper_red_1)

    lower_red_2 = np.array(data["hsv_red"]["lower_2"])
    upper_red_2 = np.array(data["hsv_red"]["upper_2"])
    mask_red_2 = cv.inRange(hsv, lower_red_2, upper_red_2)
    mask_red = mask_red_1 + mask_red_2
    

    return mask_red

#Call functions and process feed
while True:
    ret, frame = camera.read()
    
    
    for contour in getContours(createBlueMask(frame)):
        isCircle(frame, contour, "blue")
    
    for contour in getContours(createRedMask(frame)):
        isCircle(frame, contour, "red")
    
    #show windows
    cv.imshow("Detected Balls", frame)
    
    #break loop if key pressed
    key = cv.waitKey(1)
    if key == 27:
        break
       
  
camera.release()  
cv.destroyAllWindows()