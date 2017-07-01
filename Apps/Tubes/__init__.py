from PyQt5 import QtWidgets, QtCore
from Apps import baseApp
import pandas as pd
import json
import requests

class Tubes( baseApp.baseApp ):
    
    def __init__(self, mainWindow):
        super().__init__('Tubes', mainWindow)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.df_colours = self.make_colour_df()
        pass

    
    def update(self, updateCount):

        # Only update tube status every 5 minutes
        if updateCount % ( 60. * 5 ) != 0:
            return

        status = self.get_tfl_status()

        if status is None:
            self.label.setText(
                self.normalTextStr + '\'>Good Service On All Lines</span>'
            )
            pass
        else:
            text = ''
            for i in range(len(status)):
                text += self.normalTextStr + ' color:' + status.iloc[i].colour + ';\' >'
                text += status.iloc[i].shortName + '</span>' + self.normalTextStr + ' color:white; \'> - '
                text += status.iloc[i].status + '</span><br/>'
                pass
            self.label.setText( text )
            pass       
        pass

    def add_colours(self, df):
        return df.merge( self.df_colours,
                         on='line', how='left')
    


    def make_colour_df(self):
        data = [
            {'line':'Hammersmith & City', 'colour':'rgb(251,153,175)', 'shortName':'H&C'},
            {'line':'Circle', 'colour':'rgb(255, 206, 0)', 'shortName':'C'},
            {'line':'District', 'colour':'rgb( 0, 114, 41 )', 'shortName':'D'},
            {'line':'London Overground', 'colour':'rgb( 232, 106, 16)', 'shortName':'O'},
            {'line':'Jubilee', 'colour':'rgb( 134, 143, 152 )', 'shortName':'J'},
            {'line':'Piccadilly', 'colour':'rgb( 0, 25, 168 )', 'shortName':'P'},
            {'line':'Bakerloo', 'colour':'rgb( 137, 78, 36 )', 'shortName':'B'},
            {'line':'Central', 'colour':'rgb( 220, 36, 31 )', 'shortName':'C'},
            {'line':'Metropolitan', 'colour':'rgb( 117, 16, 86 )', 'shortName':'M'},
            {'line':'Victoria', 'colour':'rgb( 0, 160, 226)', 'shortName':'V'},
            {'line':'Waterloo', 'colour':'rgb( 118, 208, 189 )', 'shortName':'W&C'},
            {'line':'DLR', 'colour':'rgb( 0, 175, 173 )', 'shortName':'DLR'},
            {'line':'Northern', 'colour':'rgb(255,255,255)', 'shortName':'N'}
        ]
        df = pd.DataFrame( data, index=range(len(data)) )
        return df
        
        
    
    def get_tfl_status(self):
        send_url = 'https://api.tfl.gov.uk/line/mode/tube,overground,dlr/status'
        requestData = requests.get(send_url)
        jsonData = json.loads(requestData.text)

        data = []
        for line in jsonData:
            lineName = line['name']
            lineStatuses = [line['lineStatuses'][k]['statusSeverityDescription'] for k in range(len(line['lineStatuses']))]
            for s in lineStatuses:
                if s != 'Good Service':
                    data.append( {'line': lineName, 'status': s} )
                    pass
                pass
            pass
        
        if not len(data):
            return None
        
        df = pd.DataFrame( data, index=range(len(data)) )
        df.sort_values( ['line','status'], inplace=True )
        df.drop_duplicates( 'line', inplace=True )
        return self.add_colours(df)
        
                
