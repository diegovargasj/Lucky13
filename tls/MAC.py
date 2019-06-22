from math import ceil

from Crypto.Hash import HMAC, SHA1

from tls.constants import BLOCK_SIZE, MAC_SIZE


class MAC:
    def __init__(self, k, rep=10):
        self.k = k
        self.hmac = HMAC.new(key=k, digestmod=SHA1)
        self.sha1 = SHA1.new()
        self.rep = rep

    def tag(self, m):
        #hmac = self.hmac.copy()
        #hmac.update(m)
        return self.__hmac(m)

    def verify(self, m, t):
        #hmac = self.hmac.copy()
        #hmac.update(m)
        return self.__hmac(m) == t

    def __hmac(self, m):
        res = bytearray(MAC_SIZE)
        for b in range(int(ceil(len(m) // BLOCK_SIZE))):
            for r in range(self.rep):
                block = m[b * BLOCK_SIZE: min(len(m), (b + 1) * BLOCK_SIZE)]
                sha1 = self.sha1.copy()
                sha1.update(res + block)
                res = sha1.digest()

        return res
