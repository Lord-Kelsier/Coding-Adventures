import sys
from numpy import array
from Memory.memory import Memory
from CPU.Register.register import Register
# import pyglet
import random
import time
from PyQt5.QtCore import pyqtSignal, QObject, Qt
# keys = pyglet.window.key
KEY_MAP = {
    Qt.Key_1: 0x1,
    Qt.Key_2: 0x2,
    Qt.Key_3: 0x3,
    Qt.Key_4: 0xc,
    Qt.Key_Q: 0x4,
    Qt.Key_W: 0x5,
    Qt.Key_E: 0x6,
    Qt.Key_R: 0xd,
    Qt.Key_A: 0x7,
    Qt.Key_S: 0x8,
    Qt.Key_D: 0x9,
    Qt.Key_F: 0xe,
    Qt.Key_Z: 0xa,
    Qt.Key_X: 0,
    Qt.Key_C: 0xb,
    Qt.Key_V: 0xf
}


class CPU (QObject):
    enviar_update_color = pyqtSignal(int, int, bool)
    send_close_window = pyqtSignal()
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.key_inputs = array([0x0] * 16)
        self.widthC = 64
        self.heightC = 32
        self.should_draw = False
        self.terminated = False
        self.sprites = []
        self.log_file = open("log.txt", "w")
        # self.pixel = pyglet.resource.image("pixel.png")
        # self.batch = pyglet.graphics.Batch()
        # for i in range(self.widthC * self.heightC):
        #     self.sprites.append(pyglet.sprite.Sprite(
        #         self.pixel, batch=self.batch))
        self.log("-" * 30)
        self.display_buffer = array([0x0] * self.heightC * self.widthC)
        self.memory = Memory()
        # self.buzz = pyglet.resource.media("buzz.wav", streaming=False)
        self.register = Register()
        # self.player = pyglet.media.Player()
        self.func_map = {
            0x0: self._0XXX,
            0x1: self._1nnn,
            0x2: self._2nnn,
            0x3: self._3xkk,
            0x4: self._4xkk,
            0x5: self._5xy0,
            0x6: self._6xkk,
            0x7: self._7xkk,
            0x8: self._8xyI,
            0x9: self._9xy0,
            0xa: self._annn,
            0xb: self._bnnn,
            0xc: self._cxkk,
            #0xd: self._dxyn,
            0xe: self._eandf,
            0xf: self._eandf
        }

    def initialize(self):
        self.clear_window()
        self.should_draw = False
        self.key_inputs = array([0x0] * 16)
        self.register.set_registers_to_zero()
        self.memory.reset_memory()
        self.display_buffer = array([0x0] * self.heightC * self.widthC)
        self.load_fonts()
    def main(self):
        self.initialize()
        self.load_rom(sys.argv[1])
        i = 1
        while True:
            self.log(f"Cycle {i}")
            # self.dispatch_events()
            # self.cycle()

            if self.terminated:
                break
            # self.draw()
            i += 1
            time.sleep(0.05)

    def load_fonts(self):
        fonts = {
            0x0: [0xf0, 0x90, 0x90, 0x90, 0xf0],
            0x1: [0x20, 0x60, 0x20, 0x20, 0x70],
            0x2: [0xf0, 0x10, 0xf0, 0x80, 0xf0],
            0x3: [0xf0, 0x10, 0xf0, 0x10, 0xf0],
            0x4: [0x90, 0x90, 0xf0, 0x10, 0x10],
            0x5: [0xf0, 0x80, 0xf0, 0x10, 0xf0],
            0x6: [0xf0, 0x80, 0xf0, 0x90, 0xf0],
            0x7: [0xf0, 0x10, 0x20, 0x40, 0x40],
            0x8: [0xf0, 0x90, 0xf0, 0x90, 0x90],
            0x9: [0xf0, 0x90, 0xf0, 0x10, 0xf0],
            0xa: [0xf0, 0x90, 0xf0, 0x90, 0x90],
            0xb: [0xe0, 0x90, 0xe0, 0x90, 0xe0],
            0xc: [0xf0, 0x80, 0x80, 0x80, 0xf0],
            0xd: [0xe0, 0x90, 0x90, 0x90, 0xe0],
            0xe: [0xf0, 0x80, 0xf0, 0x80, 0xf0],
            0xf: [0xf0, 0x80, 0xf0, 0x80, 0x80]
        }
        i = 0
        for code in fonts.values():
            for linea in code:
                self.memory.RAM[i] = linea
                i += 1

    def on_key_press(self, key):
        self.log(f"Key pressed: {key}")
        if key == Qt.Key_Escape:
            self.terminate()
        if key in KEY_MAP.keys():
            self.key_inputs[KEY_MAP[key]] = 1

    def on_key_release(self, key):
        self.log(f"Key released: {key}")
        print(f"key released {key}")
        if key in KEY_MAP.keys():
            self.key_inputs[KEY_MAP[key]] = 0

    def load_rom(self, rom_path):
        self.log(f"Loading {rom_path}...")
        with open(rom_path, "rb") as binary:
            data = binary.read()
            for i in range(len(data)):
                self.memory.RAM[self.memory.START_PROG_RAM + i] = data[i]

    def clear_window(self):
        self.log("Window Cleared")

    def log(self, text):
        if not self.log_file.closed:
            print(text, file=self.log_file)

    def cycle(self):
        self.register.op_code = self.memory.RAM[self.register.program_counter] << 8 | self.memory.RAM[self.register.program_counter + 1]
        self.register.program_counter += 2  # saltamos a la siguiente instruccion

        func_map_idx = self.hex_to_list(self.register.op_code)[-1]
        self.log(
            f"executing: {hex(self.register.op_code)} - idx: {func_map_idx}")
        self.func_map[func_map_idx](self.register.op_code)

        # if self.register.delay_timer > 0:
        #     self.register.delay_timer -= 1
        # if self.register.sound_timer > 0:
        #     self.register.sound_timer -= 1
        #     if self.register.sound_timer == 0:
        #         self.buzz.play()
        # self.log("Cycle ending")

    def terminate(self):
        self.log("Safe Closing")
        self.log_file.close()
        self.terminated = True
        self.send_close_window.emit()

    def get_key(self):
        i = 0
        while i < 16:
            if self.key_inputs[i] == 1:
                return i
        i += 1
        return -1

    def hex_to_list(self, num: int) -> tuple:
        # it counts from right to left
        parts = (0x000f, 0x00f0, 0x0f00, 0xf000)
        nums = []
        for i in range(4):
            nums.append((parts[i] & num) >> 4*i)
        return tuple(nums)

    def list_to_int(self, *nums):
        i = 0
        suma = 0
        for e in nums:
            suma += e * (16 ** i)
            i += 1
        return suma

    # def draw(self):  # no entiendo lo qe hace
    #     if self.should_draw:
    #         self.log("Drawing...")
    #         self.clear_window()
    #         line_counter = 0
    #         i = 0
    #         while i < self.widthC * self.heightC:
    #             if self.display_buffer[i] == 1:
    #                 self.pixel.blit((i % self.widthC) * 10,
    #                                 ((self.heightC-1) * 10) - ((i//64) * 10))
    #             i += 1
    #         self.flip()
    #         self.should_draw = False

    def _0XXX(self, code):
        if code == 0x00e0:
            self._00E0(code)
        elif code == 0x00ee:
            self._00EE(code)
        else:
            self._0nnn(code)

    def _00E0(self, code):
        code = hex(code)
        self.log(f"{code}: Clears the screen")
        self.display_buffer = array([0] * 64 * 32)
        # self.clear_window()
        self.should_draw = True

    def _00EE(self, code):
        code = hex(code)
        self.log(f"{code}: Returns from subroutine")
        self.register.program_counter = self.register.stack.pop()

    def _0nnn(self, code):
        addr = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code} Jump to routine")
        addr = self.list_to_int(addr[0], addr[1], addr[2])
        self.memory.RAM[self.memory.START_PROG_RAM + addr]
        pass  # execute routine

    def _1nnn(self, code):
        addr = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code}: Jump to location")
        addr = self.list_to_int(addr[0], addr[1], addr[2])
        self.register.program_counter = addr

    def _2nnn(self, code):
        addr = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code}: Call subroutine")
        addr = self.list_to_int(addr[0], addr[1], addr[2])
        self.register.stack.append(self.register.program_counter)
        self.register.program_counter = addr

    def _3xkk(self, code):
        num = self.hex_to_list(code)
        idx = num[2]
        value = self.list_to_int(num[0], num[1])
        code = hex(code)
        self.log(
            f"{code}: Skip next instr if {self.register.all_purpuse[idx]} == {value}")
        if self.register.all_purpuse[idx] == value:
            self.register.program_counter += 2

    def _4xkk(self, code):
        num = self.hex_to_list(code)
        idx = num[2]
        value = self.list_to_int(num[0], num[1])
        code = hex(code)
        self.log(
            f"{code}: Skip next instr if {self.register.all_purpuse[idx]} != {value}")
        if self.register.all_purpuse[idx] != value:
            self.register.program_counter += 2

    def _5xy0(self, code):
        num = self.hex_to_list(code)
        idx = num[2]
        idy = num[1]
        code = hex(code)
        self.log(
            f"{code}: Skip next instr if {self.register.all_purpuse[idx]} != {self.register.all_purpuse[idy]}")
        if self.register.all_purpuse[idx] == self.register.all_purpuse[idy]:
            self.register.program_counter += 2

    def _6xkk(self, code):
        num = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code} Set vx = kk")
        idx = num[2]
        value = self.list_to_int(num[0], num[1])
        self.register.all_purpuse[idx] = value

    def _7xkk(self, code):
        num = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code} Set vx = vx + kk")
        idx = num[2]
        value = self.list_to_int(num[0], num[1])
        self.register.all_purpuse[idx] += value

    def _8xyI(self, code):
        num = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code} Depend of last digit")
        idx = num[2]
        idy = num[1]
        I = num[0]
        if I == 0:
            self.register.all_purpuse[idx] = self.register.all_purpuse[idy]
            # self.register.all_purpuse[idx] &= 0xff
        elif I == 1:
            self.register.all_purpuse[idx] |= self.register.all_purpuse[idy]
        elif I == 2:
            self.register.all_purpuse[idx] &= self.register.all_purpuse[idy]
        elif I == 3:
            self.register.all_purpuse[idx] ^= self.register.all_purpuse[idy]
        elif I == 4:
            suma = self.register.all_purpuse[idx] + \
                self.register.all_purpuse[idy]
            self.register.all_purpuse[0xf] = suma & 0xf00  # carry digit
            self.register.all_purpuse[idx] = suma & 0xff
        elif I == 5:
            if self.register.all_purpuse[idx] > self.register.all_purpuse[idy]:
                self.register.all_purpuse[0xf] = 1
            else:
                self.register.all_purpuse[0xf] = 0
            self.register.all_purpuse[idx] = abs(
                self.register.all_purpuse[idx] - self.register.all_purpuse[idy])
        elif I == 6:
            self.register.all_purpuse[0xf] = self.register.all_purpuse[idx] & 0x1
            self.register.all_purpuse[idx] = self.register.all_purpuse[idx] >> 1
        elif I == 7:
            if self.register.all_purpuse[idy] > self.register.all_purpuse[idx]:
                self.register.all_purpuse[0xf] = 1
            else:
                self.register.all_purpuse[0xf] = 0
            self.register.all_purpuse[idx] = abs(
                self.register.all_purpuse[idy] - self.register.all_purpuse[idx])
            self.register.all_purpuse[idx] &= 0xff
        elif I == 0xe:
            self.register.all_purpuse[0xf] = (
                self.register.all_purpuse[idx] & 0xf0) >> 7
            self.register.all_purpuse[idx] = self.register.all_purpuse[idx] << 1
            self.register.all_purpuse[idx] &= 0xff

    def _9xy0(self, code):
        num = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code} skip next instr if vx != vy")
        idx = num[2]
        idy = num[1]
        if self.register.all_purpuse[idx] != self.register.all_purpuse[idy]:
            self.register.program_counter += 2

    def _annn(self, code):
        addr = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code} set addr store to nnn")
        addr = self.list_to_int(addr[0], addr[1], addr[2])
        self.register.address_store = addr

    def _bnnn(self, code):
        addr = self.hex_to_list(code)
        code = hex(code)
        self.log(f"{code} jump to location nnn+v0")
        addr = self.list_to_int(addr[0], addr[1], addr[2])
        self.register.program_counter = addr + self.register.all_purpuse[0x0]

    def _cxkk(self, code):
        num = self.hex_to_list(code)
        idx = num[2]
        # value = self.list_to_int(num[0], num[1])
        # self.register.all_purpuse[idx] = randint(0x0, 0xff) & value
        r = int(random.random() * 0xff)
        self.register.all_purpuse[idx] = r & (code & 0xff)
        self.register.all_purpuse[idx] &= 0xff
        code = hex(code)
        self.log(f"{code} set vx = random byte & kk")

    # def _dxyn(self, code):
    #     num = self.hex_to_list(code)
    #     code = hex(code)
    #     self.log(f"{code} display n bytes sprite at addr store at vx,vy")
    #     # self.log("Draw a sprite")
    #     idx = num[2]
    #     idy = num[1]
    #     height = num[0]
    #     self.register.all_purpuse[0xf] = 0
    #     x = self.register.all_purpuse[idx] & 0xff
    #     y = self.register.all_purpuse[idy] & 0xff
    #     row = 0
    #     while row < height:
    #         curr_row = self.memory.RAM[row + self.register.address_store]
    #         pixel_offset = 0
    #         while pixel_offset < 8:
    #             loc = x + pixel_offset + ((y + row) * 64)
    #             pixel_offset += 1
    #             if (y + row) >= 32 or (x + pixel_offset - 1 >= 64):
    #                 continue
    #             mask = 1 << (8 - pixel_offset)
    #             curr_pixel = (curr_row & mask) >> (8 - pixel_offset)
    #             self.display_buffer[loc] ^= curr_pixel
    #             if self.display_buffer[loc] == 0:
    #                 self.register.all_purpuse[0xf] = 1
    #             else:
    #                 self.register.all_purpuse[0xf] = 0
    #         row += 1
    #     self.should_draw = True

    def _eandf(self, code):
        num = self.hex_to_list(code)
        code_str = hex(code)
        first = num[3]
        idx = num[2]
        last = self.list_to_int(num[0], num[1])
        if first == 0xe:
            if last == 0x9e:
                self.log(
                    f"{code_str}: Skips the next instruction if the key stored in idx is pressed")
                key = self.register.all_purpuse[idx] & 0xf
                if self.key_inputs[key] == 1:
                    self.register.program_counter += 2
            elif last == 0xa1:
                self.log(
                    f"{code_str}: Skips the next instruction if the key stored in idx isn't pressed")
                key = self.register.all_purpuse[idx] & 0xf
                if self.key_inputs[key] == 0:
                    self.register.program_counter += 2
        elif first == 0xf:
            if last == 0x07:
                self.log(f"{code_str}: set vx = delay timer")
                self.register.all_purpuse[idx] = self.register.delay_timer
            elif last == 0x0a:
                self.log(f"{code_str}: wait for a key press and store in vx")
                key = self.get_key()
                if key >= 0:
                    self.register.all_purpuse[idx] = key
                else:
                    self.register.program_counter -= 2  # repeat this instruction
            elif last == 0x15:
                self.log(f"{code_str}: set delay timer  = vx")
                self.register.delay_timer = self.register.all_purpuse[idx]
            elif last == 0x18:
                self.log(f"{code_str}: set sound timer = vx")
                self.register.sound_timer = self.register.all_purpuse[idx]
            elif last == 0x1e:
                self.log(f"{code_str}: set addr store += vx")
                self.register.address_store += self.register.all_purpuse[idx]
                if self.register.address_store > 0xfff:
                    self.register.all_purpuse[0xf] = 1
                    self.register.address_store &= 0xfff
                else:
                    self.register.all_purpuse[0xf] = 0
            elif last == 0x29:
                self.log(f"{code_str}: Set index to point to a character")
                self.register.address_store = (
                    5*(self.register.all_purpuse[idx])) & 0xfff  # No se lo que  hace
            elif last == 0x33:
                self.log(
                    f"{code_str}: separa centena decena y unidad guardando en addr store")

                num = self.register.all_purpuse[idx]
                centena = num // 100
                decena = (num % 100) // 10
                unidad = (num % 10)
                self.memory.RAM[self.register.address_store] = centena
                self.memory.RAM[self.register.address_store + 1] = decena
                self.memory.RAM[self.register.address_store + 2] = unidad

            elif last == 0x55:
                self.log(
                    f"{code_str}: Save in RAM all values from all purpose register starting at addr store position")
                vx = ((code & 0xf00) >> 8)
                for i in range(vx + 0x1):
                    self.memory.RAM[i +
                                    self.register.address_store] = self.register.all_purpuse[i]
                self.register.address_store += vx + 1
            elif last == 0x65:
                self.log(
                    f"{code_str}: Save in all purpose register the values from memory starting at addr store position")
                vx = ((code & 0xf00) >> 8)
                for i in range(vx + 0x1):
                    self.register.all_purpuse[i] = self.memory.RAM[i +
                                                                   self.register.address_store]
                self.register.address_store += vx + 1
