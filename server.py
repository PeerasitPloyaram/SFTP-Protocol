from socket import *
from datetime import datetime
from sftp import packet as pc
import sys
import os



port = 13000        # Default Port

# 1024 = 1KB
chunkSize = 10240   # 1MB

def terminal(message,operation=None):
    if operation == None:
        print(datetime.now().strftime("%H:%M:%S"),": ",message)
    else: print(datetime.now().strftime("%H:%M:%S"),": ",operation, message)


if __name__ != "__main__":
    exit



for arg in range(1,len(sys.argv)):  # Argument
    if (sys.argv[arg] == "-p" or sys.argv[arg] == "--port"):
        port = int(sys.argv[arg + 1])

    if (sys.argv[arg] == "-t" or sys.argv[arg] == "--test"):
         pass

server = socket(AF_INET,SOCK_DGRAM)
server.bind(("",port))


class fileBuffer:
    def __init__(self,numberPayload):
        self.numberPayload = numberPayload
        self.chunkList = []
        self.numChunk = 0

    def appendChunk(self,chunk): self.chunkList.append(chunk)
        


try:
    print("Server start port:",port)
    print("Server startup from",datetime.now())
    print("===================")

    buffer = [] # buffer for packet comming

    while True:
        packet, clietAddress = server.recvfrom(chunkSize)

        print("||Packet Encode: ",packet)
        packet = packet.decode(errors="ignore")
        print("||Packet Decode: ",packet)

        ea = packet.split("/",1)

        header_packet = ea[0]
        content_packet = ea[1]

        print("||Header is: ",header_packet)
        print("||Content is: ",content_packet)


        match header_packet:
            case "[PCT]":                          # Connection package
                pct_header = header_packet
                pct_content = content_packet
                terminal(pct_header+pct_content,"GET")

                ct_packet = pc.createCTPacket(int(pct_content)) # Create CT Package
                ct = ct_packet.decode().split("/")                 # Split header and content
                terminal(ct[0]+ct[1],"PUSH")

                server.sendto(ct_packet,clietAddress)              # Sent CT Package

            case "[PUSH]":
                print(f"========================Recive Packet [PUSH]======================")
                print("||Header is: ",header_packet)
                print("||Content is: ",content_packet)

                # full_payload = content_packet.split(":",4)
                totalNumber, numberPacket, id, checksum, payload = content_packet.split(":",4)

                print("||Total Number Payload is: ",totalNumber)
                print("||Packet Number: ",numberPacket)
                print("||Id: ",id)
                print("||Checksum: ",checksum)
                print("||Payload: ",payload)
                

            case "[END]":
                terminal("[END]","GET")
                terminal("Server has been stop.")
                break

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
