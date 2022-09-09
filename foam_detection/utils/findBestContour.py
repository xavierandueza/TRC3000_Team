import numpy as np
import cv2
import math

def findBestContour(canny, search_contour):
    """
    Function to find the contour that best fits the shape of the search_contour. (flask)

    :param canny: binary image of the edges of the image
    :returns best_fit_contour: the contour that best fits the shape of the flask
    :returns box: contains [x, y, w, h] coords of the bounding box of the flask
    """
    # Use the canny edges to list out the contours
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_points = -math.inf
    for c in contours:
        if cv2.contourArea(c) > 0.1*canny.shape[1]**2:

            x,y,w,h = cv2.boundingRect(c)

            in_bounds = True
            if x < 0 or y < 0 or x+w <0 or y+h <0:
                in_bounds = False
            if x > 768 or y>768 or x+w > 768 or y+h > 768:
                in_bounds = False

            if True:
                contour_fill = np.zeros(canny.shape, dtype = "uint8")
                cv2.fillPoly(contour_fill, pts=[c], color=255)
                resized_mask = cv2.resize(search_contour, (w,h))
                mask = np.zeros(canny.shape, dtype = "uint8")
                mask[y:y+resized_mask.shape[0], x:x+resized_mask.shape[1]] = resized_mask

                

                points = 0
                for i in range(y, resized_mask.shape[0]):
                    for j in range(y, resized_mask.shape[1]):
                        # print(resized_mask.shape[0], resized_mask.shape[1], mask.shape, contour_fill.shape)
                        if (mask[i][j] == 0 and contour_fill[i][j] == 0) or (mask[i][j] == 255 and contour_fill[i][j] == 255): 
                            points += 1
                points = points/cv2.contourArea(c)
                
                if points > max_points:
                    max_points = points
                    print(points)
                    cv2.imshow("mask",mask)
                    cv2.waitKey(0)
                    best_fit_contour = c
                    box = [x, y, w, h]
    return best_fit_contour, box