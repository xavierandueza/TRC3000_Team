
import numpy as np
import sys
sys.path.append("foam_detection/")
sys.path.append("foam_detection/detectron2-main/")
sys.path.append("detectron2-main/")
sys.path.append("foam_detection/rembg-main/")
from utils.rescaleFrame import rescaleFrame
from utils.getEdges import getEdges
from utils.getDigestateInfo import getDigestateInfo
from utils.toBinary import toBinary
from utils.getBoundingBox import getBoundingBox
from utils.removeGlare import removeGlare
from utils.getFoamFromModel import getFoamFromModel
from utils.colourBlockDetection import colourBlockDetection
import rembg
import cv2


def process_img(image=None):
    # image = cv2.imread("foam_detection/images/clear.jpg")
    # image = cv2.imread("foam_detection/images/fg1.jpg")
    if image is None:
        image = cv2.imread("foam_detection/foaming_images/test2.jpg")
    # image = cv2.imread("foam_detection/foaming_images/Yellowx3_foamx5.jpg")
    scale = 720/max(image.shape[0],image.shape[1])
    image = rescaleFrame(image, scale)
    # cv2.imshow("original_image", image)

    #########################################################################################################
    # Removing the backgorund using AI method from rembg package
    flask_img = rembg.remove(image)
    flask_img = cv2.cvtColor(flask_img, cv2.COLOR_BGRA2BGR)
    # # Optional: Remove Glare
    # flask_img = removeGlare(flask_img, 210)
    # cv2.imshow("removed_background", flask_img)
    # foam - foam height - digestate - digestate height
    
    viz0000 = flask_img.copy()
    viz0001 = flask_img.copy()
    viz0010 = flask_img.copy()
    viz0011 = flask_img.copy()
    viz0100 = flask_img.copy()
    viz0101 = flask_img.copy()
    viz0110 = flask_img.copy()
    viz0111 = flask_img.copy()
    viz1000 = flask_img.copy()
    viz1001 = flask_img.copy()
    viz1010 = flask_img.copy()
    viz1011 = flask_img.copy()
    viz1100 = flask_img.copy()
    viz1101 = flask_img.copy()
    viz1110 = flask_img.copy()
    viz1111 = flask_img.copy()
    viz_list = [viz0000, viz0001, viz0010, viz0011, viz0100, viz0101, viz0110, viz0111, viz1000, viz1001, viz1010, viz1011, viz1100, viz1101, viz1110, viz1111]
    viz_list_str = ["viz0000", "viz0001", "viz0010", "viz0011", "viz0100", "viz0101", "viz0110", "viz0111", "viz1000", "viz1001", "viz1010", "viz1011", "viz1100", "viz1101", "viz1110", "viz1111"]
    #########################################################################################################
    # Get the bounding box of the flask
    box = getBoundingBox(flask_img)
    x, y, w, h = box

    #########################################################################################################   
    # Get bounding box of the foam using trained mask rcnn model
    no_foam = False
    n = 0
    for i in range(len(viz_list)):
        if viz_list_str[i][-4] == "1":
            if n == 0:
                n+=1
                foam_bbox, viz_list[i] = getFoamFromModel(viz_list[i])
                foam_viz = viz_list[i].copy()
            else:
                viz_list[i] = foam_viz.copy()
    if foam_bbox == None:
        no_foam = True
    else:
        foam_edge = round(max(foam_bbox[3], foam_bbox[1]))


    #########################################################################################################
    # Extract important digestate info from image and canny edges
    digestate_info = getDigestateInfo(flask_img, box, foam_bbox, no_foam)
    liquid_colour = digestate_info["digestate colour"]
    liquid_height = digestate_info["digestate height"]
    true_liquid_height = digestate_info["real digestate height"]
    if not no_foam:
        foam_height = digestate_info["foam height"]
        foam_colour = digestate_info["foam colour"]
        true_foam_height = digestate_info["real foam height"]

    #########################################################################################################
    # Get bounding box of colours
    for i in range(len(viz_list)):
        if viz_list_str[i][-2] == "1":
            viz_list[i] = colourBlockDetection(flask_img, viz_list[i], liquid_colour)

    #########################################################################################################

    # Displaying the detected colour
    colour = np.zeros((100,100,3), dtype = "uint8")
    for i in range(100):
        for j in range(100):
            colour[i][j] = liquid_colour
    # cv2.imshow("colour_of_liquid", colour)

    # Displaying the detected foam colour
    if not no_foam:
        colour_foam = np.zeros((100,100,3), dtype = "uint8")
        for i in range(100):
            for j in range(100):
                colour_foam[i][j] = foam_colour
        # cv2.imshow("colour_of_foam", colour_foam)

    #########################################################################################################
    # Displaying height lines
    if no_foam:
        for i in range(len(viz_list)):
            if viz_list_str[i][-1] == "1":
                # Displaying the detected digestate/liquid height
                cv2.line(viz_list[i], (x+(w//2), y+h-(liquid_height)), (x+(w//2),y+h), (0, 0, 255), 2)
                string = "digestate height: " + str(round(true_liquid_height*1000,2))  +  " mm"
                cv2.putText(viz_list[i],string, (x,y+h-(liquid_height+10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                # print(string)
    else:
        for i in range(len(viz_list)):
            if viz_list_str[i][-1] == "1":
                # Displaying the detected digestate/liquid height
                cv2.line(viz_list[i], (x+(w//2), foam_edge), (x+(w//2),foam_edge+(liquid_height)), (0, 0, 255), 2)
                string = "digestate height: " + str(round(true_liquid_height*1000,2))  + " mm"
                cv2.putText(viz_list[i],string, (x, min(foam_edge+(liquid_height+25), viz_list[i].shape[0]-50)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                # print(string)
        for i in range(len(viz_list)):
            if viz_list_str[i][-3] == "1":
                # Displaying the detected foam height
                cv2.line(viz_list[i], (x+(w//2), round(foam_bbox[1])), (x+(w//2), round(foam_bbox[3])), (0, 255, 0), 2)
                string = "foam height: " + str(round(true_foam_height*1000,2))  + " mm"
                cv2.putText(viz_list[i],string, (x, max(round(min(foam_bbox[1], foam_bbox[3]) -25), 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                # print(string)
            # cv2.imshow("final_output", viz)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return viz_list, viz_list_str, colour, colour_foam, digestate_info

if __name__ == "__main__":
    process_img()