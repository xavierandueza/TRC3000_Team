import rembg
import cv2
import numpy as np
from utils.rescaleFrame import rescaleFrame
from utils.getEdges import getEdges
from utils.getDigestateInfo import getDigestateInfo
from utils.toBinary import toBinary
from utils.getBoundingBox import getBoundingBox
from utils.removeGlare import removeGlare

def main(image = None):
    image = cv2.imread("foam_detection/foaming_images/Yellowx3_foamx3.jpg")
    # image = cv2.imread("foam_detection/images/fg1.jpg")
    scale = 768/max(image.shape[0],image.shape[1])
    image = rescaleFrame(image, scale)

    #########################################################################################################
    # Removing the backgorund using AI method from rembg package
    output = rembg.remove(image)
    output = cv2.cvtColor(output, cv2.COLOR_BGRA2BGR)
    # # Optional: Remove Glare
    # output = removeGlare(output, 210)
    cv2.imshow("removed_background", output)

    #########################################################################################################
    # Get the bounding box of the flask
    box = getBoundingBox(output)
    x, y, w, h = box

    #########################################################################################################
    # Extract important digestate info from image and canny edges
    digestate_info = getDigestateInfo(output, box)
    liquid_colour = digestate_info["digestate colour"]
    liquid_height = digestate_info["digestate height"]
    foam_height = digestate_info["foam height"]

    #########################################################################################################
    # Displaying the detected colour
    colour = np.zeros(image.shape, dtype = "uint8")
    for i in range(colour.shape[0]):
        for j in range(colour.shape[1]):
            colour[i][j] = liquid_colour
    cv2.imshow("colour_of_liquid", colour)

    #########################################################################################################
    # Displaying the detected digestate/liquid height
    cv2.line(output, (x+(w//2), y+h-(liquid_height)), (x+(w//2),y+h), (0, 0, 255), 2)
    string = "height in pixels: " + str(liquid_height)
    cv2.putText(output,string, (x+(w//2)+3,y+h-(liquid_height//2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.imshow("final_output", output)

    print(foam_height)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()