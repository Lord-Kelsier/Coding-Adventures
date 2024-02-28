import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject, QThread
import time as t
from threading import Thread
class Backend(QObject):
    send_screen = pyqtSignal(np.ndarray)
    send_update_color = pyqtSignal(int, int, bool)
    request_screen = pyqtSignal()
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.screen = np.zeros((self.height, self.width), dtype=bool)
        self.threadTest = TestingThread(self, self.send_update_color, self.send_screen)
    def start(self):
        self.send_screen.emit(self.screen)
        
    def receive_screen(self, screen: np.ndarray):
        self.screen = screen

    def testing(self):
        self.threadTest.start()


class TestingThread(QThread):
    send_color = pyqtSignal(int, int, bool)
    send_screen = pyqtSignal(np.ndarray)
    def __init__(self, backend: Backend, send_color, send_screen):
        super().__init__()
        self.backend = backend
        self.send_color = send_color
        self.send_screen = send_screen
    def run(self):
        self.walkthrough()
    def walkthrough(self):
        for y in range(self.backend.height):
            for x in range(self.backend.width):
                self.send_color.emit(x, y, True)
                t.sleep(0.01)
                self.send_color.emit(x, y, False)
        self.send_screen.emit(np.random.randint(0, 2, (self.backend.height, self.backend.width), dtype=bool))
        