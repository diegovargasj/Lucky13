from time import sleep

from Crypto.Cipher import AES

from tls.MAC import MAC
from tls.constants import *


class MyTLS:
    def __init__(self, Ke, Km, IV):
        self.Ke = Ke
        self.Km = Km
        self.IV = IV
        self.MAC = MAC(Km)
        self.SQN = 0
        self.version = 0
        self.type = 0

    def encrypt(self, m):
        SE = AES.new(self.Ke, AES.MODE_CBC, self.IV)
        sqn = self.SQN.to_bytes(SQN_SIZE, 'big')
        hdr = (
                self.version.to_bytes(VERSION_SIZE, 'big') +
                self.type.to_bytes(TYPE_SIZE, 'big') +
                (len(m) // BLOCK_SIZE + 1).to_bytes(LENGTH_SIZE, 'big')
        )
        self.SQN += 1
        plaintext = sqn + hdr + m
        t = self.MAC.tag(plaintext)
        return sqn + hdr + SE.encrypt(self.__add_padding(m + t))

    def decrypt(self, c):
        SE = AES.new(self.Ke, AES.MODE_CBC, self.IV)
        plaintext = SE.decrypt(c[SQN_SIZE + HDR_SIZE:])
        if self.__check_padding(plaintext):
            pt_t = self.__remove_padding(plaintext)
            message = pt_t[:-MAC_SIZE]
            tag = pt_t[-MAC_SIZE:]
            if self.MAC.verify(c[:SQN_SIZE + HDR_SIZE] + message, tag):
                return message

            else:
                return None

        else:
            sleep(0.001)
            message = plaintext[:-MAC_SIZE]
            tag = plaintext[-MAC_SIZE:]
            self.MAC.verify(c[:SQN_SIZE + HDR_SIZE] + message, tag)
            return None

    def __check_padding(self, p):
        last_byte = p[-1]
        if last_byte >= BLOCK_SIZE:
            return False

        for byte in p[-last_byte - 1:]:
            if byte != last_byte:
                return False

        return True

    def __add_padding(self, p):
        padding_len = BLOCK_SIZE - len(p) % BLOCK_SIZE
        padding = bytes([padding_len - 1]) * padding_len
        return p + padding

    def __remove_padding(self, p):
        pad_len = p[-1]
        return p[:-(pad_len + 1)]
