from socket import *
from datetime import datetime
from sftp import packet as pc
import sys

'''
Create By: Peerasit Ployaram

'''

port = 13000            # Default Port
                        # 1024 = 1KB
chunkSize = 10240       # 1MB
server_file_id = []     # For Save ID Packet Recive

def terminal(message,operation=None)-> None:
    if operation == None:
        print(datetime.now().strftime("%H:%M:%S"),": ",message)
    else: print(datetime.now().strftime("%H:%M:%S"),": ",operation, message)

def haveId(id):                             # Check Id in Server File ID
    for _ in server_file_id:
        if id == _:
            return 1
    return 0

def findIndex(id):                          # Find Id Packet in Server Buffer
    for _ in range(len(server_file)):       # and Return Index Id Packet Location
        if server_file[_].getId() == id:
            return _
    return 0

def writeFile(filename, allChunk)->None:    # Compress file
    f = open(filename,"wb")

    try:
        for chunk in allChunk:
            f.write(chunk)
        return 1
    except:
        return 0
    finally:
        f.close()

def validatePacket(validate, idTempFile):
    re_packet = []                              # Buffer ReTransmit Packet
    file = server_file[findIndex(idTempFile)]   # Find File Temp List to File Individual
    f = file.getAllRecivePacketNumber()         # Get All Packet Number Recive

    for _ in range(validate):
        if f[_] != _:
            re_packet.append(_)     
    return re_packet



if __name__ != "__main__":          # If Not Run By Main
    exit(0)


for arg in range(1,len(sys.argv)):  # Argument
    if (sys.argv[arg] == "-p" or sys.argv[arg] == "--port"): # -p, --port
        port = int(sys.argv[arg + 1])

server = socket(AF_INET,SOCK_DGRAM) # UDP
server.bind(("",port))              # Bind Port 


class tempFile():       # File for Save Information Packet 
    def __init__(self,id,totalNumberPacket):
        self.id = id
        self.chunkList = [""] * int(totalNumberPacket)
        self.numberPacketRecieve = [""] * int(totalNumberPacket)

    # Chunk
    def appendChunk(self,chunk)-> None: self.chunkList.append(chunk)
    def addChunkByLoc(self,index ,chunk)-> None: self.chunkList[index] = chunk
    def getAllChunk(self): return self.chunkList

    # Packet Number
    def appendRecivePacketNumber(self,index,numberPacket:int)->None:
        self.numberPacketRecieve[index] = numberPacket
    def getAllRecivePacketNumber(self):
        return self.numberPacketRecieve
    
    # ID
    def setId(self, id)-> None: self.id = id
    def getId(self): return self.id
        

server_file = []    # Save File Information From Client


try:
    print("Server start port:",port)
    print("Server startup from",datetime.now())
    print(f"------------------------------------")

    print(f"-------Wait for Recive Packet-------")

    while True:
        packet, clietAddress = server.recvfrom(chunkSize)

        # print("||Packet Encode: ",packet)

        header,content = packet.split(b'/',1)
        header_packet = header.decode()

        if header_packet == "[PUSH]":
            content_packet = content
        else:
            content_packet = content.decode()
            
        # print("||Header is: ",header_packet)
        # print("||Content is: ",content_packet)


        if header_packet == "[PCT]":                               # Connection package
            pct_header = header_packet              # PCT Header
            pct_content = content_packet            # PCT Sequence
            terminal(pct_header+pct_content,"GET")

            ct_packet = pc.createCTPacket(int(pct_content))     # Create CT Package
            ct = ct_packet.decode().split("/")                  # Split header and content
            terminal(ct[0]+ct[1],"PUSH")

            server.sendto(ct_packet,clietAddress)               # Sent CT Package
            print(f"-----------Client Connect-----------")

        elif header_packet == "[PUSH]":
                # print(f"\n-------Recive Packet [PUSH]-------")

            totalNumber, numberPacket, idPacket, checksum, payload = content_packet.split(b":",4)

            totalNumber = int(totalNumber.decode())
            numberPacket = int(numberPacket.decode())
            idPacket = int(idPacket.decode())
            checksum = str(checksum.decode())

            terminal(f"Packet Id[{idPacket}] Packet Number [{numberPacket}]","GET")
                # print("||Total Number Payload is: ",totalNumber)
                # print("||Packet Number: ",numberPacket)
                # print("||Id: ",idPacket)
                # print("||Checksum: ",checksum)
                # print("||Payload: ",payload)

            if not haveId(idPacket):
                server_file_id.append(idPacket)         # Add ID Packet to Server
                file = tempFile(idPacket,totalNumber)   # Create New File
                server_file.append(file)                # Append File to server
                    
            indexFile = findIndex(idPacket)
            file = server_file[indexFile]               # File Buffer for ID
            #==========
            file.addChunkByLoc(numberPacket, payload)                   # Add Chunk to File Buffer
            file.appendRecivePacketNumber(numberPacket,numberPacket)    # Add Packet Id to File Buffer
                    
        elif header_packet == "[TFC]":
            fileName, numberOfPacket, idPacket = content_packet.split(":", 3)

            fileName = str(fileName)
            numberOfPacket = int(numberOfPacket)
            idPacket = int(idPacket)

            terminal("[TFC]-> Transfer Complete.","GET")

            for file in server_file:
                if (id := file.getId()) == idPacket:                # Find File Temp
                    # print(f"file id is: {id}")
                    # print(f"file index location: {findIndex(id)}")   

                    vp = validatePacket(numberOfPacket,id)          # Validate if packet miss

                    if len(vp) > 0: # If have Miss Packet Do [RTP]
                        terminal("Found Packet File Missing","Status:")

                        rtp_packet = pc.createRTPPacket(id,vp)      # Create RTP Packet for Retransmiss
                        server.sendto(rtp_packet, clietAddress)     # Send Back to Client

                        terminal("[RTP]","PUSH")

                    elif writeFile(fileName,file.getAllChunk()):                # If has Validate Compress All Packet to File
                        terminal("All Packet Has been Validate.", "Status:")
                        terminal("Compress Packet to File", "Status:")
                        terminal("File has been Create Successfully.", "Status:")

                        indexFile = findIndex(idPacket)                     # Find Location of File in File Buffer
                        server_file.remove(server_file[indexFile])          # Remove File in File Buffer After Successful Compress 

                        server.sendto(pc.createEndPacket(), clietAddress)   # Send END Packet 
                        terminal("[END]","PUSH")

                
        elif header_packet == "[END]":
            terminal("[END]","GET")
            terminal("Server has been stop.")
            break

        else:
            print("[OPERATION ERROR]")

except:
    print("[ERROR]")
    exit(1)
