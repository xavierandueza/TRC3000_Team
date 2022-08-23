import cv2
import numpy as np
import math

# Rescaling image
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

def toBinary(image):
    """
    Function to convert an image to binary version using OTSU thresholding

    :param image: The OpenCV cv::Mat BGR image
    :returns: Binary image
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Bilateral Blurring (to reduce noise while keeping edges sharp)
    blur = cv2.bilateralFilter(gray, 5, 75, 75)
    # Converting blurred image into binary image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # cv2.imshow('thresh',thresh)

    return thresh

def extractFlask(binary_image):
    pass

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

def findBestContour(canny, search_contour):
    """
    Function to find the contours in the closed binary image that best fit the shape of a pipe (rectangle)

    :param closed_bianry: Binary image that has undergone closing and opening morphological operations
    :returns: large contour that best fits a rectangular shape
    """
    # Use the canny edges to list out the contours
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Finding the contour that fits the best into a rectangle
    for c in contours:
        if cv2.contourArea(c) > 0.1*canny.shape[1]**2:
            best_fit_contour = c
            break

    min_area = math.inf
    print(len(contours))
    for c in contours:
        if cv2.contourArea(c) > 0.1*canny.shape[1]**2:
            # Fit contours into a rectangular box with minimum area
            min_rect = cv2.minAreaRect(c)

            # calculate box points
            box = cv2.boxPoints(min_rect)
            box = np.intp(box)

            in_bounds = True
            for i in range(len(box)):
                for j in range(len(box[0])):
                    if box[i][j] < 0:
                        in_bounds = False

            if in_bounds:
                print(box)
                # calculate area of rectangle
                x = math.sqrt(((box[0][0] - box[1][0]) ** 2) + ((box[0][1] - box[1][1])) ** 2)
                y = math.sqrt(((box[0][0] - box[3][0]) ** 2) + ((box[0][1] - box[3][1])) ** 2)
                box_area = x*y

                if (box_area - cv2.contourArea(c))/box_area < min_area:
                    best_fit_contour = c
                    min_area = (box_area - cv2.contourArea(c))/box_area

    return best_fit_contour

def colour_detection(image=None):

    image = cv2.imread("foam_detection/images/2.jpg")
    
    scale = 768/max(image.shape[0],image.shape[1])
    image = rescaleFrame(image, scale)
    
    cv2.imshow("original image", image)

    binary = toBinary(image)
    cv2.imshow("binary", binary)

    canny = getEdges(image, 3)
    cv2.imshow("canny", canny)

    lines = cv2.HoughLines(canny,1,np.pi/180,130)

    # Draw the lines
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            theta_deg =theta*180/np.pi
            if theta_deg < 60 or theta_deg > 150: 
                print(theta_deg)
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(canny, pt1, pt2, (255,255,255), 2, cv2.LINE_AA)

    cv2.imshow("lines", canny)
    cv2.imwrite("outline.jpg", canny)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=1)
    cv2.imshow("close", close)

    search_contour = cv2.imread("foam_detection/images/contour/outline.jpg")

    best_contour =  findBestContour(close, search_contour)
    
    # bit mask and extract object
    mask = np.zeros(image.shape, dtype = "uint8")
    cv2.fillPoly(mask, pts=[best_contour], color=(255,255,255))
    masked_image = cv2.bitwise_and(image, mask)

    cv2.imshow("masked", masked_image)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

colour_detection()

