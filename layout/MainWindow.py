from PyQt5 import QtWidgets, QtCore, QtGui
from Apps import Weather, Clock, Tubes, Sports, Mail
from Utils import Utils

class MainWindow( QtWidgets.QMainWindow ):

    def __init__(self, app):

        super().__init__()

        self.application = app
        self.desktop = app.desktop()
        self.center = self.desktop.screen().rect().center()
        
        self.utils = Utils()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        #self.verticalLayout.setContentsMargins( 30, 20, 50, 20 )
        self.setup_apps()
        self.set_black_background()
        self.timer = QtCore.QTimer(self.centralWidget)
        self.timer.timeout.connect(self.update_apps)
        self.timer.start(1000)
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
        self.topHorLayout.addWidget( self.apps['Clock'].label )
        self.topHorLayout.addWidget( self.apps['Tubes'].label )
        self.topHorLayout.setAlignment( self.apps['Weather'].label, QtCore.Qt.AlignTop )
        self.topHorLayout.setAlignment( self.apps['Clock'].label, QtCore.Qt.AlignTop )
        self.topHorLayout.setAlignment( self.apps['Tubes'].label, QtCore.Qt.AlignTop )
        
        self.verticalLayout.addLayout( self.topHorLayout )
        self.verticalLayout.addStretch(1)

        self.apps['Sports'] = Sports.Sports( self )
        self.apps['Mail'] = Mail.Mail( self )
        self.bottomHorLayout = QtWidgets.QHBoxLayout()
        self.bottomHorLayout.addWidget( self.apps['Sports'].label )
        self.bottomHorLayout.addStretch(1)
        self.bottomHorLayout.addWidget( self.apps['Mail'].label )
        self.bottomHorLayout.setAlignment( self.apps['Sports'].label, QtCore.Qt.AlignBottom )
        self.bottomHorLayout.setAlignment( self.apps['Mail'].label, QtCore.Qt.AlignBottom )
        self.verticalLayout.addLayout( self.bottomHorLayout )
        pass
 
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        

    def update_apps(self):
        [ a.update(self.updateCount) for k,a in self.apps.items() ]
        self.updateCount += 1
        return 1
