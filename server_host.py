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
file_name = client.recv(1024).decode()
print(file_name)

# Open and write file
with open("transferred_files/" + file_name, "wb") as f:    
    start_time = time.time()

    while True:
        data = client.recv(1024)
        if not data:
            print("breaking")
            break
        f.write(data)
    end_time = time.time()
f.close()
print("Transfer Complete, Time Taken: " + str(end_time-start_time))

time.sleep(2)

# Server processes img
img = cv2.imread("transferred_files/" + file_name)
viz, digestate_data = process_img(img)
cv2.imwrite("transferred_files/viz.png", viz)

# Server sends processed img back to pi
file_name = "transferred_files/viz.png"
file_size = os.path.getsize(file_name)

# Send the file details to the client.
client.send(file_name.encode('utf-8'))
# client.send(str(file_size).encode('utf-8'))

# Open and read the file.
with open(file_name, "rb") as file:
    start_time = time.time()
    while True:
        data = file.read(1024)
        if not (data):
            break
        client.send(data)
    end_time = time.time()
file.close()
print("Transfer Complete, Time Taken: " + str(end_time-start_time))


client.close()