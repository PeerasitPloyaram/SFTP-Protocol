import sys
import time
from random import randrange
from socket import *

# Random number from 0 - 98
# Retrive number in range 1 - 99
def randomSequence()-> str:return str(randrange(0,98))

class operations:

    pct = "[PCT]"       # PreContact
    ct = "[CT]"         # Contact

    get = "[GET]"       # GET
    push = "[PUSH]"     # PUSH

    end = "[END]"       # END
    tfc = "[TFC]"       # Transfer Complete
    err = "[ERROR]"     # Error

class packet:
    # Create PCT Packet
    def createPCTPacket()-> bytearray:
        operation = operations.pct                      # [PCT]
        sequence = randomSequence().encode()
        return operation.encode() +b"/"+sequence        # [PCT]/Sequence

    # Create CT Packet
    def createCTPacket(sequence)-> bytearray:
        operation = operations.ct                       # [CT]
        sequence_ack = str(sequence + 1).encode()
        return operation.encode() +b"/"+sequence_ack    #[CT]/Sequence + 1

    # Create END Packet
    def createEndPacket()-> bytearray:
        operation = operations.end                      # [END]
        return operation.encode() + b"/"                # [END]/

    # Create File Packet
    def createPacket(totalNumberPayload,packetNumber,id,checksum ,payload)-> bytearray:
        operation = operations.push                     # [PUSH]
        return id, operation.encode() + b"/" + str(totalNumberPayload).encode() + b":" + str(packetNumber).encode() + b":" + str(id).encode() + b":" + str(checksum).encode()+ b":" + payload
        # ID Packet
        # [PUSH]/totalNumberPayload:packetNumber:id:checksum:payload
    
    def createTFCPacket(lengthPacket, totalNumberPayload, id)-> bytearray:
        operation = operations.tfc                      # [TFC]
        return operation.encode() + b"/" + str(lengthPacket).encode() + b":" + str(totalNumberPayload).encode() + b":" + str(id).encode()



class core:
    def __init__(self):
        self.chunkSize = 1024   # Default 1KB
        self.Status = None      # Status
        self.operation = None

    def createChunk(self, file, chunk,verbose=False):  # Create Chunk of file
        self.chunkList = []    # Chunk buffer

        if chunk >= 1:
            self.chunkSize = chunk
        else:
            return 1
        
        with open(file,"rb") as fi:             # Split file to packet
            while True:
                packet = fi.read(chunk)         # Read chunk
                self.chunkList.append(packet)   # Push to buffer

                if not packet:                  # If last chunk
                    self.chunkList.pop()        # Delete last b''
                    break
        fi.close()
        
        if verbose == True:                                                 # Debug if set verbos
            for _ in range(len(self.chunkList)):
                print("[CHUNK {0}]-> {1}\n".format(_,self.chunkList[_]))    # Dump any chunk

    def getChunkById(self,id):
        return self.chunkList[id]

    def getChunkSize(self):
        return self.chunkSize
    
    def getChunkCount(self):
        return len(self.chunkList)


