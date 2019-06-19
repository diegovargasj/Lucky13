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
        correct_index = self.__recover_last_two_bytes(ciphertext)
        recovered = bytearray(
            [
                (correct_index // 256) ^ 1,
                (correct_index % 256) ^ 1
            ]
        )
        deltas = [correct_index // 256, correct_index % 256]
        for byte in range(2, BLOCK_SIZE):
            recovered = self.__recover_byte(
                ciphertext,
                deltas,
                byte
            ) + recovered
            for i in range(len(deltas)):
                deltas[i] = (deltas[i] + 1) % 256

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
        return correct_index

    def __recover_byte(self, ciphertext, deltas, byte):
        recovered = b''
        attack_blocks = []
        for i in range(256):
            delta = self.__get_delta(i, deltas)
            attack_blocks.append(self.__c_att(ciphertext, delta))

        correct_delta = self.oracle.find_correct_padding(attack_blocks)
        recovered += bytes([byte ^ correct_delta])
        deltas.insert(0, correct_delta)
        self.pbar.update()
        return recovered

    def __get_delta(self, num, deltas):
        reminder = bytearray(BLOCK_SIZE - len(deltas) - 1)
        return reminder + num.to_bytes(1, 'big') + bytearray(deltas)

    def __c_att(self, ciphertext, delta):
        c_att = bytearray(ciphertext)
        c_att[:] = ciphertext
        for i in range(BLOCK_SIZE):
            c_att[-2 * BLOCK_SIZE + i] = (
                    ciphertext[-2 * BLOCK_SIZE + i] ^ delta[i]
            )

        return c_att

