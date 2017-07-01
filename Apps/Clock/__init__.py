from PyQt5 import QtWidgets, QtCore
from Apps import baseApp
import datetime

class Clock( baseApp.baseApp ):
    
    def __init__(self, mainWindow):
        super().__init__('Clock', mainWindow)
        
        self.xGrid = 2

    def update(self, updateCount):
        now = datetime.datetime.today()
        time = now.strftime('%H:%M')
        date = now.strftime('%-d - %b - %Y')
        day = now.strftime('%A')
        text = self.largeTextStr + "'> " + time + "</span><br/>"
        text += self.normalTextStr + "'> " + date + "<br/>"
        text += day + "</span>"
        self.label.setText( text )
        pass
        
