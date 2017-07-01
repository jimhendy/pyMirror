import requests
import json

class Utils( object ):



    def __init__(self):
        self.location = None
        pass

    def get_location(self):
        if self.location is None:
            send_url = 'http://freegeoip.net/json'
            r = requests.get(send_url)
            j = json.loads(r.text)
            lat = j['latitude']
            lon = j['longitude']
            self.location = (lat, lon)
            pass
        return self.location
