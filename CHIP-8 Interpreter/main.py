# from CPU.Register.register import Register
from CPU.cpu import CPU
from testing.unit_tests import execute_unit_tests
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QObject
from frontend.display import Display

# http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0
# https://github.com/maranas/pyChip8Emu

class Executer(QThread):
    def __init__(self, cpu) -> None:
        super().__init__()
        self.cpu = cpu
    def run(self) -> None:
        self.cpu.main()


def hook(type, value, traceback):
    print(type)
    print(traceback)

def main():
    cpu = CPU()
    if len(sys.argv) != 2:
        print("Colocar ruta de la ROM")
        return
    if sys.argv[1] in ['test', 'TEST']:
        execute_unit_tests(cpu)
        return
    sys.__excepthook__ = hook
    app = QApplication([])
    height = 32
    width = 64
    window = Display(width, height)
    executer = Executer(cpu)
    connect_signals(window, executer)
    executer.start()
    window.show()
    sys.exit(app.exec())
def connect_signals(window: Display, executer: Executer):
    window.send_key_pressed.connect(executer.cpu.on_key_press)
    executer.cpu.send_close_window.connect(window.close)
    window.send_key_released.connect(executer.cpu.on_key_release)
main()

