from time import time

from numpy import argmin


class CorrectPaddingOracle:
    def __init__(self, tls, n=10):
        self.tls = tls
        self.n = n

    def find_correct_padding(self, ciphertexts):
        delays = []
        for ciphertext in ciphertexts:
            init_time = time()
            for j in range(self.n):
                try:
                    self.tls.decrypt(ciphertext)

                except ValueError:
                    pass

            delays.append(time() - init_time)

        return int(argmin(delays))
