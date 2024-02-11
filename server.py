from socket import *
from datetime import datetime
from sftp import packet as pc
import sys
import os



port = 13000            # Default Port
                        # 1024 = 1KB
chunkSize = 10240       # 1MB
server_file_id = []     # For Save ID Packet Recive

def terminal(message,operation=None)-> None:
    if operation == None:
        print(datetime.now().strftime("%H:%M:%S"),": ",message)
    else: print(datetime.now().strftime("%H:%M:%S"),": ",operation, message)


def debugPacket(content:bytearray,)-> None:
        totalNumber, numberPacket, id, checksum, payload = content.split(":",4)
        print(f"========================Recive Packet [PUSH]======================")
        print("||Total Number Payload is: ",totalNumber)
        print("||Packet Number: ",numberPacket)
        print("||Id: ",id)
        print("||Checksum: ",checksum)
        # print("||Payload: ",payload)

def haveId(id):                 # Check Id in Server File ID
    for _ in server_file_id:
        if id == _:
            return 1
    return 0

def findIndex(id):
    for _ in range(len(server_file)):
        if server_file[_].getId() == id:
            return _
    return 0

if __name__ != "__main__":
    exit



for arg in range(1,len(sys.argv)):  # Argument
    if (sys.argv[arg] == "-p" or sys.argv[arg] == "--port"):
        port = int(sys.argv[arg + 1])

    if (sys.argv[arg] == "-t" or sys.argv[arg] == "--test"):
         pass

server = socket(AF_INET,SOCK_DGRAM)
server.bind(("",port))


class tempFile():
    def __init__(self,id,totalNumberPacket,numberPayload=None):
        self.id = id
        self.chunkList = [""] * int(totalNumberPacket)

        self.numberPayload = None
        self.numChunk = None

    def appendChunk(self,chunk)-> None: self.chunkList.append(chunk)
    def addChunkByLoc(self,index ,chunk)-> None:
        self.chunkList[index] = chunk
    def getAllChunk(self): return self.chunkList

    def setId(self, id)-> None: self.id = id
    def getId(self): return self.id
        

server_file = []    # Save File Comming


try:
    print("Server start port:",port)
    print("Server startup from",datetime.now())
    print("===================")


    while True:
        packet, clietAddress = server.recvfrom(chunkSize)

        # print("||Packet Encode: ",packet)
        packet = packet.decode(errors="ignore")
        # print("||Packet Decode: ",packet)

        ea = packet.split("/",1)

        header_packet = ea[0]
        content_packet = ea[1]

        # print("||Header is: ",header_packet)
        # print("||Content is: ",content_packet)


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
                print(f"=============Recive Packet [PUSH]===============")

                totalNumber, numberPacket, idPacket, checksum, payload = content_packet.split(":",4)
                numberPacket = int(numberPacket)
                # print("||Total Number Payload is: ",totalNumber)
                print("||Packet Number: ",numberPacket)
                print("||Id: ",idPacket)
                # print("||Checksum: ",checksum)
                # print("||Payload: ",payload)

                if not haveId(idPacket):
                    server_file_id.append(idPacket)         # Add ID Packet to Server
                    file = tempFile(idPacket,totalNumber)   # Create New File
                    server_file.append(file)                # Append File to server
                    
                indexFile = findIndex(idPacket)
                file = server_file[indexFile]               # File Buffer for ID
                #==========
                file.addChunkByLoc(numberPacket, payload)   # Add Chunk to File Buffer
                    

                
            case "[TFC]":
                lengthPacket, numberOfPacket, idPacket = content_packet.split(":", 3)

                lengthPacket = int(lengthPacket)
                numberOfPacket = int(numberOfPacket)
                idPacket = int(idPacket)

                print("TFC Packet: ",lengthPacket, numberOfPacket, idPacket)


                for file in server_file:
                    id = file.getId()
                    print(f"file id is: {id}")
                    print(f"file index location: {findIndex(id)}")
                    # for i in file.getAllChunk():
                    #     print(f"||{i}||")


                
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
