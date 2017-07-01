from PyQt5 import QtWidgets, QtCore, QtGui
from Apps import Weather, Clock, Tubes
from Utils import Utils

class MainWindow( QtWidgets.QMainWindow ):

    def __init__(self):

        super().__init__()
        self.utils = Utils()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        
        #self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)        
        self.setup_apps()
        #self.gridLayout.setColumnStretch(1, 1)
        #self.gridLayout.setColumnStretch(2, 1)
        #self.gridLayout.setRowStretch(1, 1)
        self.set_black_background()
        self.timer = QtCore.QTimer(self.centralWidget)
        self.timer.timeout.connect(self.update_apps)
        self.timer.start(500)
        self.updateCount = 0
        self.centralWidget.setLayout(self.verticalLayout)


    def set_black_background(self):
        self.pallette = self.palette()
        self.pallette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(self.pallette)

    def setup_apps(self):
        self.apps = {}
        self.apps['Weather'] = Weather.Weather( self )
        self.apps['Clock'] = Clock.Clock( self )
        self.apps['Tubes'] = Tubes.Tubes( self )

        self.topHorLayout = QtWidgets.QHBoxLayout()
        self.topHorLayout.addWidget( self.apps['Weather'].label )
        self.topHorLayout.addStretch(0.5)
        self.topHorLayout.addWidget( self.apps['Clock'].label )
        self.topHorLayout.addStretch(0.5)
        self.topHorLayout.addWidget( self.apps['Tubes'].label )

        self.verticalLayout.addLayout( self.topHorLayout )
        self.verticalLayout.addStretch(1)
        
        self.bottomHorLayout = QtWidgets.QHBoxLayout()
        #self.bottomHorLayout.addWidget( self.apps['Clock'].label )

        self.verticalLayout.addLayout( self.bottomHorLayout )

        #[ self.gridLayout.addWidget(a.label, a.yGrid, a.xGrid) for k,a in self.apps.items() ]
 
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        

    def update_apps(self):
        [ a.update(self.updateCount) for k,a in self.apps.items() ]
        self.updateCount += 1
        return 1
