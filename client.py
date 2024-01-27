from socket import *
import ftp

server_name = 'localhost'
port = 13000
chunkSize = 4096

file = "/Users/peerasit/ku_study/network/projectProtocol/pic.png"



client_socket = socket(AF_INET, SOCK_DGRAM)
core = ftp.core
core.createChunk(core,file,"png",chunk=chunkSize,verbose=False)    # Create packet to send


#Send
for _ in range(core.getChunkCount(core)):          # Send packet
    payload = core.getChunkById(core,_)

    # print("\n",payload)

    client_socket.sendto(payload,(server_name,port))


message = "END..."

client_socket.sendto(message.encode() ,(server_name,port))
client_socket.close()

