from socket import *
from datetime import datetime
from sftp import packet as packet
from sftp import core as core
import sys
import re

# Config
server_name = 'localhost'
port = 13000        # Port Default
chunkSize = 4096    # 4Kb Default
timeOut = 5         # Time out

# Flags
connect = False     # Is connecting
connectId = None    # Connection ID
argv_test = 0

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
client_socket = socket(AF_INET, SOCK_DGRAM) # UDP Transport
client_socket.settimeout(timeOut)           # Set Time Out

list_file_name = [] # Handle Multiple File for Transfer

for arg in range(1,len(sys.argv)):  # Argument

    if ((sys.argv[arg] == "-p" or sys.argv[arg] == "--port") and (re.match("[0-9]+",sys.argv[arg + 1]))):   # -p, --port
        try:
            port = int(sys.argv[arg + 1])
        except:
            print(f"[ERROR] Port Argument Require Integer not String.")
            exit(1)

    elif (sys.argv[arg] == "-t" or sys.argv[arg] == "--test"):  # -t, --test
        argv_test = 1

    elif re.match("[/a-zA-Z]",sys.argv[arg]):   # Path File Name
        file_name = sys.argv[arg]
        list_file_name.append(file_name)


if len(list_file_name) == 0 and argv_test:              # If Have Only -t, --test
    con_packet = packet.createPCTPacket()               # Create PCT
    try:                                                # Connection Establishment
        terminal(f"-----Try to Connect to Server-----")
        c_packet = con_packet.decode().split("/")
        terminal(c_packet[0] + c_packet[1],"PUSH")
        client_socket.sendto(con_packet,(server_name,port))     # Send PCT
        message,server = client_socket.recvfrom(chunkSize)      # Wait CT Response
        message = message.decode().split("/")                   # Divide Header and Content

        if message[0] == operations["CT"]:              # Recive connection knownlagement
            connect = True                              # Connected
            connectId = message[1]                      # CT Sequence
            terminal(message[0] + message[1], "GET")
            if connect :
                exit(0)
        
    except timeout:     # Time Out
        terminal("Can't connect to server because server not response.", operations["ERR"])
        exit(1)
    exit(1)

elif len(list_file_name) == 1 and argv_test:                # IF Have Path File Name With Argument -t, --test
    print("[ERROR] Can't Use File With Argument --test.")
    exit(1)


# Connection Phase
con_packet = packet.createPCTPacket()   # Create PCT
try:    # Connection Establishment
    terminal(f"-----Try to Connect to Server-----")
    c_packet = con_packet.decode().split("/")
    terminal(c_packet[0] + c_packet[1],"PUSH")
    client_socket.sendto(con_packet,(server_name,port))     # Send PCT
    message,server = client_socket.recvfrom(chunkSize)      # Wait CT Response
    message = message.decode().split("/")                   # Divide Header and Content

    if message[0] == operations["CT"]:              # Recive connection knownlagement
        connect = True                              # Connected
        connectId = message[1]                      # CT Sequence
        terminal(message[0] + message[1], "GET")

except timeout:     # Time Out
    terminal("Can't connect to server because server not response.", operations["ERR"])
    exit(1)

# Main Phase
if connect: # If Connect to Server
    terminal("-----Client Connected To Server-----")

    for file_name in list_file_name:    # Loop File Transfer

        # Create file chunk
        file = file_name                                                # Path File Name
        path_file = file_name.split("/")                                # Path File
        file_id = packet.genPacketId()                                  # Gen File ID Packet
        core.createChunk(core,file,chunk=chunkSize,verbose=False)       # Create Chunk of File


        temp_total_payload = core.getChunkCount(core)           # Get All Chunk of File
        for packet_number in range(temp_total_payload):
            buffer = core.getChunkById(core, packet_number)     # Create Payload
            id, pk = packet.createPacket(temp_total_payload,packet_number ,file_id, 1101,buffer)    # Create Packet and Return IDPacket, Packet

            client_socket.sendto(pk,(server_name,port))         # Send to Server
            o = f"PUSH Packet Id {id} Number {packet_number}"

            terminal(o)
        ##
        client_socket.sendto(packet.createTFCPacket(path_file[len(path_file) - 1],temp_total_payload, file_id),(server_name, port)) # Send TFC Packet to Server
        terminal("[TFC]","PUSH")

        # Wait Response from Server
        while True:
            message,server = client_socket.recvfrom(chunkSize) 
            header,content = message.split(b'/',1)
            header = header.decode()

            match header:
                case "[RTP]":   # RTP Packet
                    terminal("[RTP]<- Packet Missing","GET")

                    content = content.decode()
                    id, num = content.split(":",1)  # Split to Id and List Number Packet
                    p = num.split(":")              # Split Number Packet

                    for numberPacket in p:
                        numberPacket = int(numberPacket)                # Str to int
                        chunk = core.getChunkById(core, numberPacket)   # get Chunk by Id
                        id, pk = packet.createPacket(temp_total_payload,numberPacket ,file_id, 1101,chunk)  # Create Packet

                        client_socket.sendto(pk,(server_name,port))     # Resend Missing Packet to Server

                        o = f"PUSH Packet Id {id} Number {numberPacket}"
                        terminal(o)
            
                    client_socket.sendto(packet.createTFCPacket(path_file[len(path_file) - 1],temp_total_payload, file_id),(server_name, port)) # Send TFC Packet to Server
                    terminal("[TFC]","PUSH")

                case "[END]":   # END Packet
                    terminal("[END]","GET")
                    break

                case _: # Error
                    terminal("[OPERATION ERROR]")
    terminal("-----Client Disconnect From Server-----")
    client_socket.close()   # Close Connection

