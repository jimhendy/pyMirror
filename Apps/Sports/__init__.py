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
            3:['Glasgow','Scotland','Munster','Ireland','British and Irish Lions','Edinburgh'],
            1:['Everton']
        }
        self.columns = ['0','Teams','1','DateTime','Competition','Channel']
        self.regExpr = re.compile('^(.+?) v (.+?)  (.+?) at (.+?) on (.+?)$')
        self.dayStrings = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
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
            print(url)
            dfs = pd.read_html( url )
            if not len(dfs) == 1:
                print('Problem getting sport data for sportId: %i' % sportId )
                print('Attempted url: %s' % url )
                pass
            df = dfs[0]
            df.columns = self.columns
            df.dropna( subset=['Channel','Teams'], inplace=True )
            for i in range(len(df)):
                matches = self.regExpr.search(df.iloc[i].Teams)
                if matches is None:
                    continue
                if any(myTeam in matches.group(i) for myTeam in myTeams for i in (1,2) ):
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
        if not len(data):
            self.label.setText( 'No Upcoming Matches' )
            pass
        else:
            df = pd.DataFrame( data ).drop_duplicates()
            df = df[['Team1','Team2','Day','Time','Channel']]
            df.loc[:,'TimeInt'] = ( df.Time.str.split(":").str[0] ).astype(int)
            for i,d in enumerate(self.dayStrings):
                df.loc[ df.Day == d ,'DayNum'] = i
                pass
            df.sort_values( ['DayNum','TimeInt'], ascending=True, inplace=True )
            del df['DayNum']
            del df['TimeInt']
            df.loc[ df.Channel.str.contains('televised'), 'Channel' ] = 'Not on TV'
            text =  '''<style>.padding_df td { padding: 3px; }</style>'''
            text += df.to_html( index=False, header=False, classes="padding_df")
            self.label.setText( text )
            pass
        pass
