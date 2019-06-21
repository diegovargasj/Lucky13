from statistics import mean
from time import time

from numpy import argmin


class CheatingOracle:
    def __init__(self, tls, n=10, max_parallel=2):
        self.tls = tls
        self.n = n
        self.max_parallel = max_parallel

    def find_correct_padding(self, ciphertexts):
        for i in range(len(ciphertexts)):
            ciphertext = ciphertexts[i]
            plaintext = self.tls.decrypt_with_padding(ciphertext)
            if plaintext and plaintext[-1] != 0:
                return i
       
