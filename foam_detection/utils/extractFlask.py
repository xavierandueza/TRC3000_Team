import cv2
import numpy as np
from utils.findBestContour import findBestContour
from utils.extendLines import extendLines

def extractFlask(image, canny):
    """
    This function extracts the flask from the image given canny edges, after perfoming
    different morphological operations
    :param image: coloured image containing flask
    :param canny: binary image of the canny edges
    :returns masked_image: image of the extract flask
    :returns box: contains [x, y, w, h] coords of the bounding box of the flask
    """
    # Extend any straight lines in the canny edges image to fill big gaps of the contour
    canny = extendLines(canny)

    # Closing any small gaps in the edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    canny = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # Filling all the contours white
    canny_filled = canny.copy()
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contours:
         cv2.fillPoly(canny_filled, pts=[c], color=255)
    # then eroding any external thin line contours
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    close = cv2.erode(canny_filled, kernel, iterations=4)
    close = cv2.dilate(close, kernel, iterations=4)

    # bit mask and extract flask object from the original image
    masked_edges = cv2.bitwise_and(canny, close)
    masked_edges = cv2.morphologyEx(masked_edges, cv2.MORPH_CLOSE, kernel, iterations=3)


    cv2.imshow("canny_ex", canny)
    cv2.imshow("masked_edges", masked_edges)
    cv2.waitKey(0)


    # Finding the best contour that matches the flask
    search_contour = cv2.imread("foam_detection/images/object_mask.jpg", 0)
    best_contour, box =  findBestContour(masked_edges, search_contour)
    
    # bit mask and extract flask object from the original image
    mask = np.zeros(image.shape, dtype = "uint8")
    cv2.fillPoly(mask, pts=[best_contour], color=(255,255,255))
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image, box