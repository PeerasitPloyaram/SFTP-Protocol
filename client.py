from socket import *
from random import randrange
import sftp
import time

server_name = 'localhost'
port = 13000
chunkSize = 4096

file = "/Users/peerasit/ku_study/network/projectProtocol/pic.png"


# Create Socket
client_socket = socket(AF_INET, SOCK_DGRAM)
core = sftp.core
core.createChunk(core,file,"png",chunk=chunkSize,verbose=False)    # Create packet to send

con_package = sftp.createPCTPackage()

client_socket.sendto(con_package,(server_name,port))
message,server = client_socket.recvfrom(4096)
print(message)
#Send
# for _ in range(core.getChunkCount(core)):          # Send packet
#     payload = core.getChunkById(core,_)

#     # print("\n",payload)

#     client_socket.sendto(payload,(server_name,port))


# message = "[END]"
# client_socket.sendto(message.encode() ,(server_name,port))
client_socket.close()

