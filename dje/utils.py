
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
    data = {"leagueId":1,"seasonId":8918,"matchId":11730060}
    teams = service_request("GetMatchNarration", data)
    j_obj = json.loads(teams)
    datalist = j_obj["data"]
    narrationDict = []
    for min in datalist:
        if min == "_id":
            print min
        else:
            x = "team"
            team_id = datalist[min][x]
            x = "typeInt"
            type_ = datalist[min][x]
            x = "text"
            text_ = datalist[min][x]
            print text_





try_service()