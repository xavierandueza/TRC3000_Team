import os, socket, time
from foam_detection.process_img import process_img
import cv2
import struct

# Creating socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "0.0.0.0"
PORT = 52212
machine = socket.gethostbyname(socket.gethostname())
sock.bind((HOST, PORT))
sock.listen(3)
print("HOST: ", sock.getsockname())
print("Server is Listening...")

# Accepting the connection from the client
client, addr = sock.accept()

# Server recieves img from raspberry pi

# Client recieves processed img from server
file_name = 'transferred_files/foam_img_from_pi.jpg'
msg_header = client.recv(4)
while len(msg_header) != 4:
    msg_header += client.recv(4- len(msg_header))
file_len = struct.unpack('<I', msg_header)[0]
nFile = open(file_name, 'wb')
data = client.recv(file_len)
while len(data) != file_len:
    data += client.recv(file_len - len(data))
nFile.write(data)
nFile.close()
print("Image Recieved From Pi")

# Server processes img
img = cv2.imread("transferred_files/foam_img_from_pi.jpg")
viz, digestate_data = process_img(img)
cv2.imwrite("transferred_files/viz.jpg", viz)

# Server sends processed img back to pi

file_name = "transferred_files/viz.jpg"
file_len = os.stat(file_name).st_size
msg_header = struct.pack('<I', file_len)
client.sendall(msg_header)
fd = open(file_name, 'rb')
data = fd.read(file_len)
while data:
    client.sendall(data)
    data = fd.read(file_len)
fd.close()
print("Analyzed Image Sent To Client")


client.close()