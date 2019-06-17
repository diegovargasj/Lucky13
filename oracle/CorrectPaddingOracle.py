from time import time

from numpy import argmin


class CorrectPaddingOracle:
    def __init__(self, tls, n=10, max_parallel=2):
        self.tls = tls
        self.n = n
        self.max_parallel = max_parallel

    def find_correct_padding(self, ciphertexts):
        delays = []
        for ciphertext in ciphertexts:
            delays.append(self.__get_time(ciphertext))

        print(min(delays))
        return int(argmin(delays))

    def __get_time(self, ciphertext):
        init_time = time()
        for j in range(self.n):
            self.tls.decrypt(ciphertext)

        return time() - init_time
