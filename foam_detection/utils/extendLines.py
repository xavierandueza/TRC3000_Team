import cv2
import numpy as np

def extendLines(canny):
    # Finding any lines in the canny edge image using HoughLines transform
    lines = cv2.HoughLinesP(canny,rho = 1,theta = 1*np.pi/180,threshold = 100,minLineLength = 100,maxLineGap = 50)

    # Drawing the lines onto the edges image to fill any gaps in the bottle contour
    N = lines.shape[0]
    for i in range(N):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]    
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]

        # Finding the angle of the lines
        m = (y2-y1)/(x2-x1)
        theta = np.arctan(m)*180/np.pi

        # Only keeping the lines that are not flat so we don't get the table
        if theta >30 or theta <-30:
            x0 = x1-40
            y0 = np.round(m*(x0-x1)+y1).astype(int)
            x3 = x2+40
            y3 = np.round(m*(x3-x1)+y1).astype(int)
            # Drawing the lines onto the image
            cv2.line(canny,(x0,y0),(x3,y3),255,2)
    return canny
