import os, socket, time

HOST = "192.168.246.239"
HOST = "192.168.234.172"
PORT = 52214

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#trying to connect to socket
# try:
sock.connect((HOST,PORT))


# Raspberry Pi sends over img it captures from pi-cam:
file_name = "Bluex3_foamx3.jpg"

# Send the file details to the client.
file = open(file_name, "rb")
image_data = file.read(2048)
while image_data:
    sock.send(image_data)
    image_data = file.read(2048)
file.close()
print("Image Sent To Host")



# Client recieves processed img from server
file = open('transferred_files/viz.jpg', "wb")
image_chunk = sock.recv(2048)

while image_chunk:
    file.write(image_chunk)
    image_chunk = sock.recv(2048)
file.close
print("Image Recieved From Pi")

sock.close()