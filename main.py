# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *

import sys

# Класс основного меню
class MainWindow(QMainWindow):
    
    # region Init
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FFmpeg PyQT')
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        
        # region Target
        self.target_file_name = QLineEdit(parent = self)
        self.target_open_button = QPushButton(text = 'Открыть', parent = self)
        self.target_open_button.clicked.connect(self.target_open_button_click)

        self.target_hor_layout = QHBoxLayout()
        self.target_hor_layout.addWidget(self.target_file_name)
        self.target_hor_layout.addWidget(self.target_open_button)

        self.target_group_box = QGroupBox('Файл')
        self.target_group_box.setLayout(self.target_hor_layout)
        # endregion Target

        # region Mainform
        self.form_layout = QFormLayout()
        self.form_layout.addRow(self.target_group_box)
        #endregion Mainform

        # region Container 
        container = QWidget()
        container.setLayout(self.form_layout)
        
        self.setCentralWidget(container)
        # endregion Container

    # endregion Init

    # region Functions
    def target_open_button_click(self):
        file_name = QFileDialog.getOpenFileName(self, 'Файл для конвертации', '/', 'Видео файл (*.avi *.mov *.mp4 *.m4a *.3gp *.3g2 *.mj2 *.mpeg)')
        self.target_file_name.setText(file_name[0])
        pass
    # endregion Functions

# Основная программа
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())