# Connor Kanalec

from common import *

class receiver:
    
    def isCorrupted(self, packet):
        ''' Checks if a received packet has been corrupted during transmission.
        Return true if computed checksum is different than packet checksum.'''
        checksum = checksumCalc(packet.payload) + packet.seqNum + packet.ackNum
        return packet.checksum != checksum
   
    def isDuplicate(self, packet):
        '''checks if packet sequence number is the same as expected sequence number'''
        return packet.seqNum != self.expectSeqNum
    
    def getNextExpectedSeqNum(self):
        '''The expected sequence numbers are 0 or 1'''
        if (self.expectSeqNum == 1): self.expectSeqNum = 0
        else: self.expectSeqNum = 1
        return
    
    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))

    def init(self):
        '''initialize expected sequence number'''
        self.expectSeqNum = 0
        return

    def input(self, packet):
        '''This method will be called whenever a packet sent 
        from the sender arrives at the receiver. If the received
        packet is corrupted or duplicate, it sends a packet where
        the ack number is the sequence number of the  last correctly
        received packet. Since there is only 0 and 1 sequence numbers,
        you can use the sequence number that is not expected.
        
        If packet is OK (not a duplicate or corrupted), deliver it to the
        application layer and send an acknowledgement to the sender
        ''' 
        # packet is ok
        if (not self.isDuplicate(packet) and not self.isCorrupted(packet)): 
            # new ack num and then increment next expected seq num
            ackNum = self.expectSeqNum
            self.getNextExpectedSeqNum()
            # deliver packet to application layer
            msg = Message(packet.payload)
            self.networkSimulator.deliverData(self.entity, msg)
        # packet is not ok, use old ack num
        elif (self.expectSeqNum == 1): ackNum = 0
        else: ackNum = 1
        # create ack packet
        seqNum = 0
        checksum = ackNum
        packet = Packet(seqNum, ackNum, checksum)
        # send ack packet
        self.networkSimulator.udtSend(self.entity, packet)
        return
