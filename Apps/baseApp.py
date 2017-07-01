from PyQt5 import QtWidgets, QtCore

class baseApp( object ):

    def __init__(self, appName, mainWindow):

        self.appName = appName
        self.mainWindow = mainWindow
        self.label = QtWidgets.QLabel(appName, self.mainWindow)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        #font-variant:Small-Caps;
        self.label.setStyleSheet('color: white;  font-weight:bold; font-family:Times')
        self.smallTextStr = "<span style='font-size:13pt; "
        self.normalTextStr = "<span style='font-size:15pt; "
        self.largerTextStr = "<span style='font-size:25pt; "
        self.largeTextStr = "<span style='font-size:32pt; "
        pass


    def update(self, updateCount):
        pass
        
