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
file_name = 'transferred_files/foam_img_from_pi.png'
file_size = client.recv(1024).decode()
with open(file_name, "wb") as file:
    c = 0
    start_time = time.time()
    while c <= int(file_size):
        data = client.recv(1024)
        if not (data):
            break
        file.write(data)
        c+= len(data)
        print(c, file_size)
    end_time = time.time()
time.sleep(2)
print("Image Recieved From Pi, Time Taken: " + str(end_time-start_time))

# Server processes img
img = cv2.imread("transferred_files/foam_img_from_pi.png")
viz, digestate_data = process_img(img)
cv2.imwrite("transferred_files/viz.png", viz)

# Server sends processed img back to pi

file_name = "transferred_files/viz.png"
file_size = os.path.getsize(file_name)
client.send(str(file_size).encode())
with open(file_name, "rb") as file:
    c = 0
    start_time = time.time()
    while c <= file_size:
        data = file.read(1024)
        if not (data):
            break
        client.sendall(data)
        c+= len(data)
    end_time = time.time()
time.sleep(2)
print("Analyzed Image Sent To Client, Time Taken: " + str(end_time-start_time))


client.close()