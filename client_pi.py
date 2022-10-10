import os, socket, time, struct

HOST = "192.168.246.239"
HOST = "192.168.234.172"
PORT = 52212

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#trying to connect to socket
# try:
sock.connect((HOST,PORT))


# Raspberry Pi sends over img it captures from pi-cam:
file_name = "foam_img.jpg"
file_len = os.stat(file_name).st_size
msg_header = struct.pack('<I', file_len)
sock.sendall(msg_header)
fd = open(file_name, 'rb')
data = fd.read(file_len)
while data:
    sock.sendall(data)
    data = fd.read(file_len)
fd.close()
# print("Image Sent To Host")

viz_list_str = ["viz0000", "viz0001", "viz0010", "viz0011", "viz0100", "viz0101", "viz0110", "viz0111", "viz1000", "viz1001", "viz1010", "viz1011", "viz1100", "viz1101", "viz1110", "viz1111"]
# Client recieves processed img from server
for i in range(16):
    file_name = 'transferred_files/' + viz_list_str[i] + '.jpg'
    msg_header = sock.recv(4)
    while len(msg_header) != 4:
        msg_header += sock.recv(4- len(msg_header))
    file_len = struct.unpack('<I', msg_header)[0]
    nFile = open(file_name, 'wb')
    data = sock.recv(file_len)
    while len(data) != file_len:
        data += sock.recv(file_len - len(data))
    nFile.write(data)
    nFile.close()
    # print("Image Recieved From Host")

file_name = "transferred_files/digestate_colour.jpg"
msg_header = sock.recv(4)
while len(msg_header) != 4:
    msg_header += sock.recv(4- len(msg_header))
file_len = struct.unpack('<I', msg_header)[0]
nFile = open(file_name, 'wb')
data = sock.recv(file_len)
while len(data) != file_len:
    data += sock.recv(file_len - len(data))
nFile.write(data)
nFile.close()

file_name = "transferred_files/foam_colour.jpg"
msg_header = sock.recv(4)
while len(msg_header) != 4:
    msg_header += sock.recv(4- len(msg_header))
file_len = struct.unpack('<I', msg_header)[0]
nFile = open(file_name, 'wb')
data = sock.recv(file_len)
while len(data) != file_len:
    data += sock.recv(file_len - len(data))
nFile.write(data)
nFile.close()

sock.close()