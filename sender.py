# Connor Kanalec

from common import *

class sender:
    RTT = 20
    
    def isCorrupted (self, packet):
        '''Checks if a received packet (acknowledgement) has been corrupted
        during transmission.
        Return true if computed checksum is different than packet checksum.
        '''
        return 1 < packet.seqNum or 1 < packet.ackNum or packet.payload == "="

    def isDuplicate(self, packet):
        '''checks if an acknowledgement packet is duplicate or not
        similar to the corresponding function in receiver side
        '''
        return self.seqNum != packet.ackNum
 
    def getNextSeqNum(self):
        '''generate the next sequence number to be used.
        '''
        if (self.seqNum == 1): self.seqNum = 0
        else: self.seqNum = 1
        return 

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        '''initialize the sequence number and the packet in transit.
        Initially there is no packet is transit and it should be set to None
        '''
        self.seqNum = 0
        self.packetInTransit = None
        return

    def timerInterrupt(self):
        '''This function implements what the sender does in case of timer
        interrupt event.
        This function sends the packet again, restarts the time, and sets
        the timeout to be twice the RTT.
        You never call this function. It is called by the simulator.
        '''
        # send packet and start timer
        increment = self.RTT * 2.0
        self.networkSimulator.udtSend(self.entity, self.packetInTransit)
        self.networkSimulator.startTimer(self.entity, increment)
        return


    def output(self, message):
        '''prepare a packet and send the packet through the network layer
        by calling calling utdSend.
        It also start the timer.
        It must ignore the message if there is one packet in transit
        '''
        # if there is no packet in transit
        if (self.packetInTransit == None):
            # calc checksum
            ackNum = 0
            payload = message.data
            checksum = checksumCalc(payload) + self.seqNum + ackNum
            # create packet
            packet = Packet(self.seqNum, ackNum, checksum, payload)
            # set packet to packet in transit
            self.packetInTransit = packet
            # send packet and start timer
            increment = self.RTT
            self.networkSimulator.udtSend(self.entity, packet)
            self.networkSimulator.startTimer(self.entity, increment)
        return
 
    
    def input(self, packet):
        '''If the acknowlegement packet isn't corrupted or duplicate, 
        transmission is complete. Therefore, indicate there is no packet
        in transition.
        The timer should be stopped, and sequence number  should be updated.

        In the case of duplicate or corrupt acknowlegement packet, it does 
        not do anything and the packet will be sent again since the
        timer will be expired and timerInterrupt will be called by the simulator.
        '''
        # ack packet is ok
        if (not self.isCorrupted(packet) and not self.isDuplicate(packet)):
            # stop timer, set new sequence number, remove packet in transit
            self.networkSimulator.stopTimer(self.entity)
            self.getNextSeqNum()
            self.packetInTransit = None
        return 
