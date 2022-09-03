import cv2
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

# Choose image
original = cv2.imread("foam_detection/images/fg2.jpg")
duplicate = cv2.imread("foam_detection/images/background/bg2.jpg")

scale = 768/max(original.shape[0],original.shape[1])
original = rescaleFrame(original, scale)
duplicate = rescaleFrame(duplicate, scale)


# Store the image shape into variable
ori_shape = original.shape[:2]
dup_shape = duplicate.shape[:2]

# TEST 1: Based on shape of image
if ori_shape == dup_shape:
    print("Image size is same")
else:
    print("Image is different in size")

# TEST 1: Based on shape of image
if ori_shape == dup_shape:
    print("Image size is same")

    # Extract the difference of color element between two image
    difference = cv2.subtract(original, duplicate)
    b, g, r = cv2.split(difference)


# TEST 1: Based on shape of image
if ori_shape == dup_shape:
    # ...

    # TEST 2: Based on color of image
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("The color is equal")
    else:
        print('The color of image is different')
        cv2.imshow('Difference', difference)

cv2.waitKey(0)
cv2.destroyAllWindows(0)