from Crypto import Random

from adversary.Lucky13Adversary import Lucky13Adversary
from oracle.CorrectPaddingOracle import CorrectPaddingOracle
from tls.constants import *
from tls.my_tls import MyTLS

debug = True
N = 30
max_parallel = 2

if debug:
    Ke = b'secretpassword12'
    Km = b'1234567890123456'
    IV = b'0000000000000000'

else:
    Ke = Random.new().read(KEY_SIZE)
    Km = Random.new().read(KEY_SIZE)
    IV = Random.new().read(BLOCK_SIZE)

if __name__ == '__main__':
    plaintext = input('Enter message: ').encode()

    tls = MyTLS(Ke, Km, IV)
    oracle = CorrectPaddingOracle(tls, N, max_parallel)

    ciphertext = tls.encrypt(plaintext)
    print(f'Ciphertext: {ciphertext}')

    adversary = Lucky13Adversary(oracle)
    recoveredText = adversary.decipher(ciphertext)
    print(f'Plaintext recovered: {recoveredText}')
