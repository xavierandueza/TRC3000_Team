import rembg
import cv2
import numpy as np
from utils.rescaleFrame import rescaleFrame
from utils.getEdges import getEdges
from utils.getDigestateInfo import getDigestateInfo
from utils.toBinary import toBinary
from utils.getBoundingBox import getBoundingBox
from utils.removeGlare import removeGlare
from utils.getFoamFromModel import getFoamFromModel

def main(image = None):
    # image = cv2.imread("foam_detection/images/clear.jpg")
    # image = cv2.imread("foam_detection/images/fg1.jpg")
    image = cv2.imread("foam_detection/foaming_images/Yellowx3_foamx5.jpg")
    scale = 720/max(image.shape[0],image.shape[1])
    image = rescaleFrame(image, scale)

    #########################################################################################################
    # Removing the backgorund using AI method from rembg package
    flask_img = rembg.remove(image)
    flask_img = cv2.cvtColor(flask_img, cv2.COLOR_BGRA2BGR)
    # # Optional: Remove Glare
    # flask_img = removeGlare(flask_img, 210)
    cv2.imshow("removed_background", flask_img)

    #########################################################################################################
    # Get the bounding box of the flask
    box = getBoundingBox(flask_img)
    x, y, w, h = box

    #########################################################################################################   
    # Get bounding box of the foam using trained mask rcnn model
    no_foam = False
    foam_bbox, viz = getFoamFromModel(flask_img)
    if foam_bbox == None:
        no_foam = True
    # cv2.imshow("final_output", viz)
    #########################################################################################################
    # Extract important digestate info from image and canny edges
    digestate_info = getDigestateInfo(flask_img, box, foam_bbox)
    liquid_colour = digestate_info["digestate colour"]
    liquid_height = digestate_info["digestate height"]
    if not no_foam:
        foam_height = digestate_info["foam height"]
        foam_colour = digestate_info["foam colour"]

    #########################################################################################################
    # Displaying the detected colour
    colour = np.zeros(image.shape, dtype = "uint8")
    for i in range(colour.shape[0]):
        for j in range(colour.shape[1]):
            colour[i][j] = liquid_colour
    cv2.imshow("colour_of_liquid", colour)

    # Displaying the detected foam colour
    if not no_foam:
        colour_foam = np.zeros(image.shape, dtype = "uint8")
        for i in range(colour_foam.shape[0]):
            for j in range(colour_foam.shape[1]):
                colour_foam[i][j] = foam_colour
        cv2.imshow("colour_of_foam", colour_foam)

    #########################################################################################################
    # Displaying the detected digestate/liquid height
    cv2.line(viz, (x+(w//2), y+h-(liquid_height)), (x+(w//2),y+h), (0, 0, 255), 2)
    string = "height in pixels: " + str(liquid_height)
    cv2.putText(viz,string, (x+(w//2)+3,y+h-(liquid_height//2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    # Displaying the detected foam height
    if not no_foam:
        cv2.line(viz, (x+(w//2), int(foam_bbox[1])), (x+(w//2), int(foam_bbox[3])), (0, 255, 0), 2)
        string = "height in pixels: " + str(foam_height)
        cv2.putText(viz,string, (x+(w//2)+3,int(abs(foam_bbox[3]-foam_bbox[1]))+int(min(foam_bbox[1], foam_bbox[3]))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.imshow("final_output", viz)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()