# Python code for Multiple Color Detection 

import numpy as np 
import cv2 

def colourBlockDetection(imageFrame, viz, bgr):
    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    bgr = np.uint8([[bgr]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hsv = np.squeeze(np.squeeze(hsv))


    # Set range for red color and 
    # define mask 

    h_thresh = 50
    s_thresh = 70
    v_thresh = 70
    minHSV = np.array([hsv[0] - h_thresh, hsv[1] - s_thresh, hsv[2] - v_thresh])
    if minHSV[0] <= 0:
        minHSV[0] = 1
    if minHSV[1] <= 0:
        minHSV[1] = 1
    if minHSV[2] <= 0:
        minHSV[2] = 1


    maxHSV = np.array([hsv[0] + h_thresh, hsv[1] + s_thresh, hsv[2] + v_thresh])
    mask = cv2.inRange(hsvFrame, minHSV, maxHSV)


    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernal = np.ones((5, 5), "uint8") 

    # For red color 
    mask = cv2.erode(mask, kernal) 
    mask = cv2.dilate(mask, kernal, iterations=2) 
    res = cv2.bitwise_and(imageFrame, imageFrame, mask = mask) 

    # cv2.imshow("colour_mask", mask)
    # print(hsv)
    # print(minHSV)
    # print(maxHSV)


    # Creating contour of colour blob
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    max_contour = sorted(contours, key = cv2.contourArea, reverse=True)[0]
    if cv2.contourArea(max_contour) > 300: 
        x, y, w, h = cv2.boundingRect(max_contour) 
        viz = cv2.rectangle(viz, (x, y), (x + w, y + h), (255, 0, 0), 2) 
        # cv2.putText(viz, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    return viz