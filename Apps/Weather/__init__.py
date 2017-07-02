# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from Apps import baseApp
import pyowm
import json

class Weather( baseApp.baseApp ):
    
    def __init__(self, mainWindow):
        super().__init__('Weather', mainWindow)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.location = self.mainWindow.utils.get_location()
        self.apiKey = 'bdfb08a582089b5e61de0fe0aa19b606'
        self.owm = pyowm.OWM(self.apiKey)
        pass

    def get_new_forecast(self):
        weather = self.owm.daily_forecast_at_coords(
            self.location[0],
            self.location[1],
            1
        ).get_forecast()
        return json.loads( weather.to_JSON() )

    def get_current_temperature(self):
        weather = self.owm.weather_around_coords(
            self.location[0],
            self.location[1],
            1
        )[0]
        j = json.loads( weather.to_JSON() )
        return self.to_celcius( j['Weather']['temperature']['temp'] )
    
    def update(self, updateCount):
        return
        # Only update the weather every half hour
        if updateCount % ( 60. * 30 ) != 0:
            return

        weather = self.get_new_forecast()

        # Note the weather location
        text = self.largerTextStr + "'> "
        text += weather['Location']['name'] + ', ' + weather['Location']['country']
        text += '</span><br/>'
        weather = weather['weathers'][0]
        
        # Add icon and current temp.
        text += self.largerTextStr + "display:block; vertical-align: middle; '> "
        text += "<img margin=\"-50px 0px\" src='WeatherSymbols/"
        text += weather['weather_icon_name'] + ".png'></img>"
        text += self.get_current_temperature() + "</span><br/>"

        # Add Max/Min temp.s
        text += self.smallTextStr + "'> "
        text += '▲' + self.to_celcius(weather['temperature']['max'])
        text += ' ▼' + self.to_celcius(weather['temperature']['min'])
        text += '<br/>'

        # Add wind details
        text += self.get_wind_direction_icon(weather)
        text += ' %.1f mph<br/>' % weather['wind']['speed']

        # Add rain details    
        text += self.add_rain(weather)
        text += '</span>'

        self.label.setText( text )
        pass
    
    def add_rain(self, weather):
        symbol = '☔'
        if 'all' in weather['rain'].keys():
            return  '%s %i mm' % (
                symbol,
                int(float(weather['rain']['all']) * 100.)
            )
        else:
            return '%s 0 mm' % symbol
        pass
    
    def to_celcius(self, value):
        absZero = 273.15
        return '%i°C' % int(float(value) - absZero)

    def get_wind_direction_icon(self, weather):
        direction = int(weather['wind']['deg'])
        arrows = ['↗','→','↘','↓','↙','←','↖','↑']

        step = 22.5
        minDeg = 22.5

        for i in range(len(arrows)):
            if i == len(arrows):
                return arrows[-1]
            elif (
                    direction > minDeg
                    and
                    direction <= (minDeg + 2. * step)
            ) :
                return arrows[i]
            minDeg += ( 2. * step )
        pass
