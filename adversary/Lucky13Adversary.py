from network.Connection import Connection
from oracle.CorrectPaddingOracle import CorrectPaddingOracle


class Lucky13Adversary:
    def __init__(self, ciphertext, inPort, destIP, destPort):
        self.ciphertext = ciphertext
        self.delta = 0x0
        self.conn = Connection(inPort, destIP, destPort)
        self.oracle = CorrectPaddingOracle()

    def decipher(self):
        # TODO implement attack
        pass
