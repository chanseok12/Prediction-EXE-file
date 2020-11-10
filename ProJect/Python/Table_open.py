import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TableWidgetWindow(QMainWindow):
    def __init__(self, parent):
        super(TableWidgetWindow, self).__init__(parent)
        self.data = parent.data
        self.r = parent.r
        self.c = parent.c
        self.setupUI(self.data, self.r, self.c)

    def setupUI(self, data, r, c):
        self.tableWidget.setRowCount(r)
        self.tableWidget.setColumnCount(c)

        for i in range(r):
            for j in range(c):
                self.table.setItem(
                    i, j, QTableWidgetItem(str(data.iloc[i, j])))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)