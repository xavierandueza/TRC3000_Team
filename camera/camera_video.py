from picamera import PiCamera
import time


camera = PiCamera()

#set camera resolution
camera.resolution = (640, 360)

#set camera position upright
camera.vflip = True

#turn on camera after 5 seconds when code runs
camera.start_preview()
time.sleep(5)

#start recording and stop after 3 seconds
camera.start_recording("videotest.h264") #video is saved as .h264 file
time.sleep(3)
camera.stop_recording()

time.sleep(2) #sleep 2 seconds
camera.stop_preview() #close camera display on the screen
