import cv2
import numpy as np


def getEdges(image, blur):
    kernel = np.array([[0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]], )
    image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    cv2.imshow('sharpened image', image_sharp)

    # Apply Bilateral Blurring (to reduce noise while keeping edges sharp)
    # blurred = cv2.bilateralFilter(image_sharp, blur, 75, 75)
    blurred = cv2.GaussianBlur(image_sharp,(blur,blur),0)

    canny_edges = cv2.Canny(blurred, 45, 155)
    return canny_edges

def rescaleFrame(frame, scale):
    """
    Function to rescale an image based on a scale ratio
    :param frame: image to rescale
    :param scale: positive float representing scale
    :returns: rescaled image
    """
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_CUBIC)


image = cv2.imread("./object_mask.jpg", 0)

thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)[1]
cv2.imshow("img", thresh)
cv2.imwrite("object_mask.jpg", thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()