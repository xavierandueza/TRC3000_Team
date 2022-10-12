import cv2

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
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow('thresh',thresh)

    return thresh