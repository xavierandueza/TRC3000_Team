import cv2
import numpy as np
import os

bg_filepath = "backgrounds"
img_filepath = "images"
label_filepath = "labels"

out_images_filepath = "train_images"
out_label_filepath = "train_labels"
# out_images_filepath = "valid_images"
# out_label_filepath = "valid_labels"

number_of_images_per_backround = 10

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


for imgf in os.listdir(img_filepath):
    if imgf.endswith('.jpg') or imgf.endswith('.png') or imgf.endswith('.JPG'):
        img_ = cv2.imread(img_filepath + '/' + imgf)
        label_ = cv2.imread(label_filepath + '/' + imgf[0:-4] + ".png")

        for bg in os.listdir(bg_filepath):
            if bg.endswith('.jpg') or bg.endswith('.png') or bg.endswith('.JPG'):
                for k in range(number_of_images_per_backround):
                    background = cv2.imread(bg_filepath + '/' + bg)
                    # Resize images/labels
                    rescale_size = np.random.randint(150, min(background.shape[0],background.shape[1])/1.25)
                    scale = rescale_size/max(img_.shape[0],img_.shape[1])
                    img = rescaleFrame(img_, scale)
                    label = rescaleFrame(label_, scale)


                    new_label = np.zeros(background.shape, dtype = "uint8")
                    start_i = np.random.randint(0, background.shape[0]-img.shape[0])
                    start_j = np.random.randint(0, background.shape[1]-img.shape[1])
                    for i in range(img.shape[0]):
                        for j in range(img.shape[1]):
                            if sum(img[i][j])!= 0:
                                background[start_i+i][start_j+j] = img[i][j]
                                if sum(label[i][j]) != 0:
                                    new_label[start_i+i][start_j+j] = (0,0,128)
                    
                    cv2.imwrite(out_images_filepath + '/'+ str(k) + bg[0:-4] + imgf, background)
                    cv2.imwrite(out_label_filepath + '/'+ str(k) + bg[0:-4] + imgf[0:-4] + ".png", new_label)
