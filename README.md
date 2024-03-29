# 2022-FRC-Vision

My vision coding projects for the 2022 FRC robotics tournaments used by the vision team

## Overview:

cargo_detection folder contains official python scripts that detects blue and red cargo

Hub detection folder is work-in-progress.

Limelight folder has custom cargo detection scripts.


## Approach to Circle Detection

```py
def isCircle(img, contour, color):  
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
   
    (coord_x, coord_y), radius = cv.minEnclosingCircle(contour)
    center = (int(coord_x), int(coord_y))
   
    contour_area = cv.contourArea(contour)
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = w/h

   
    if  1.0 >= contour_area / (radius**2 * 3.14) >= .8 and 1.1 >= aspect_ratio >= .8 and contour_area > 200:
            return True
    return False
 ```

 
## Dependencies:

Python

OpenCV package

Numpy package

PyVision Package - https://github.com/SathR12/PyVision

## How to run:

Save the python code and the images in the same directory.
Input the filename for the picture.
If you are running the live feed, place the ball in the frame and hopefully it should detect the cargo.

## Output:
You will have windows displaying the detected objects.
The detected object will have a green rectangular box/ green circle around it, depending on which version you are running. 
It will display distance and center coordinates to help Robot Code align. 


![image](https://user-images.githubusercontent.com/74515743/157141048-23eee427-241b-450f-a55e-3b7c30a72cd2.png)

## Bumper detection in-progress:

<img width="764" alt="Screen Shot 2022-03-12 at 8 39 56 PM" src="https://user-images.githubusercontent.com/74515743/158041176-59e0f6e4-ae35-4fa9-99b3-a8246f5127af.png">
