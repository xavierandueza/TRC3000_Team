import cv2
import numpy as np

def extendLines(canny):
    """
    Function that finds any straight lines in an image and draws an extended white line over it.
    (purpose is to fill any gaps in edge contours of our flask)
    
    :param canny: The image to find the lines on
    :returns: image with the extended lines drawn
    """
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
        if x2 == x1:
            theta = 90
        else:
            m = (y2-y1)/(x2-x1)
            theta_rad = np.arctan(m)
            theta = theta_rad *180/np.pi

        # calculate the length to extend by
        length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        length_to_extend = 0.39*length

        # Only keeping the lines that are not flat so we don't get the table
        if theta >30 or theta <-30:
            # calculating coordinates of lines after extension
            if theta != 90:
                x0 = np.round(x1-length_to_extend*np.cos(theta_rad)).astype(int)
                x3 = np.round(x2+length_to_extend*np.cos(theta_rad)).astype(int)
                y0 = np.round(y1-length_to_extend*np.sin(theta_rad)).astype(int)
                y3 = np.round(y2+length_to_extend*np.sin(theta_rad)).astype(int)
            else:
                x0 = x1
                x3 = x2
                y0 = np.round(y1-length_to_extend).astype(int)
                y3 = np.round(y2+length_to_extend).astype(int)

            # Drawing the lines onto the image
            cv2.line(canny,(x0,y0),(x3,y3),255,2)
    return canny
