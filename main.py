# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *

import os
import subprocess
import sys

VERSION = '0.0.1'

RESIZE_EDIT_WIDTH = 50

# Класс основного меню
class MainWindow(QMainWindow):
    
    # region Init
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'FFmpeg PyQT {VERSION}')
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
        self.form_edit_src_width = QLineEdit(parent=self, readOnly=True)
        self.form_edit_src_width.setFixedWidth(RESIZE_EDIT_WIDTH)
        self.form_edit_dest_width = QLineEdit(parent=self, maxLength=4)
        self.form_edit_dest_width.setFixedWidth(RESIZE_EDIT_WIDTH)

        self.form_edit_src_height = QLineEdit(parent=self, readOnly=True)
        self.form_edit_src_height.setFixedWidth(RESIZE_EDIT_WIDTH)
        self.form_edit_dest_height = QLineEdit(parent=self, maxLength=4)
        self.form_edit_dest_height.setFixedWidth(RESIZE_EDIT_WIDTH)

        
        self.form_layout_resize = QHBoxLayout()
        self.form_layout_resize.addWidget(QLabel(parent=self, text='Ширина'))
        self.form_layout_resize.addWidget(self.form_edit_src_width)
        self.form_layout_resize.addWidget(QLabel(parent=self, text='-->'))
        self.form_layout_resize.addWidget(self.form_edit_dest_width)
        
        self.form_layout_resize.addSpacing(32)
        
        self.form_layout_resize.addWidget(QLabel(parent=self, text='Высота'))
        self.form_layout_resize.addWidget(self.form_edit_src_height)
        self.form_layout_resize.addWidget(QLabel(parent=self, text='-->'))
        self.form_layout_resize.addWidget(self.form_edit_dest_height)
        
        self.form_layout_resize.addStretch(1)

        self.form_group_box_resize = QGroupBox('Изменение размера изображения')
        self.form_group_box_resize.setCheckable(True)
        self.form_group_box_resize.setChecked(False)
        self.form_group_box_resize.setLayout(self.form_layout_resize)
        # endregion Resize

        # region Обрезка видео по времени
        
        self.form_spin_from_time_crop = QSpinBox()
        self.form_spin_from_time_crop.setMinimum(0)
        self.form_spin_from_time_crop.setMaximum(0)
        self.form_spin_from_time_crop.valueChanged.connect(self.form_spin_time_crop_valueChanged)
        

        self.form_spin_to_time_crop = QSpinBox()
        self.form_spin_to_time_crop.setMinimum(0)
        self.form_spin_to_time_crop.setMaximum(0)
        self.form_spin_to_time_crop.valueChanged.connect(self.form_spin_time_crop_valueChanged)
        

        self.form_layout_time_crop = QHBoxLayout()
        self.form_layout_time_crop.addWidget(self.form_spin_from_time_crop)
        self.form_layout_time_crop.addWidget(self.form_spin_to_time_crop)

        self.form_group_box_time_crop = QGroupBox('Обрезка по времени')
        self.form_group_box_time_crop.setCheckable(True)
        self.form_group_box_time_crop.setChecked(False)
        self.form_group_box_time_crop.setLayout(self.form_layout_time_crop)
        # endregion

        # region Mainform
        self.form_layout = QFormLayout()
        self.form_layout.addRow(self.form_group_box_target)
        self.form_layout.addRow(self.form_group_box_resize)
        self.form_layout.addRow(self.form_group_box_time_crop)
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
        self.src_file_name = file_name[0]
        src_file_name_split = os.path.splitext(self.src_file_name)
        self.dest_file_name = src_file_name_split[0]+"-out"+src_file_name_split[1]
        self.form_edit_target_file_name.setText(self.src_file_name)
        cmd = f'ffprobe -v error -show_entries stream=width,height,duration -of default=noprint_wrappers=1:nokey=1 -i {file_name[0]}'
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result_parse = result.stdout.split('\n')
        self.input_file_width = int(result_parse[0])
        self.input_file_height = int(result_parse[1])

        duration = int(float(result_parse[2]))
        
        self.form_spin_from_time_crop.setValue(0)

        self.form_spin_to_time_crop.setMaximum(duration)
        self.form_spin_to_time_crop.setValue(duration)


        hours = int(duration / 3600)
        duration -= hours * 3600
        minutes = int(duration / 60)
        seconds = duration - (minutes * 60)

        self.form_edit_src_width.setText(str(self.input_file_width))
        self.form_edit_dest_width.setText(str(self.input_file_width))
        self.form_edit_src_height.setText(str(self.input_file_height))
        self.form_edit_dest_height.setText(str(self.input_file_height))

    def form_spin_time_crop_valueChanged(self, value):
        self.form_spin_from_time_crop.setMaximum(self.form_spin_to_time_crop.value() - 1)
        self.form_spin_to_time_crop.setMinimum(self.form_spin_from_time_crop.value() + 1)

    def form_spin_time_crop_textFromValue(self, value):
        pass
    # endregion Functions

# Основная программа
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())