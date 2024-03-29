from Crypto import Random

from adversary.Lucky13Adversary import Lucky13Adversary
from oracle.CorrectPaddingOracle import CorrectPaddingOracle
from oracle.CheatingOracle import CheatingOracle
from tls.constants import *
from tls.my_tls import MyTLS

debug = True
N = 5

if __name__ == '__main__':
    plaintext = input('Enter message: ').encode()

    Ke = Random.new().read(KEY_SIZE)
    Km = Random.new().read(KEY_SIZE)
    IV = Random.new().read(BLOCK_SIZE)

    tls = MyTLS(Ke, Km, IV)
    # oracle = CorrectPaddingOracle(tls, N)
    oracle = CheatingOracle(tls, N)

    ciphertext = tls.encrypt(plaintext)
    print(f'Ciphertext: {ciphertext}')

    adversary = Lucky13Adversary(oracle)
    recoveredText = adversary.decipher(ciphertext)
    print(f'Full plaintext recovered: {recoveredText}')
