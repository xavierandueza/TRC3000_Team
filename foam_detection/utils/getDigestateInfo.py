from utils.getEdges import getEdges
import cv2

def getDigestateInfo(image, box, foam_bbox):
    """
    Function to get various info on the digestate sample.

    :param image: image of sample
    :param canny: canny edges of the sample
    :param box: bounding box coordinates of the flask
    :returns: a dictionary containing various information of the sample
    
    """



    canny = getEdges(image, 3)
    cv2.imshow("edges for digestate info", canny)
    x,y,w,h = box

    TRUE_FLASK_HEIGHT = 0.1421 #metres

    # print( box)
    for i in range(h):
        if canny[y+h-(i+1)][canny.shape[1]//2] == 255 and i>50:
            liquid_height = i
            break
    liquid_colour = image[y+h-(liquid_height//2)][x+(w//2)]
    if foam_bbox is None:
        foam_height = None
        foam_colour = None
        ratio_foam_to_flask = 0
    else:
        foam_height = int(abs(foam_bbox[3] - foam_bbox[1]))
        foam_colour = image[int(abs(foam_bbox[3]-foam_bbox[1])//2)+int(min(foam_bbox[1], foam_bbox[3]))][x+(w//2)]
        ratio_foam_to_flask = foam_height/h
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