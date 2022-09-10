import rembg
import cv2
import numpy as np
import os


filepath = "foam_detection/images"
savepath = "foam_semantic_segmentation/images"

for img in os.listdir(filepath):
    if img.endswith('.jpg') or img.endswith('.png') or img.endswith('.JPG'):
        image = cv2.imread(filepath + '/' + img)
        output = rembg.remove(image)
        output = cv2.cvtColor(output, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(savepath + '/' + img, output)