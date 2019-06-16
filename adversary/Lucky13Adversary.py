from tqdm import tqdm

from tls.constants import BLOCK_SIZE


class Lucky13Adversary:
    def __init__(self, oracle):
        self.oracle = oracle

    def decipher(self, ciphertext):
        fullCiphertext = bytearray(ciphertext[13:])
        recovered = b''
        blocks = len(fullCiphertext) // BLOCK_SIZE
        pbar = tqdm(total=len(fullCiphertext))
        cnt = 0
        for b in range(blocks):
            ciphertext = fullCiphertext[b * BLOCK_SIZE: (b + 1) * BLOCK_SIZE]
            deltas = []
            for bt in range(BLOCK_SIZE):
                attack_blocks = []
                for i in range(255):
                    delta = self.__get_delta(i + 1, deltas)
                    attack_blocks.append(self.__c_att(ciphertext, delta))

                correct_delta = self.oracle.find_correct_padding(
                    attack_blocks
                ) + 1
                d = self.__get_delta(correct_delta, deltas)
                target_byte = self.__c_att(ciphertext, d)[-bt - 1]
                recovered += bytes([target_byte ^ bt ^ correct_delta])
                deltas = [correct_delta] + deltas
                for i in range(len(deltas)):
                    deltas[i] = (deltas[i] + 1) % 256

                cnt += 1
                pbar.update(cnt * 2 / len(fullCiphertext))

        return recovered

    def __get_delta(self, num, deltas):
        reminder = bytearray(BLOCK_SIZE - len(deltas) - 1)
        return reminder + num.to_bytes(1, 'big') + bytearray(deltas)

    def __c_att(self, ciphertext, delta):
        return delta + ciphertext
        # for i in range(BLOCK_SIZE):
        #     ciphertext[-2 * BLOCK_SIZE + i] = (
        #             ciphertext[-2 * BLOCK_SIZE + i] ^ delta[i]
        #     )
        #
        # return ciphertext
