from PyQt5 import QtWidgets, QtCore

class baseApp( object ):

    def __init__(self, appName, mainWindow):

        self.appName = appName
        self.mainWindow = mainWindow
        self.label = QtWidgets.QLabel(appName, self.mainWindow)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet('color: white; font-variant:Small-Caps; font-weight:bold; font-family:serif')
        
        # "<span style='font-size:18pt; font-weight:600; color:#aa0000;'>text1</span><span style='font-size:10pt; font-weight:600; color:#00aa00;'>text2</span>"
        self.xGrid = 0
        self.yGrid = 0

        self.normalTextStr = "<span style='font-size:18pt; "
        self.largeTextStr = "<span style='font-size:32pt; "
        
        pass


    def update(self):
        pass
        
