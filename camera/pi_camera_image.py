from picamera import PiCamera
import time


camera = PiCamera()
camera.resolution = (640, 960) #set resolution
camera.vflip = False #set the camera upright


# camera.start_preview() #camera display on the screen
time.sleep(2) #sleep 5 seconds

#take photo after running the code for 2 seconds
camera.capture("foam_img.png")
#image taken is saved as jpg file in the same directory. Saved on desktop in this case
camera.close()
# time.sleep(1) #sleep 1 seconds
#  camera.stop_preview() #close camera display on the screen
