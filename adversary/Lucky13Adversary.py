from tqdm import tqdm

from tls.constants import BLOCK_SIZE


class Lucky13Adversary:
    def __init__(self, oracle):
        self.oracle = oracle
        self.pbar = None

    def decipher(self, ciphertext):
        ciphertext = bytearray(ciphertext)
        fullCiphertext = ciphertext[13 + BLOCK_SIZE:]
        recovered = b''
        blocks = len(fullCiphertext) // BLOCK_SIZE
        self.pbar = tqdm(total=len(fullCiphertext))
        for block in range(blocks):
            recovered = self.__recover_last_block(ciphertext) + recovered
            ciphertext = ciphertext[:-BLOCK_SIZE]

        return recovered

    def __recover_last_block(self, ciphertext):
        recovered = self.__recover_last_two_bytes(ciphertext)
        for byte in range(2, BLOCK_SIZE):
            recovered = self.__recover_byte(
                ciphertext,
                recovered,
                byte
            ) + recovered

        return recovered

    def __recover_last_two_bytes(self, ciphertext):
        attack_blocks = []
        base = bytearray(BLOCK_SIZE - 2)
        for i in range(256):
            for j in range(256):
                delta = base + bytearray([i, j])
                c_att = self.__c_att(ciphertext, delta)
                attack_blocks.append(c_att)

        correct_index = self.oracle.find_correct_padding(attack_blocks)
        self.pbar.update()
        self.pbar.update()
        return bytearray(
            [
                (correct_index // 256) ^ 1,
                (correct_index % 256) ^ 1
            ]
        )

    def __recover_byte(self, ciphertext, recovered, byte):
        attack_blocks = []
        for i in range(256):
            delta = self.__get_delta(i, recovered, byte)
            attack_blocks.append(self.__c_att(ciphertext, delta))

        correct_delta = self.oracle.find_correct_padding(attack_blocks)
        self.pbar.update()
        return bytes([byte ^ correct_delta])

    def __get_delta(self, num, recovered, target_byte):
        reminder = bytearray(BLOCK_SIZE - len(recovered) - 1)
        deltas = bytearray(len(recovered))
        for i in range(len(recovered)):
            deltas[i] = recovered[i] ^ target_byte

        return reminder + num.to_bytes(1, 'big') + deltas

    def __c_att(self, ciphertext, delta):
        c_att = bytearray(ciphertext)
        c_att[:] = ciphertext
        for i in range(BLOCK_SIZE):
            c_att[-2 * BLOCK_SIZE + i] = (
                    ciphertext[-2 * BLOCK_SIZE + i] ^ delta[i]
            )

        return c_att
