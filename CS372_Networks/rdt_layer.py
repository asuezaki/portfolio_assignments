# CS 372 - Project 2: RDT
# Andrew Suezaki

# Citations
# Idea to use dictionary to keep track of segments from TA ed post https://edstem.org/us/courses/5258/discussion/417710
# Sort method using python stdlib and lambda function https://realpython.com/python-sort/#ordering-values-with-sort
# ways to remove key from dictionary:
# https://thispointer.com/different-ways-to-remove-a-key-from-dictionary-in-python/#:~:text=Remove%20a%20key%20from%20a%20dictionary%20using%20del,-We%20can%20use&text=If%20the%20key%20is%20present,throw%20an%20error%20i.e.%20KeyError.

import copy
from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    # Add items as needed

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        # Add items as needed
        self.dataReceived = ''
        self.index = 0
        self.nextseqnum = 0
        self.SegmentTimeouts = {}
        self.countSegmentTimeouts = 0
        self.sendAck = False
        self.segmentReceived = []
        self.sendBase = 0
        self.acks = []

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        # print('getDataReceived(): Complete this...')

        # ############################################################################################################ #
        # reset string
        self.dataReceived = ''
        # sort segments received by seqnum
        self.segmentReceived.sort(key=lambda x: x.seqnum)
        # build the string with current segments received
        for i in self.segmentReceived:
            self.dataReceived += i.payload
        # return the final string
        return self.dataReceived

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):

        # checking for segment timeouts
        if len(self.SegmentTimeouts) > 0 and self.sendBase == self.nextseqnum:
            # checking all segments still in dict
            for j in self.SegmentTimeouts.values():
                # if it has been more than 5 iterations
                if (self.currentIteration - j.getStartIteration()) > 5 and len(self.sendChannel.sendQueue) < 3:
                    # increase timeout counter
                    self.countSegmentTimeouts += 1
                    # reset start iteration for segment to be resent
                    j.setStartIteration(self.currentIteration)
                    # copy sending segment and resend
                    copy_seg = copy.deepcopy(j)
                    self.sendChannel.send(copy_seg)

        # check that there is data to be sent
        if len(self.dataToSend) > 0:
            # max 3 packets of size 4 characters (<FLOW_CONTROL_WIN_SIZE)
            while len(self.sendChannel.sendQueue) < 3:
                # create a segment
                segmentSend = Segment()
        # ############################################################################################################ #

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)
                # 4 characters max per segment
                data = self.dataToSend[self.nextseqnum:self.nextseqnum+4]
                # seq number for segment
                seqnum = self.nextseqnum
        # ############################################################################################################ #
                # Display sending segment
                segmentSend.setData(seqnum,data)
                print("Sending segment: ", segmentSend.to_string())
                # copy sending segment
                copy_segment = copy.deepcopy(segmentSend)
        # Use the unreliable sendChannel to send the copy of the segment
                self.sendChannel.send(copy_segment)
                self.SegmentTimeouts[seqnum] = copy_segment
                # increment seqnum for next segment
                self.sendBase = self.nextseqnum
                self.nextseqnum += 4


    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()
        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented

        # checking if nothing was received
        if len(listIncomingSegments) == 0:
            return
        # sorts the list of segments by seqnum
        else:
            listIncomingSegments.sort(key=lambda x: x.seqnum)

        # if it is the client
        if len(self.dataToSend) > 0:
            self.sendAck = False
            # for each ack from the server
            for i in listIncomingSegments:
                if i.acknum < self.sendBase:
                    self.sendBase = i.acknum
                else:
                    return
            self.nextseqnum = self.sendBase
            return

        # check segments received
        for j in listIncomingSegments:
            # check checksum
            if j.checkChecksum():
                # add segment to data received
                print("Segment received:", j.payload)
                dupe = False
                # checking if segment was already added to dataReceived string
                for k in self.segmentReceived:
                    if j.seqnum == k.seqnum:
                        dupe = True
                # if not, adds it to dataReceived string
                if not dupe:
                    self.segmentReceived.append(j)
                # remove segment from timeout dict if received
                if j.seqnum in self.SegmentTimeouts.keys():
                    self.SegmentTimeouts.pop(j.seqnum)
                # send an Ack for received segment
                self.sendAck = True
            if not j.checkChecksum():
                continue

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?
        # print('processReceive(): Complete this...')

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
            if self.sendAck:
                # for each segment received, send an ack
                segmentAck = Segment()  # Segment acknowledging packet(s) received
                acknum = j.seqnum + 4
        # ############################################################################################################ #
        # Display response segment
                segmentAck.setAck(acknum)
                print("Sending ack: ", segmentAck.to_string())
        # Use the unreliable sendChannel to send the ack packet
                self.sendChannel.send(segmentAck)
                # set prev ack sent
                self.sendBase = acknum
