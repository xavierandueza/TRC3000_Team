import cv2

def removeGlare(image, threshold):
    # convert to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # threshold grayscale image to extract glare
    mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
    # use mask with input to do inpainting
    output = cv2.inpaint(image, mask, 25, cv2.INPAINT_TELEA) 
    return output