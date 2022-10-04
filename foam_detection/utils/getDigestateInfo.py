from utils.getEdges import getEdges
import cv2

def getDigestateInfo(image, box, foam_bbox, no_foam):
    """
    Function to get various info on the digestate sample.

    :param image: image of sample
    :param box: bounding box coordinates of the flask
    :param foam_bbox: bounding box of foam given in coordinates of top left and bottom right corners
    :param no_foam: Boolean of whether there is foam or not
    :returns: a dictionary containing various information of the sample
    
    """

    canny = getEdges(image, 5)
    # cv2.imshow("edges for digestate info", canny)
    x,y,w,h = box

    TRUE_FLASK_HEIGHT = 0.1421 #metres



    # print( box)

    
    if no_foam:
        foam_height = None
        foam_colour = None
        ratio_foam_to_flask = 0

        # get liquid height
        for i in range(h):
            if canny[y+h-(i+1)][canny.shape[1]//2] == 255 and i>50:
                liquid_height = i
                break
        liquid_colour = image[y+h-(liquid_height//2)][x+(w//2)]
    else:
        foam_height = round(abs(foam_bbox[3] - foam_bbox[1]))
        foam_colour = image[round(abs(foam_bbox[3]-foam_bbox[1])//2)+round(min(foam_bbox[1], foam_bbox[3]))][x+(w//2)]
        ratio_foam_to_flask = foam_height/h
        
        # get liquid height
        foam_edge = round(max(foam_bbox[3], foam_bbox[1]))
        for i in range(h):
            if canny[foam_edge+(i+1)][canny.shape[1]//2] == 255 and i>50:
                liquid_height = i
                break
        liquid_colour = image[foam_edge+(liquid_height//2)][x+(w//2)]

    ratio_liquid_to_flask = liquid_height/h

    
    digestate_info = {
        "digestate height": liquid_height,
        "digestate colour": liquid_colour,
        "foam height": foam_height,
        "foam colour": foam_colour,
        "real foam height": ratio_foam_to_flask*TRUE_FLASK_HEIGHT,
        "real digestate height": ratio_liquid_to_flask*TRUE_FLASK_HEIGHT
    }



    return digestate_info