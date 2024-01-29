import sys
import time
from random import randrange
from socket import *

# Random number from 0 - 98
# Retrive number in range 1 - 99
def randomSequence():return str(randrange(0,98))


# Create PCT Package
def createPCTPackage():
    pct = "[PCT]"
    sequence = randomSequence().encode()
    return pct.encode() +b"/"+sequence  # [PCT]/Sequence
    

# Create CT Package
def createCTPackage(sequence):
    operation = "[CT]"
    sequence_ack = str(sequence + 1).encode()
    return operation.encode() +b"/"+sequence_ack    #[CT]/Sequence + 1


class core:
    def __init__(self):
        self.chunkSize = 1024   # Default 1KB
        self.Status = None      # Status
        self.operation = None

        # self.operations = {     # OPERATIONS
        #     1: "GET",           # Get packet
        #     2: "PUSH",          # Send packet
        #     3: "REP",           # Retransmit packet
        #     10: "PCT",      # Precontact
        #     11: "CT",       # Contact
        
        # # === WARNING ===

        #     20: "ERROR"         # Error
        # }

    def createChunk(self, file,type, chunk,verbose=False):  # Create Chunk of file
        self.chunkList = []    # Chunk buffer

        if chunk >= 1:
            self.chunkSize = chunk
        else:
            return 1
        

        if type == "png":                           # If type is png
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


