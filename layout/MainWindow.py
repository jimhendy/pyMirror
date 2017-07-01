from PyQt5 import QtWidgets, QtCore, QtGui
from Apps import Weather, Clock, Tubes

class MainWindow( QtWidgets.QMainWindow ):

    def __init__(self):

        super().__init__()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)        
        self.setup_apps()
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.set_black_background()
        self.timer = QtCore.QTimer(self.centralWidget)
        self.timer.timeout.connect(self.update_apps)
        self.timer.start(500)
        self.centralWidget.setLayout(self.gridLayout)


    def set_black_background(self):
        self.pallette = self.palette()
        self.pallette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(self.pallette)

    def setup_apps(self):
        self.apps = {}
        self.apps['Weather'] = Weather.Weather( self.centralWidget )
        self.apps['Clock'] = Clock.Clock( self.centralWidget )
        self.apps['Tubes'] = Tubes.Tubes( self.centralWidget )

        [ self.gridLayout.addWidget(a.label, a.yGrid, a.xGrid) for k,a in self.apps.items() ]

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        

    def update_apps(self):
        [ a.update() for k,a in self.apps.items() ]
        return 1
