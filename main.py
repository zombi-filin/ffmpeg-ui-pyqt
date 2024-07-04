# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *

import sys

# Класс основного меню
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FFmpeg PyQT')
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        
        self.form_layout = QFormLayout()

        self.hor_layout_target = QHBoxLayout()
        self.target_label = QLabel(parent = self, text = 'Файл')
        self.hor_layout_target.addWidget(self.target_label)

        self.target_file_name = QLineEdit(parent = self)
        self.hor_layout_target.addWidget(self.target_file_name)

        self.form_layout.addRow(self.hor_layout_target)

        container = QWidget()
        container.setLayout(self.form_layout)
        
        self.setCentralWidget(container)
        


# Основная программа
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())