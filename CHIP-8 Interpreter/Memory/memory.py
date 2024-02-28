from sys import getsizeof
import numpy as np


class Memory:
    RAM = np.array([0x0] * 4096)
    START_PROG_RAM = 0x200

    def __repr__(self) -> str:
        return str(self.RAM)

    def reset_memory(self):
        self.RAM = np.array([0x0] * 4096)


if __name__ == '__main__':
    memory = Memory()
    print(getsizeof(memory.MAP))
