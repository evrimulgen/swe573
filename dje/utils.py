
"""
Utilities for Sentiolytics Frontend
"""

import urllib2
import django.utils.simplejson as json

def service_request(id, data):
    url = "http://sentios.cloudapp.net/api/%s" % id
    if data:
        d = json.dumps(data)
        try:
            result = urllib2.urlopen(url,d)
            j_obj = json.loads(result.read())
            list_data = j_obj["data"]
            return list_data
        except:
            empty = []
            return empty

def tryService():
    colorDict = []
    colorList = service_request("GetTeamColors", {"homeid": 1, "awayid": 2})
    colorDict = {'homeFill': colorList["homefill"], 'homeStroke': colorList["homestroke"], 'awayFill': colorList["awayfill"], 'awayStroke': colorList["awaystroke"]}

    print colorDict

tryService()

