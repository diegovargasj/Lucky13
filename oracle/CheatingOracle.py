class CheatingOracle:
    def __init__(self, tls, n=10):
        self.tls = tls
        self.n = n

    def find_correct_padding(self, ciphertexts):
        for i in range(len(ciphertexts) - 1, -1, -1):
            ciphertext = ciphertexts[i]
            plaintext = self.tls.dec_no_mac(ciphertext)
            if plaintext and plaintext[-1] != 0:
                return i
