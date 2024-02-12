from socket import *
from datetime import datetime
from sftp import packet as packet
from sftp import core as core
import threading
import time
import os

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
    "PSH" : "[PUSH]",
    "RTP" : "[RTP]",

    "CT" : "[CT]",      # Contact
    "PCT" : "[PCT]",    # PreContact
    "TFC" : "[TFC]",
    "END" : "[END]",

    "ERR" : "[ERROR]"
}


def terminal(message,operation=None):
    if operation == None:
        print(datetime.now().strftime("%H:%M:%S"),": ",message)
    else: print(datetime.now().strftime("%H:%M:%S"),": ",operation, message)

# Init client
client_socket = socket(AF_INET, SOCK_DGRAM) # UDP
client_socket.settimeout(timeOut)           # Set Time Out


# Connection Phase
con_packet = packet.createPCTPacket()   # Create PCT
try:    # Connection Establishment
    c_packet = con_packet.decode().split("/")
    terminal(c_packet[0] + c_packet[1],"PUSH")
    client_socket.sendto(con_packet,(server_name,port))     # Send PCT
    message,server = client_socket.recvfrom(chunkSize)      # Wait CT Response
    message = message.decode().split("/")                   # Divide Header and Content

    if message[0] == operations["CT"]:              # Recive connection knownlagement
        connect = True                              # Connected
        connectId = message[1]                      # CT Sequence
        terminal(message[0] + message[1], "GET")

except timeout:
    terminal("Can't connect to server because server not response.", operations["ERR"])
    exit()

# Main
if connect: # If Connect to Server
    terminal("-----Client Connected To Server-----")

    # Create file chunk
    file = "/Users/peerasit/ku_study/network/projectProtocol/pic.png"
    core.createChunk(core,file,chunk=chunkSize,verbose=False)    # Create packet to send
    file_id = 14


    temp_total_payload = core.getChunkCount(core)
    for packet_number in range(10):
        buffer = core.getChunkById(core, packet_number)
        id, pk = packet.createPacket(temp_total_payload,packet_number ,file_id, 1101,buffer)    

        client_socket.sendto(pk,(server_name,port))
        # print(f"PUSH Packet ID {id} Number {packet_number}.")
        o = f"PUSH Packet Id {id} Number {packet_number}"

        terminal(o)
    ##
    client_socket.sendto(packet.createTFCPacket("png",temp_total_payload, file_id),(server_name, port))
    terminal("[TFC]","PUSH")



    # # Wait Response from Server
    # message,server = client_socket.recvfrom(4096) 
    # header,content = message.split(b'/',1)
    # header = header.decode()

    # Wait Response from Server
    while True:
        message,server = client_socket.recvfrom(chunkSize) 
        header,content = message.split(b'/',1)
        header = header.decode()

        match header:
            case "[RTP]":   # RTP Packet
                terminal("[RTP]-> Packet Missing","GET")

                content = content.decode()
                id, num = content.split(":",1)  # Split to Id and List Number Packet
                p = num.split(":")              # Split Number Packet

                for numberPacket in p:
                    # print(numberPacket)
                    numberPacket = int(numberPacket)                # Str to int
                    chunk = core.getChunkById(core, numberPacket)   # get Chunk by Id
                    id, pk = packet.createPacket(temp_total_payload,numberPacket ,file_id, 1101,chunk)  # Create Packet

                    client_socket.sendto(pk,(server_name,port))     # Resend Missing Packet to Server

                    o = f"PUSH Packet Id {id} Number {numberPacket}"
                    terminal(o)
            
                client_socket.sendto(packet.createTFCPacket("png",temp_total_payload, file_id),(server_name, port)) # Send TFC Packet to Server
                terminal("[TFC]","PUSH")

            case "[END]":   # END Packet
                terminal("[END]","GET")
                terminal("-----Client Disconnect From Server-----")
                break

            case _: # Error
                terminal("[OPERATION ERROR]")
        


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
client_socket.close()

