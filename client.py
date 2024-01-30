from socket import *
from datetime import datetime
import sftp
import threading
import time

# Config
server_name = 'localhost'
port = 13000
chunkSize = 4096
timeOut = 5

# Flags
connect = False     # Is connecting
connectId = None    # Connection ID

operations = {
    "GET" : "[GET]",
    "PUSH" : "[PUSH]",

    "CT" : "[CT]",      # Contact
    "PCT" : "[PCT]",    # PreContact

    "ERR" : "[ERROR]"
}


def terminal(message,operation=None):
    if operation == None:
        print(datetime.now().strftime("%H:%M:%S"),": ",message)
    else: print(datetime.now().strftime("%H:%M:%S"),": ",operation, message)

# Init client
client_socket = socket(AF_INET, SOCK_DGRAM) # UDP
client_socket.settimeout(timeOut)
core = sftp.core


# Connection Phase
con_package = sftp.createPCTPackage()   # Create PCT
try:    # Connection establishment
    client_socket.sendto(con_package,(server_name,port))    # Send PCT
    message,server = client_socket.recvfrom(chunkSize)      # Wait CT Response
    message = message.decode().split("/")                   # Divide Header and Content

    if message[0] == operations["CT"]:                # Recive connection knownlagement
        connect = True                    # Connected
        connectId = message[1]              # CT Sequence
        # print("GET",message[0],message[1])
        terminal(message[0] + message[1], "GET")

except timeout:
    # print("[ERROR]:","Can't connect to server because server not response.")
    terminal("Can't connect to server because server not response.", operations["ERR"])
    exit()

# Main
# Create file chunk
file = "/Users/peerasit/ku_study/network/projectProtocol/pic.png"
core.createChunk(core,file,"png",chunk=chunkSize,verbose=False)    # Create packet to send

if connect:
    terminal("Client connected to server.")
        


# while True:
#     message,server = client_socket.recvfrom(4096)
#     message = message.decode().split("/")
#     header_message = message[0]
#     content_message = message[1]

#     match header_message:
#         case "[CT]":    # Recive connection knownlagement
#             print("GET",header_message,content_message)
        
#         case "[END]":
#             break
#Send
# for _ in range(core.getChunkCount(core)):          # Send packet
#     payload = core.getChunkById(core,_)

#     # print("\n",payload)

#     client_socket.sendto(payload,(server_name,port))


# message = "[END]"
# client_socket.sendto(message.encode() ,(server_name,port))
client_socket.close()

