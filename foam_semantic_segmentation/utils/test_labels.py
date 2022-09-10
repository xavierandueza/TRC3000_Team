# import cv2

# img = cv2.imread("train_images/0resized_1test.jpg")
# print(img.shape)
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         print(img[i][j])


# cv2.imshow("",img)
# pxl = [0] * 256
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         pxl[img[i][j]] += 1
# print(pxl)

# colours = []
# for i in range(len(pxl)):
#     if pxl[i]!= 0 and i not in colours:
#         colours.append(i)
# print(colours)

# # import os
# # out_label_filepath = "train_labels"

# # for imgf in os.listdir(out_label_filepath):
# #     if imgf.endswith('.jpg'):
# #         os.remove(out_label_filepath + '/' + imgf)


# cv2.waitKey(0)
import torch
import gc

gc.collect()

torch.cuda.empty_cache()