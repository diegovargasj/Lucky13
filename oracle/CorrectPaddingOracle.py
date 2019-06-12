import math
from numpy import argmin
from time import time


class CorrectPaddingOracle:
    def __init__(self, tls, n=10):
        self.minRegister = None
        self.minDelaly = math.inf
        self.tls = tls
        self.n = n

    def find_correct_padding(self, ciphertexts):
        delays = []
        for i in range(len(ciphertexts)):
            ciphertext = ciphertexts[i]
            init_time = time()
            for j in range(self.n):
                self.tls.decrypt(ciphertext)

            delays.append(time() - init_time)

        return argmin(delays)
