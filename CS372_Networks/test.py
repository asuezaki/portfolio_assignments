# check segments received
        for j in range(1, len(listIncomingSegments)):
            # check checksum
            listIncomingSegments[j-1].checkChecksum()
            # checking for all segments received
            if listIncomingSegments[j-1].seqnum == listIncomingSegments[j].seqnum - 4:
                print("Segment received:", listIncomingSegments[j-1].payload)
                self.dataReceived += listIncomingSegments[j-1].payload
            if j+1 == len(listIncomingSegments):
                if listIncomingSegments[j].seqnum == listIncomingSegments[j-1].seqnum + 4:
                    print("Segment received:", listIncomingSegments[j].payload)
                    self.dataReceived += listIncomingSegments[j].payload


# checking for lost segments
        if len(listIncomingSegments) < 3:
            # don't send Ack if missing a segment
            self.sendAck = False
        else:
            # otherwise send Ack to confirm all segments were received
            self.sendAck = True