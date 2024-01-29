import sftp

core = sftp.core

core.createPacket(core,"/Users/peerasit/ku_study/network/projectProtocol/pic.png",chunk=4096)
print(core.getChunkSize(core))
print(core.getPacketCount(core))




# buffer = []

# with open("/Users/peerasit/ku_study/network/projectProtocol/pic.png", 'rb') as fi:
#     while True:
#         packet = fi.read(4096)
#         buffer.append(packet)


#         if not packet:
#             buffer.pop()
#             break


    
#         with open("after.png", 'wb') as new:
#             for i in buffer:
#                 new.write(i)


#             new.close()
        