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

# Client recieves processed img from server
file_name = 'transferred_files/foam_img_from_pi.jpg'
file_size = sock.recv(100).decode()
with open(file_name, "wb") as file:
    c = 0
    start_time = time.time()
    while c <= int(file_size):
        data = sock.recv(1024)
        if not (data):
            break
        file.write(data)
        c+= len(data)
    end_time = time.time()
print("Image Recieved From Pi, Time Taken: " + str(end_time-start_time))

# Server processes img
img = cv2.imread("transferred_files/foam_img_from_pi.jpg")
viz, digestate_data = process_img(img)
cv2.imwrite("transferred_files/viz.jpg", viz)

# Server sends processed img back to pi

file_name = "transferred_files/viz.jpg"
file_size = os.path.getsize(file_name)
sock.send(str(file_size).encode())
with open(file_name, "rb") as file:
    c = 0
    start_time = time.time()
    while c <= file_size:
        data = file.read(1024)
        if not (data):
            break
        sock.sendall(data)
        c+= len(data)
    end_time = time.time()
print("Analyzed Image Sent To Client, Time Taken: " + str(end_time-start_time))


client.close()