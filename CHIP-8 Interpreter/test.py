from frontend.display import Display, QApplication
from testing.display_test.backend import Backend
import sys


def hook(type, value, traceback):
    print(type)
    print(traceback)


def main():
    sys.__excepthook__ = hook
    app = QApplication([])
    height = 32
    width = 64
    window = Display(width, height)
    processor = Backend(width, height)
    connect_signals(window, processor)
    processor.start()
    window.show()
    sys.exit(app.exec())


def connect_signals(window, processor):
    processor.send_screen.connect(window.update_screen)
    processor.send_update_color.connect(window.update_color)
    processor.request_screen.connect(window.send_screen)
    window.send_screen_signal.connect(processor.receive_screen)
    window.send_ended_gui.connect(processor.testing)

main()