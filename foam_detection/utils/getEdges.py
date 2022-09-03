import cv2
import numpy as np

def getEdges(image, blur):
    kernel = np.array([[0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]], )
    image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    # cv2.imshow('sharpened image', image_sharp)

    # Apply Bilateral Blurring (to reduce noise while keeping edges sharp)
    # blurred = cv2.bilateralFilter(image_sharp, blur, 75, 75)
    blurred = cv2.GaussianBlur(image_sharp,(blur,blur),0)

    canny_edges = cv2.Canny(blurred, 45, 155)
    return canny_edges