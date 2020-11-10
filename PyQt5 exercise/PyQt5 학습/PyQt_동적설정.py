import sys
import os
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic


class CenterPanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent
        self.data = QTableWidget()  # construct TableWidget
        self.data.setColumnCount(2)  # set columns and column labels
        self.data.setHorizontalHeaderLabels(('P', 'T'))
        self.btn = QPushButton('Plot')  # button to populate QTableBox
        self.btn.clicked.connect(self.plot)
        vbx_Data = QVBoxLayout()  # Create vertical box layout to hold table
        vbx_Data.setTitle('Data')
        vbx_Data.addWidget(self.data)  # Add table to box layout
        vbx_Data.addWidget(self.btn)  # Add button to box layout
        self.setLayout(vbx_Data)

    def plot(self):
        # dataframe with 2 columns and n rows
        df = pd.DataFrame((some_Data), ('z', 'T'))
        self.data.setRowCount(len(df))
        # Enter data onto Table
        for n, value in enumerate(df['z']):  # loop over items in first column
            self.data.setItem(n, 0, QTableWidgetItem(str(value)))
            print(n)
            print(value)
        for n, value in enumerate(df['T']):  # loop over items in second column
            self.data.setItem(n, 1, QTableWidgetItem(str(value)))
            print(n)
            print(value)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Plotting')
        WinLeft = 150
        WinTop = 150
        WinWidth = 1100
        WinHight = 800
        self.setGeometry(WinLeft, WinTop, WinWidth, WinHight)
        self.CenterPane = CenterPanel(self)
        self.setCentralWidget(self.CenterPane)
        self.setStyle(QStyleFactory.create('Cleanlooks'))


if __name__ == "__main__":
    MainThred = QApplication([])
    MainGui = MainWindow()
    MainGui.setFocus()
    MainGui.show()
    sys.exit(MainThred.exec_())
