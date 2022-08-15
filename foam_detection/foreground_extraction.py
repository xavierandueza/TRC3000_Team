import cv2 as cv
import numpy as np
import os

# Normalise color hue and save them in a new directory - from color to grayscale
def normalise_hue(img_dir,grayscale_dir,width,height):
    for file in sorted(img_dir):
        filepath = ''
        if file.endswith('.JPG'):
            filepath = img_dir + '/' + file
            image = cv.imread(filepath)
            if image is None:
                break

            #change color to gray by using (r+g+b)*0.33
            for i in range(height):
                for j in range(width):
                    if image[i][j][0] != 0 or image[i][j][1] != 0 or image[i][j][2] != 0:
                        gray_value =sum(image[i][j])*0.33
                        image[i][j] =  [gray_value, gray_value,gray_value] 

            save_path = grayscale_dir + '/'+file
            cv.imwrite(save_path, image)


# apply background model 
def bg_learn(grayscale_dir):
    backSub = cv.createBackgroundSubtractorMOG2()

    for file in sorted(grayscale_dir):
        filepath = ''
        if file.endswith('.JPG'):
            filepath = grayscale_dir + '/' + file
            frame = cv.imread(filepath)
            if frame is None:
                print(file, None)
                break

            fgMask = backSub.apply(frame, learningRate=-0.5)
    return backSub


# apply foreground extraction
def bg_generate(grayscale_dir,bg_dir,backSub):
    for file in sorted(grayscale_dir):
        filepath = ''
        if file.endswith('.JPG'):
            filepath = grayscale_dir + '/' + file
            frame = cv.imread(filepath)
            if frame is None:
                print(file, None)
                break

            fgMask = backSub.apply(frame, learningRate=0)

            fgMask = np.expand_dims(fgMask,axis=2)
            fgMask[fgMask<=255/2] = 0
            fgMask[fgMask>255/2] = 1
            fgExtract = frame*fgMask

            save_path = bg_dir + '/'+file
            cv.imwrite(save_path, fgExtract)
            print(save_path,'done')

def foreground_extraction():
    pass