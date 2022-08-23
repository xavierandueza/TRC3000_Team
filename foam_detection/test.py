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


image = cv2.imread("foam_detection/images/contour/contour_paint_thick.jpg")
image = cv2.resize(image, (768, 768), interpolation=cv2.INTER_CUBIC)
img = np.zeros(image.shape, dtype = "uint8")

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        if image[i][j][0] == 255 or image[i][j][1] == 255 or image[i][j][2] == 255:
            img[i][j] = [255, 255, 255] 

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

canny_edges = cv2.Canny(img, 0, 0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
close = cv2.morphologyEx(canny_edges, cv2.MORPH_CLOSE, kernel, iterations=1)


contours, hierarchy = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key =cv2.contourArea)


output_img = np.zeros(img.shape, dtype = "uint8")
cv2.fillPoly(output_img, pts =contours[-1], color=(255,255,255))
canny_edges = cv2.Canny(output_img, 0, 0)


contours, hierarchy = cv2.findContours(canny_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for i in range(len(contours)):
    cv2.fillPoly(output_img, pts =contours[i], color=(255,255,255))

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
close = cv2.morphologyEx(output_img, cv2.MORPH_OPEN, kernel, iterations=5)

canny_edges = cv2.Canny(close, 0, 0)
contours, hierarchy = cv2.findContours(canny_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for i in range(len(contours)):
    cv2.fillPoly(output_img, pts =contours[i], color=(255,255,255))

cv2.imwrite("object_mask.jpg", output_img)

# canny = getEdges(image, 3)
# canny1 = rescaleFrame(canny, 0.2)
# contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# cv2.imshow("canny", canny1)
# cv2.waitKey(0)

# img = np.zeros(image.shape)
# cv2.fillPoly(img, pts =[sorted(contours)[1]], color=(255,255,255))
cv2.imshow("img", output_img)

cv2.waitKey(0)
cv2.destroyAllWindows()