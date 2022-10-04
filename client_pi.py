import os, socket, time

HOST = "192.168.246.239"
PORT = 52223

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#trying to connect to socket
# try:
sock.connect((HOST,PORT))
#     print("Connected Successfully")
# except:
#     print("Unable to Connect")
#     exit(0)


# Raspberry Pi sends over img it captures from pi-cam:
file_name = "img_from_picam.jpg"
file_size = os.path.getsize(file_name)

# Send the file details to the client.
sock.send(file_name.encode('utf-8'))
# client.send(str(file_size).encode('utf-8'))

# Open and read the file.
with open(file_name, "rb") as file:
    start_time = time.time()
    while True:
        data = file.read(1024)
        if not (data):
            break
        sock.send(data)
    end_time = time.time()
file.close()
print("Transfer Complete, Time Taken: " + str(end_time-start_time))



# Client recieves processed img from server
file_name = sock.recv(100).decode()
print(file_name)

# Open and write file
with open("transferred_files/" + file_name, "wb") as f:    
    start_time = time.time()

    while True:
        data = sock.recv(1024)
        # print(data)
        if not data:
            break
        f.write(data)
        
    end_time = time.time()
f.close()
print("Transfer Complete, Time Taken: " + str(end_time-start_time))


sock.close()