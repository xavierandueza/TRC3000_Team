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
    # cv2.imshow('sharpened image', image_sharp)

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

    max_points = -math.inf
    for c in contours:
        if cv2.contourArea(c) > 0.1*canny.shape[1]**2:

            x,y,w,h = cv2.boundingRect(c)

            in_bounds = True
            if x < 0 or y < 0 or x+w <0 or y+h <0:
                in_bounds = False
            if x > 768 or y>768 or x+w > 768 or y+h > 768:
                in_bounds = False

            if in_bounds:
                contour_fill = np.zeros(canny.shape, dtype = "uint8")
                cv2.fillPoly(contour_fill, pts=[c], color=255)
                resized_mask = cv2.resize(search_contour, (w,h))
                mask = np.zeros(canny.shape, dtype = "uint8")
                mask[y:y+resized_mask.shape[0], x:x+resized_mask.shape[1]] = resized_mask

                cv2.imshow("mask",mask)
                cv2.waitKey(0)

                points = 0
                for i in range(y, resized_mask.shape[0]):
                    for j in range(y, resized_mask.shape[1]):
                        # print(resized_mask.shape[0], resized_mask.shape[1], mask.shape, contour_fill.shape)
                        if (mask[i][j] == 0 and contour_fill[i][j] == 0) or (mask[i][j] == 255 and contour_fill[i][j] == 255): 
                            points += 1
                points = points/cv2.contourArea(c)
                if points > max_points:
                    best_fit_contour = c
                    box = [x, y, w, h]
    
    return best_fit_contour, box

def colour_detection(image=None):

    image = cv2.imread("foam_detection/images/2_yellow.jpg")
    
    scale = 768/max(image.shape[0],image.shape[1])
    image = rescaleFrame(image, scale)
    
    cv2.imshow("original image", image)

    binary = toBinary(image)
    # cv2.imshow("binary", binary)

    canny = getEdges(image, 3)
    # cv2.imshow("canny", canny)

    lines = cv2.HoughLinesP(canny,rho = 1,theta = 1*np.pi/180,threshold = 100,minLineLength = 100,maxLineGap = 50)


    # Draw the lines
    N = lines.shape[0]
    for i in range(N):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]    
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]
        m = (y2-y1)/(x2-x1)
        theta = np.arctan(m)*180/np.pi
        if theta >30 or theta <-30:
            x0 = x1-40
            y0 = np.round(m*(x0-x1)+y1).astype(int)
            x3 = x2+40
            y3 = np.round(m*(x3-x1)+y1).astype(int)
            
            cv2.line(canny,(x0,y0),(x3,y3),255,2)

    # cv2.imshow("lines", canny)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        cv2.fillPoly(close, pts=[c], color=255)

    close = cv2.erode(close, kernel, iterations=4) 

    # cv2.imshow("close", close)
    
    search_contour = cv2.imread("foam_detection/images/object_mask.jpg", 0)

    best_contour, box =  findBestContour(close, search_contour)
    x,y,w,h = box

    # bit mask and extract object
    mask = np.zeros(image.shape, dtype = "uint8")
    cv2.fillPoly(mask, pts=[best_contour], color=(255,255,255))
    masked_image = cv2.bitwise_and(image, mask)

    cv2.imshow("masked", masked_image)

    canny = getEdges(masked_image, 3)
    cv2.imshow("canny", canny)    

    for i in range(h):
        if canny[y+h-(i+1)][canny.shape[1]//2] == 255 and i>50:
            liquid_height = i
            break

    liquid_colour = masked_image[y+h-(liquid_height//2)][x+(w//2)]
    colour = np.zeros(image.shape, dtype = "uint8")
    for i in range(colour.shape[0]):
        for j in range(colour.shape[1]):
            colour[i][j] = liquid_colour
    
    cv2.imshow("colour", colour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

colour_detection()

