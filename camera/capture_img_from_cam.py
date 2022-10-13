from picamera import PiCamera
import time
import cv2
import numpy as np

def capture_img_from_cam():
    camera = PiCamera()
    camera.resolution = (608, 423) #set resolution
    camera.vflip = True #set the camera upright

    time.sleep(2)
    output = np.empty((600, 420, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    return output

if __name__ == "__main__":
    img = capture_img_from_cam()
    cv2.imwrite("foam_img.png", img)                                                                               