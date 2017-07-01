from PyQt5 import QtWidgets, QtCore
from Apps import baseApp

class Tubes( baseApp.baseApp ):
    
    def __init__(self, mainWindow):
        super().__init__('Tubes', mainWindow)
        self.xGrid = 4
    
