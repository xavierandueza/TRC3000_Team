import cv2
from utils.getEdges import getEdges
from utils.toBinary import toBinary

def getBoundingBox(image):
    binary = toBinary(image)
    canny = getEdges(binary, 1)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    best_contour = contours[0]
    box = cv2.boundingRect(best_contour)

    return box
