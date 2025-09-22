# -*- coding: utf-8 -*-

from MyQtWidgets import *
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *

import io
import json
import os
import re
import subprocess
import sys
import threading
import time

VERSION = '0.0.1'

RESIZE_EDIT_WIDTH = 50
CROP_TIME_SPIN_WIDTH = 70

def timeToSec(text:str):
    '''
    Функция возвращает количество секунд из строки вида 00:00:00
    '''
    text_split = text.split(':')
    return (int(text_split[0]) * 3600 ) + (int(text_split[1]) * 60) + int(text_split[2])

# Класс основного меню
class MainWindow(QMainWindow):
    
    # region Init
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'FFmpeg PyQT {VERSION}')
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        self.src_file_name = ''

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
        self.form_edit_dest_width.editingFinished.connect(self.form_edit_dest_width_editingFinished)

        self.form_edit_src_height = QLineEdit(parent=self, readOnly=True)
        self.form_edit_src_height.setFixedWidth(RESIZE_EDIT_WIDTH)
        self.form_edit_dest_height = QLineEdit(parent=self, maxLength=4)
        self.form_edit_dest_height.setFixedWidth(RESIZE_EDIT_WIDTH)
        self.form_edit_dest_height.editingFinished.connect(self.form_edit_dest_height_editingFinished)
        
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
        
        self.form_spin_from_time_crop = QTimeSpinBox()
        self.form_spin_from_time_crop.setMinimum(0)
        self.form_spin_from_time_crop.setMaximum(0)
        self.form_spin_from_time_crop.setFixedWidth(CROP_TIME_SPIN_WIDTH)
        self.form_spin_from_time_crop.valueChanged.connect(self.form_spin_time_crop_valueChanged)
        self.form_spin_from_time_crop.textChanged.connect(self.form_spin_time_crop_textChanged)


        self.form_spin_to_time_crop = QTimeSpinBox()
        self.form_spin_to_time_crop.setMinimum(0)
        self.form_spin_to_time_crop.setMaximum(0)
        self.form_spin_to_time_crop.setFixedWidth(CROP_TIME_SPIN_WIDTH)
        self.form_spin_to_time_crop.valueChanged.connect(self.form_spin_time_crop_valueChanged)
        self.form_spin_to_time_crop.textChanged.connect(self.form_spin_time_crop_textChanged)
        # self.form_spin_to_time_crop.keyPressEvent()

        self.form_layout_time_crop = QHBoxLayout()
        self.form_layout_time_crop.addWidget(self.form_spin_from_time_crop)
        self.form_layout_time_crop.addSpacing(32)
        self.form_layout_time_crop.addWidget(self.form_spin_to_time_crop)
        self.form_layout_time_crop.addStretch(1)

        self.form_group_box_time_crop = QGroupBox('Обрезка по времени')
        self.form_group_box_time_crop.setCheckable(True)
        self.form_group_box_time_crop.setChecked(False)
        self.form_group_box_time_crop.setLayout(self.form_layout_time_crop)
        # endregion

        #region Пуск
        self.form_button_start = QPushButton(text='Пуск', parent=self)
        self.form_button_start.setEnabled(False)
        self.form_button_start.clicked.connect(self.form_button_start_click)
        self.form_label_message = QLabel(text='Ожидание', parent=self)
        self.form_layout_start = QHBoxLayout()
        self.form_layout_start.addWidget(self.form_button_start)
        self.form_layout_start.addWidget(self.form_label_message)
        self.form_layout_start.addStretch(1)
        #endregion

        # region Mainform
        self.form_layout = QFormLayout()
        self.form_layout.addRow(self.form_group_box_target)
        self.form_layout.addRow(self.form_group_box_resize)
        self.form_layout.addRow(self.form_group_box_time_crop)
        self.form_layout.addRow(self.form_layout_start)
        # endregion Mainform

        # region Container 
        container = QWidget()
        container.setLayout(self.form_layout)
        self.setCentralWidget(container)
        # endregion Container

    # endregion Init

    # region Functions
    def form_button_target_open_click(self):
        if self.src_file_name == '':
            open_dir = os.path.dirname(__file__)
        else:
            open_dir = os.path.dirname(self.src_file_name)
        file_name = QFileDialog.getOpenFileName(self, 'Файл для конвертации', open_dir, 'Видео файл (*.avi *.mov *.mp4 *.m4a *.3gp *.3g2 *.mj2 *.mpeg)')
        
        self.src_file_name = file_name[0]
        self.form_edit_target_file_name.setText(self.src_file_name)
        
        command = f'ffprobe -v quiet -print_format json -show_format -show_streams -i "{file_name[0]}"'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result_json = json.loads(result.stdout)
        
        duration = int(float(result_json['format']['duration']))
        for stream in result_json['streams']:
            if stream['codec_type'] != 'video':
                continue
            self.input_file_width = int(float(stream['width']))
            self.input_file_height = int(float(stream['height']))
        
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
        
        self.form_button_start.setEnabled(True)

    def form_edit_dest_height_editingFinished(self):
        try:
            dest_height = int(self.form_edit_dest_height.text())
        except ValueError:
            self.form_edit_dest_height.setText(str(self.input_file_height))
        self.form_edit_dest_width.setText(str(int((dest_height * self.input_file_width) / self.input_file_height)))

    def form_edit_dest_width_editingFinished(self):
        try:
            dest_width = int(self.form_edit_dest_width.text())
        except ValueError:
            self.form_edit_dest_width.setText(str(self.input_file_width))
        self.form_edit_dest_height.setText(str(int((dest_width * self.input_file_height) / self.input_file_width)))

    def form_spin_time_crop_valueChanged(self, value):
        self.form_spin_from_time_crop.setMaximum(self.form_spin_to_time_crop.value() - 1)
        self.form_spin_to_time_crop.setMinimum(self.form_spin_from_time_crop.value() + 1)
    
    def form_spin_time_crop_textChanged(self, value):
        pass
    
    def processed(self):
        src_file_name_split = os.path.splitext(self.src_file_name)
        dest_file_name = src_file_name_split[0] + '-out-' + str(int(time.time())) + src_file_name_split[1]
        self.form_button_start.setEnabled(False)
        
        if self.form_group_box_resize.isChecked() or self.form_group_box_time_crop.isChecked():
            self.form_label_message.setText('Начали')
            command = f'ffmpeg '
            if self.form_group_box_time_crop.isChecked():
               command += f'-ss {self.form_spin_from_time_crop.text()} '
               command += f'-to {self.form_spin_to_time_crop.text()} '
            
            command += f' -i "{self.src_file_name}" '
            
            if self.form_group_box_resize.isChecked():
                dest_width = self.form_edit_dest_width.text()
                dest_height = self.form_edit_dest_height.text()

                command += f' -vf "scale={dest_width}:{dest_height}" '

            command += f'-progress pipe:1 "{dest_file_name}"'
            
            sec_len = timeToSec(self.form_spin_to_time_crop.text()) - timeToSec(self.form_spin_from_time_crop.text())
            regex = r'out_time=(.+)\.'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

            for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
                if 'out_time=' in line:
                    matches = re.findall(regex,line)
                    progress = int((timeToSec(matches[0]) / sec_len) * 100)
                    self.form_label_message.setText(f'Обработка: {progress}%')

            self.form_label_message.setText('Готово')
        self.form_button_start.setEnabled(True)

    def form_button_start_click(self):
        th = threading.Thread(target = self.processed)
        th.start()
    # endregion Functions

# Основная программа
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())