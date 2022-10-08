import os, socket, time
from foam_detection.process_img import process_img
import cv2

# Creating socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "0.0.0.0"
PORT = 52212
machine = socket.gethostbyname(socket.gethostname())
sock.bind((HOST, PORT))
sock.listen(3)
print("HOST: ", sock.getsockname())
print(machine)

# Accepting the connection from the client
client, addr = sock.accept()

# Server recieves img from raspberry pi

file = open('transferred_files/foam_img_from_pi.jpg', "wb")
image_chunk = client.recv(2048)

while image_chunk:
    file.write(image_chunk)
    image_chunk = client.recv(2048)
file.close
print("Image Recieved From Pi")

time.sleep(2)

# Server processes img
img = cv2.imread("transferred_files/foam_img_from_pi.jpg")
viz, digestate_data = process_img(img)
cv2.imwrite("transferred_files/viz.jpg", viz)

# Server sends processed img back to pi

file = open("transferred_files/viz.jpg", "rb")
image_data = file.read(2048)
while image_data:
    client.send(image_data)
    image_data = file.read(2048)
file.close()
print("Analyzed Image Sent To Client")


client.close()