from PyQt5 import QtWidgets, QtCore
from Apps import baseApp
import os
import re

class Mail( baseApp.baseApp ):
    
    def __init__(self, mainWindow):
        super().__init__('Mail', mainWindow)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.regExprFrom = re.compile('\\nFrom: (.+?) <(.+?)>\\n')
        self.regExprSubject = re.compile('\\nSubject\: (.+?)\\n')
        self.newEmailDir = '/home/jim/mail/new/'
        pass

    def update(self, updateCount):

        # Only update every 3 minutes
        if updateCount % ( 60. * 3 ) != 0:
            return

        os.system( '/home/jim/bin/GetMail.sh' )
        emailFiles = sorted(os.listdir( self.newEmailDir ))
        text = self.normalTextStr + '\'>'
        
        for eF in emailFiles:
            fileText = ''.join(open( self.newEmailDir + eF ).readlines())
            fromMatches = self.regExprFrom.search( fileText )
            subjectMatches = self.regExprSubject.search( fileText )
            shortName = self.get_short_name( fromMatches )
            if shortName is None:
                continue            
            text += shortName + ' - ' + subjectMatches.group(1) + '<br/>'
            pass
        self.label.setText(text)
        pass

    def get_short_name( self, fromMatches ):

        email = fromMatches.group(2).lower()
        if 'jimhendy' in email:
            return 'Jim'
        elif 'alison' in email:
            return 'Ali'
        elif 'evertonfc87' in email:
            return 'Ali'
        else:
            return fromMatches.group(1)
        
        
        
