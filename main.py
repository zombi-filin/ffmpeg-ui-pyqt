# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot
import PySide6.QtWidgets as QT
from __feature__ import snake_case, true_property
import sys

# Main window class
class MyWindow(QT.QWidget):
    def __init__(self):
        QT.QWidget.__init__(self)

# Main
if __name__ == '__main__':
    app = QT.QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())