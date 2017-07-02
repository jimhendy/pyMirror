from PyQt5 import QtWidgets, QtCore
from Apps import baseApp
import pandas as pd
import datetime
import re

class Sports( baseApp.baseApp ):
    
    def __init__(self, mainWindow):
        super().__init__('Sports', mainWindow)
        self.baseUrl = 'http://www.wheresthematch.com/tv/home.asp?'
        self.teams = {
            3:['Glasgow','Scotland','Munster','Ireland','British and Irish Lions'],
            1:['Everton']
        }
        self.columns = ['0','Teams','1','DateTime','Competition','Channel']
        self.regExpr = re.compile('^(.+?) v (.+?) Live Stream  (.+?) at (.+?) on (.+?)$')
        
        pass

    def update(self, updateCount):

        # Only update every hour
        if updateCount % ( 60. * 60 ) != 0:
            return
        
        now = datetime.datetime.today()
        todayStr = now.strftime('%Y%m%d')
        nextWeekStr = ( now + pd.tseries.offsets.DateOffset( days=7 ) ).strftime('%Y%m%d')

        data = []
        for sportId, myTeams in self.teams.items():
            url = self.baseUrl + 'showdatestart=%s&showdateend=%s&sportid=%i' % (todayStr, nextWeekStr, sportId )
            dfs = pd.read_html( url )
            if not len(dfs) == 1:
                print('Problem getting sport data for sportId: %i' % sportId )
                print('Attempted url: %s' % url )
                pass
            df = dfs[0]
            df.columns = self.columns
            df.dropna( subset=['Channel','Teams'], inplace=True )
            for myTeam in myTeams:
                dfSub = df[ df.Teams.str.contains( myTeam ) ]
                for i in range(len(dfSub)):
                    matches = self.regExpr.search(dfSub.iloc[i].Teams)
                    if matches is None:
                        continue
                    data.append(
                        {'Team1':matches.group(1),
                         'Team2':matches.group(2),
                         'Day':matches.group(3),
                         'Time':matches.group(4),
                         'Channel':matches.group(5)
                        }
                    )
                    pass
                pass
            pass
        df = pd.DataFrame( data )
        df = df[['Team1','Team2','Day','Time','Channel']]
        text =  '''<style>.padding_df td { padding: 3px; }</style>'''
        text += df.to_html( index=False, header=False, classes="padding_df")
        self.label.setText( text )
        pass
