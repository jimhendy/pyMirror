from .MainWindow import MainWindow
from PyQt5 import QtWidgets, QtCore
import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = MainWindow(app)
MainWindow.showFullScreen()
app.setOverrideCursor(QtCore.Qt.BlankCursor);
sys.exit(app.exec_())
    
