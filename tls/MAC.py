from Crypto.Hash import HMAC, SHA1


class MAC:
    def __init__(self, k):
        self.k = k
        self.hmac = HMAC.new(key=k, digestmod=SHA1)

    def tag(self, m):
        hmac = self.hmac.copy()
        hmac.update(m)
        return hmac.digest()

    def verify(self, m, t):
        hmac = self.hmac.copy()
        hmac.update(m)
        return hmac.digest() == t
