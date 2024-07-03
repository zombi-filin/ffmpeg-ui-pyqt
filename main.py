# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *

import sys

# Класс основного меню
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FFmpeg PyQT')
        
        
        self.target_label = QLabel(parent = self, text = 'Path')
        self.target_file_name = QLineEdit(parent = self)
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.target_label, 0 , 0)
        self.layout.addWidget(self.target_file_name, 0 , 1)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        


# Основная программа
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())