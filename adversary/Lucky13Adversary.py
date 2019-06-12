class Lucky13Adversary:
    def __init__(self, ciphertext, oracle):
        self.ciphertext = ciphertext
        self.delta = 0x0
        self.oracle = oracle
        self.recovered = b''

    def decipher(self):
        # TODO implement attack
        pass
