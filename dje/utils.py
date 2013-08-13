
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
    data = {"league_id":1,"season_id":8918,"count":1}
    print service_request("GetBestAssisters", data)


try_service()