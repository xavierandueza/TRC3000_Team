def getDigestateInfo(image, canny, box):
    """
    Function to get various info on the digestate sample.

    :param image: image of sample
    :param canny: canny edges of the sample
    :param box: bounding box coordinates of the flask
    :returns: a dictionary containing various information of the sample
    
    """

    x,y,w,h = box
    getting_liquid = True
    for i in range(h):
        if canny[y+h-(i+1)][canny.shape[1]//2] == 255 and i>50:
            if getting_liquid:
                liquid_height = i
                getting_liquid = False
            else:
                foam_height = i
                break

    liquid_colour = image[y+h-(liquid_height//2)][x+(w//2)]

    digestate_info = {
        "digestate height": liquid_height,
        "digestate colour": liquid_colour,
        "foam height": foam_height,
        "foam colour": None
    }

    return digestate_info