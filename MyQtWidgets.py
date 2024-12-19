# -*- coding: utf-8 -*-

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
    
    def valueFromText(self, text):
        pass
        return 100