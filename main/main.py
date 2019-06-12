from Crypto import Random

from adversary.Lucky13Adversary import Lucky13Adversary
from oracle.CorrectPaddingOracle import CorrectPaddingOracle
from tls.constants import *
from tls.my_tls import MyTLS

if __name__ == '__main__':
    Ke = Random.new().read(KEY_SIZE)
    Km = Random.new().read(KEY_SIZE)
    IV = Random.new().read(BLOCK_SIZE)
    tls = MyTLS(Ke, Km, IV)
    plaintext = input('Enter message: ').encode()
    ciphertext = tls.encrypt(plaintext)
    print(f'Ciphertext: {ciphertext}')
    oracle = CorrectPaddingOracle(tls)
    adversary = Lucky13Adversary(ciphertext, oracle)
    recoveredText = adversary.decipher()
    print(f'Plaintext recovered: {recoveredText}')
