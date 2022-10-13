import cv2
camera = cv2.VideoCapture(0)
# print(camera.isOpened())
ret, image = camera.read()
cv2.imwrite("foam_img.jpg", image)
camera.release()
del(camera)                                                                            