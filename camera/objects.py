#This file contains examples of camera objects and is not intended for use

cam1 = Camera("Logitech c720", 0)
cam2 = Camera("Gopro 5", 0)
cam2.setDimensions(1000, 500)
cam1.setDimensions(640, 480)
cam1.setExposure(-7)
cam1.setSource(0)
cam1.initialize()
cam1.displayFeed()
