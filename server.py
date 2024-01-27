from socket import *
from datetime import datetime
import sys
import os



port = 13000 # Default Port
chunkSize = 4096

def terminal(word):
        print(datetime.now().strftime("%H:%M:%S"),": ",word)

for arg in range(1,len(sys.argv)):
    if (sys.argv[arg] == "-p" or sys.argv[arg] == "--port"):
        port = int(sys.argv[arg + 1])

    if (sys.argv[arg] == "-t" or sys.argv[arg] == "--test"):
         pass

server = socket(AF_INET,SOCK_DGRAM)
server.bind(("",port))


try:
    print("Server start port:",port)
    print("Server startup from",datetime.now())
    print("===================")
    buffer = [] # buffer for packet comming

    while True:
        packet, clietAddress = server.recvfrom(chunkSize)

        if packet == b'END...':
            terminal("[END]") # In testing
            f = open("Compress.png","wb")

            for i in range(len(buffer)):
                buff = buffer[i]
                f.write(buff)
            f.close
            buffer.clear()
            continue

        buffer.append(packet)  
except:
    print(Exception())
