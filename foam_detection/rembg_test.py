import rembg
import cv2
import numpy as np
from utils.rescaleFrame import rescaleFrame
from utils.getEdges import getEdges
from utils.getDigestateInfo import getDigestateInfo
from utils.toBinary import toBinary

image = cv2.imread("foam_detection/images/test3.jpg")
# image = cv2.imread("foam_detection/images/fg1.jpg")
scale = 768/max(image.shape[0],image.shape[1])
image = rescaleFrame(image, scale)

output = rembg.remove(image)
output = cv2.cvtColor(output, cv2.COLOR_BGRA2BGR)
cv2.imshow("out", output)

binary = toBinary(output)
cv2.imshow("binary", binary)
canny = getEdges(binary, 1)
cv2.imshow("canny", canny)

contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
best_contour = contours[0]
box = cv2.boundingRect(best_contour)
x, y, w, h = box

canny = getEdges(output, 3)
cv2.imshow("canny", canny)

digestate_info = getDigestateInfo(output, canny, box)
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
cv2.line(output, (x+(w//2), y+h-(liquid_height)), (x+(w//2),y+h), (0, 0, 255), 2)
string = "height in pixels: " + str(liquid_height)
cv2.putText(output,string, (x+(w//2)+3,y+h-(liquid_height//2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
cv2.imshow("masked", output)

print(foam_height)

cv2.waitKey(0)
cv2.destroyAllWindows()