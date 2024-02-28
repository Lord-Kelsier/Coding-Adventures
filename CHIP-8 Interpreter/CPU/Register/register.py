from numpy import array
from Memory.memory import Memory
from collections import deque
class Register:
    def __init__(self) -> None:
        self.all_purpuse = array([0x0] * 16) # 16 8bit all purpose register/ Vx/ gpio 
        self.address_store = 0x0 # 16bit register for memory address / index
        self.op_code = 0x0
        self.sound_timer = 0x0 # 8bit register for sound
        self.delay_timer = 0x0 # 8bit register for sound
        self.program_counter = Memory.START_PROG_RAM #16bit register to store the currently executing address / pc
        # self.stack_pointer = 0 # 8bit register used to point the top most level of the stack
        self.stack = deque() #16 16bits to store the address that the interpreter shoud return to when finishend with a subroutine 

    def set_registers_to_zero(self):
        self.__init__()