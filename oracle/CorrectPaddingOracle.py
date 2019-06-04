import math


class CorrectPaddingOracle:
    def __init__(self):
        self.minRegister = None
        self.minDelaly = math.inf

    def add_delay(self, register, delay):
        if delay < self.minDelaly:
            self.minDelaly = delay
            self.minRegister = register

    def get_correct_padding_register(self):
        self.minDelaly = math.inf
        return self.minRegister
