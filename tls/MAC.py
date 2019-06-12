from Crypto.Hash import HMAC, SHA1


class MAC:
    def __init__(self, k):
        self.k = k

    def tag(self, m):
        hmac = HMAC.new(key=self.k, digestmod=SHA1)
        hmac.update(m)
        return hmac.digest()

    def verify(self, m, t):
        hmac = HMAC.new(key=self.k, digestmod=SHA1)
        hmac.update(m)
        hmac.verify(t)
