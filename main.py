# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *

import sys

# Класс основного меню
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FFmpeg PyQT')
        

# Основная программа
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())