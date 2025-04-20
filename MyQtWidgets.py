# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class QTimeSpinBox(QSpinBox):
    def __init__(self, *args):
       QSpinBox.__init__(self, *args)
       self.setRange(0,0)

    def textFromValue(self, value):
        hours = int(value / 3600)
        value -= hours * 3600
        minutes = int(value / 60)
        seconds = value - (minutes * 60)
        return "%02d:%02d:%02d" % (hours,minutes,seconds)
    
    def keyPressEvent(self, event):
        editor = self.lineEdit()
        pos = editor.cursorPosition()
        if event.key() == Qt.Key.Key_Left and pos > 0:
            editor.setCursorPosition(pos - 1)
        elif event.key() == Qt.Key.Key_Right and pos < 8:
            editor.setCursorPosition(pos + 1)
        elif pos < 8:
            ev_text = event.text()
            if ev_text in ['0','1','2','3','4','5','6','7','8','9']:
                text = editor.text()
                text = text [:pos] + ev_text + text[pos+1:]
                if pos in [1,4]:
                    pos +=2
                else:
                    pos += 1
                editor.setText(text)
                editor.setCursorPosition(pos)
            if pos == 8:
                new_value = int(text[0] + text[1]) * 3600
                new_value += int(text[3] + text[4]) * 60
                new_value += int(text[6] + text[7])
                if (new_value >= self.minimum()) and (new_value <= self.maximum()):
                    self.setValue(new_value)
        event.ignore
        pass