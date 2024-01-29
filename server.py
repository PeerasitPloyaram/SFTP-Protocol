from socket import *
from datetime import datetime
import sys
import os
import sftp



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
        package, clietAddress = server.recvfrom(chunkSize)

        package = package.decode().split("/")
        header_package = package[0]
        content_package = package[1]

        match header_package:
            case "[PCT]":                          # Connection package
                pct_header = header_package
                pct_content = content_package
                print("GET",pct_header,pct_content)

                ct_package = sftp.createCTPackage(int(pct_content)) # Create CT Package
                ct = ct_package.decode().split("/")                 # Split header and content
                print("PUSH",ct[0],ct[1])

                server.sendto(ct_package,clietAddress)              # Sent CT Package

            case _:
                print("[OPERATION ERROR]")


        # if packet == b'END...':
        #     terminal("[END]") # In testing
        #     f = open("Compress.png","wb")

        #     for i in range(len(buffer)):
        #         buff = buffer[i]
        #         f.write(buff)
        #     f.close
        #     buffer.clear()
        #     continue

        # terminal(package)
        # buffer.append(packet)  
except:
    print(Exception())
