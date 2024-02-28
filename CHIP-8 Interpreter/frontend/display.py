from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal
import sys
from random import randint
import numpy as np

class Display(QWidget):
    send_screen_signal = pyqtSignal(np.ndarray)
    send_ended_gui = pyqtSignal()
    send_key_pressed = pyqtSignal(Qt.Key)
    send_key_released = pyqtSignal(Qt.Key)
    def __init__(self, w: int, h: int):
        super().__init__()
        self.x_lenght = w
        self.y_lenght = h
        # Definimos la geometría de la ventana.
        # Parámetros: (x_superior_izq, y_superior_izq, ancho, alto)
        self.setGeometry(75, 100, 1792, 896)
        self.white = QPixmap(1, 1)
        self.white.fill(Qt.white)
        self.black = QPixmap(1, 1)
        self.black.fill(Qt.black)
        self.width_px = self.width() // self.x_lenght
        self.height_px = self.height() // self.y_lenght
        self.set_gui()
    def keyPressEvent(self, event) -> None:
        self.send_key_pressed.emit(event.key())
    def keyReleaseEvent(self, event) -> None:
        self.send_key_released.emit(event.key())
    def set_gui(self):
        self.grid = [[QLabel(self) for _ in range(self.x_lenght) ] for __ in range(self.y_lenght)]
        for y in range(self.y_lenght):
            for x in range(self.x_lenght):
                self.set_color_of_pixel(x, y, self.black)
        
    def send_screen(self):
        array = np.zeros((self.y_lenght, self.x_lenght), dtype=bool)
        for y in range(self.y_lenght):
            for x in range(self.x_lenght):
                if self.grid[y][x].pixmap() == self.white:
                    array[y][x] = True
                else:
                    array[y][x] = False
        self.send_screen_signal.emit(array)
    def set_color_of_pixel(self, x: int, y: int, color: QPixmap):
        self.grid[y][x].setPixmap(color)
        self.grid[y][x].setScaledContents(True)
        self.grid[y][x].setGeometry(x * self.width_px, y * self.height_px, self.width_px, self.height_px)
    
    def update_color(self, x: int, y: int, color: bool):
        self.set_color_of_pixel(x, y, self.white if color else self.black)

    def update_screen(self, screen: np.ndarray):
        print("updating screen")
        for y in range(self.y_lenght):
            for x in range(self.x_lenght):
                self.set_color_of_pixel(x, y, self.white if screen[y][x] else self.black)
        self.send_ended_gui.emit()
if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = Display(64, 32)
    ventana.show()
    sys.exit(app.exec())
