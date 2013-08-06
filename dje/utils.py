
"""
Utilities for Sentiolytics Frontend
"""

import urllib2
import django.utils.simplejson as json

def service_request(id, data):
    url = "http://sentio.cloudapp.net:8080/api/%s" % id
    if data:
        d = json.dumps(data)
        result = urllib2.urlopen(url,d)
    return result.read()


def try_service():
    data = {"leagueId":1,"seasonId":8918,"teamId":3,"type":0,"weekid":24}
    print service_request("GetTeamForm", data)


try_service()