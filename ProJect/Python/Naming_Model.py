import sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np
from keras.models import load_model
Naming_Model_Dialog_ui = '../_uiFiles/Model_Save.ui'


class Naming_Model_Dialog(QDialog):
    def __init__(self, parent):
        super(Naming_Model_Dialog, self).__init__(parent)
        uic.loadUi(Naming_Model_Dialog_ui, self)
        # test = ARIMAResults.load('../save/test_model.h5')
        self.model = parent.model
        self.show()
        self.save_pushButton.clicked.connect(self.Save)

    def Save(self):
        # path = '../save/'
        file_name = self.Model_Name.text()
        # path_file_name = path + file_name

        self.model.save(f"../save/{file_name}.h5")
        QMessageBox.about(self, "Alert", "저장되었습니다.")
        self.close()
