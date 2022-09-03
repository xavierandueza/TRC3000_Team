import cv2
import numpy as np

from utils.rescaleFrame import rescaleFrame
from utils.getEdges import getEdges
from utils.extractFlask import extractFlask
from utils.getDigestateInfo import getDigestateInfo


def main(image=None):

    # Reading the image (this usually will not be needed if an image is passed into this function)
    image = cv2.imread("foam_detection/images/2.jpg")
    
    # Rescaling the image to be maximum size of (768x768)
    scale = 768/max(image.shape[0],image.shape[1])
    image = rescaleFrame(image, scale)
    cv2.imshow("original image", image)

    # Finding the edges of the image using Canny Edge detector
    canny = getEdges(image, 3)
    cv2.imshow("canny", canny)

    # Extract the flask from the image using the canny edges and getting the bounding box
    masked_image, box = extractFlask(image, canny)
    x,y,w,h = box

    # Detecting edges again using Canny Edges method to find the water/foam levels
    canny = getEdges(masked_image, 3)
    cv2.imshow("canny", canny)    

    # Getting info about the digestate such as colour, amount, foaming etc
    digestate_info = getDigestateInfo(masked_image, canny, box)
    liquid_colour = digestate_info["digestate colour"]
    liquid_height = digestate_info["digestate height"]
    foam_height = digestate_info["foam height"]

    # Displaying the detected colour
    colour = np.zeros(image.shape, dtype = "uint8")
    for i in range(colour.shape[0]):
        for j in range(colour.shape[1]):
            colour[i][j] = liquid_colour
    cv2.imshow("colour", colour)

    # Displaying the detected digestate/liquid height
    cv2.line(masked_image, (x+(w//2), y+h-(liquid_height)), (x+(w//2),y+h), (0, 0, 255), 2) 
    string = "height in pixels: " + str(liquid_height)
    cv2.putText(masked_image,string, (x+(w//2)+3,y+h-(liquid_height//2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.imshow("masked", masked_image)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

