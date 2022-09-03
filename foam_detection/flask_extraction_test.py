import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation

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



img_b = cv2.imread('images/background/bg1.jpg')
scale = 768/max(img_b.shape[0],img_b.shape[1])
img_b = rescaleFrame(img_b, scale)

img = cv2.imread('images/fg1.jpg')
scale = 768/max(img.shape[0],img.shape[1])
img = rescaleFrame(img, scale)

segmentor = SelfiSegmentation()
out = segmentor.removeBG(img_b, (0,0,255), threshold=0.6)
cv2.imshow("extraction", out)
cv2.waitKey(0)
cv2.destroyAllWindows()

