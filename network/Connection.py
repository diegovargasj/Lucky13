from time import time


class Sniffer:
    def __init__(self):
        pass

    def intercept(self):
        # TODO implement interception of datagram
        pass


class Connection:
    def __init__(self, inPort, destIP, destPort):
        self.inPort = inPort
        self.destIP = destIP
        self.destPort = destPort

    def send(self, payload):
        # TODO implement send
        pass

    def receive(self):
        # TODO implement receive
        pass

    def sendMultiple(self, payload, n):
        for i in range(n):
            self.send(payload)

        initTime = time()
        # TODO send datagram that forces response and wait for it
        datagram = None
        self.send(datagram)
        self.receive()
        return time() - initTime
