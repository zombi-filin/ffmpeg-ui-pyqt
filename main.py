# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *

import subprocess
import sys

version = '0.0.1'

# Класс основного меню
class MainWindow(QMainWindow):
    
    # region Init
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'FFmpeg PyQT {version}')
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        
        # region Target
        self.input_file_width = 0
        self.input_file_height = 0
        
        self.form_edit_target_file_name = QLineEdit(parent=self)
        self.form_button_target_open = QPushButton(text='Открыть', parent=self)
        self.form_button_target_open.clicked.connect(self.form_button_target_open_click)

        self.form_layout_target = QHBoxLayout()
        self.form_layout_target.addWidget(self.form_edit_target_file_name)
        self.form_layout_target.addWidget(self.form_button_target_open)

        self.form_group_box_target = QGroupBox('Файл')
        self.form_group_box_target.setLayout(self.form_layout_target)
        # endregion Target

        # region Изменение размера
        self.form_label_resize_width = QLabel(parent=self, text='Ширина')
        self.form_edit_source_width = QLineEdit(parent=self, readOnly=True)

        self.form_label_resize_height = QLabel(parent=self, text='Высота')
        self.form_edit_source_height = QLineEdit(parent=self, readOnly=True)

        self.form_layout_resize = QHBoxLayout()
        self.form_layout_resize.addWidget(self.form_label_resize_width)
        self.form_layout_resize.addWidget(self.form_edit_source_width)
        self.form_layout_resize.addWidget(self.form_label_resize_height)
        self.form_layout_resize.addWidget(self.form_edit_source_height)
        
        self.form_group_box_resize = QGroupBox('Изменение размера изображения')
        self.form_group_box_resize.setCheckable(True)
        self.form_group_box_resize.setLayout(self.form_layout_resize)
        # endregion Resize

        # region Mainform
        self.form_layout = QFormLayout()
        self.form_layout.addRow(self.form_group_box_target)
        self.form_layout.addRow(self.form_group_box_resize)
        # endregion Mainform

        # region Container 
        container = QWidget()
        container.setLayout(self.form_layout)
        self.setCentralWidget(container)
        # endregion Container

    # endregion Init

    # region Functions
    def form_button_target_open_click(self):
        file_name = QFileDialog.getOpenFileName(self, 'Файл для конвертации', '/', 'Видео файл (*.avi *.mov *.mp4 *.m4a *.3gp *.3g2 *.mj2 *.mpeg)')
        self.target_file_name.setText(file_name[0])
        cmd = f'ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1 -i {file_name[0]}'
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pass
    # endregion Functions

# Основная программа
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())