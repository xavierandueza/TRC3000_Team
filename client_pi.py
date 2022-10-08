import os, socket, time

HOST = "192.168.246.239"
HOST = "192.168.234.172"
PORT = 52215

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#trying to connect to socket
# try:
sock.connect((HOST,PORT))


# Raspberry Pi sends over img it captures from pi-cam:
file_name = "foam_img.jpg"
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
print("Image Sent To Host, Time Taken: " + str(end_time-start_time))

# Client recieves processed img from server
file_name = 'transferred_files/viz.jpg', "wb"
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
print("Image Recieved From Host, Time Taken: " + str(end_time-start_time))

sock.close()