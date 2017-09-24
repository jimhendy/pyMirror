from PyQt5 import QtWidgets, QtCore
from Apps import baseApp
import os
import re
import pandas as pd

class Mail( baseApp.baseApp ):
    
    def __init__(self, mainWindow):
        super().__init__('Mail', mainWindow)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.regExprFrom = re.compile('\\nFrom: (.+?) <(.+?)>\\n')
        self.regExprSubject = re.compile('\\nSubject\: (.+?)\\n')
        self.regExprDate = re.compile('\\nDate\: (.+?)\\n')
        self.newEmailDir = '/home/jim/mail/new/'
        pass

    def update(self, updateCount):

        # Only update every 3 minutes
        if updateCount % ( 60. * 3 ) != 0:
            return

        os.system( '/home/jim/bin/GetMail.sh' )
        emailFiles = sorted(os.listdir( self.newEmailDir ))
        text = self.normalTextStr + '\'>'

        data = []
        for eF in emailFiles:
            fileText = ''.join(open( self.newEmailDir + eF ).readlines())
            fromMatches = self.regExprFrom.search( fileText )

            shortName = self.get_short_name( fromMatches )
            if shortName is None:
                continue
            subjectMatches = self.regExprSubject.search( fileText )
            dateMatches = self.regExprDate.search( fileText )
            date = pd.to_datetime( dateMatches.group(1).split('+')[0] )
            data.append(
                {'Name':shortName,                 
                 'Message':subjectMatches.group(1),
                 'Date':date
             }
            )
            pass
        if not len(data):
            text = 'No Mail'
        else:
            df = pd.DataFrame( data )
            df.sort_values( 'Date', ascending=True )
            for i in range(len(df)):
                text += df.iloc[i].Name + ' - ' + df.iloc[i].Message + '<br/>'
                pass
            text += '</span>'
            pass
        self.label.setText(text)
        pass

    def get_short_name( self, fromMatches ):
        try:
            email = fromMatches.group(2).lower()
            if 'jimhendy' in email:
                return 'Jim'
            elif 'alison' in email:
                return 'Ali'
            elif 'evertonfc87' in email:
                return 'Ali'
            else:
                return fromMatches.group(1)
        except:
            return 'None'
        
        
        
