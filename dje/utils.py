
"""
Utilities for Sentiolytics Frontend
"""

import urllib2
import django.utils.simplejson as json

def service_request(id, data):
    url = "http://sentio.cloudapp.net:8080/api/%s" % id
    if data:
        d = json.dumps(data)
        try:
            result = urllib2.urlopen(url,d)
            j_obj = json.loads(result.read())
            list_data = j_obj["data"]
            return list_data
        except:
            return []

