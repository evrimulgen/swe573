
"""
Utilities for Sentiolytics Frontend
"""

import urllib2
from datetime import datetime
import django.utils.simplejson as json
import pytz

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

def calc_match_minute(stamp_str, status):
    """
    Calculate the match minute of the match,

    :param status: match status id as given by BroadAge
    :param stamp_str: a timestamp string as returned by CUR_TIMESTAMP field in the MSSQL database
    """

    tdelta = None
    if status is None:
        return tdelta

    status = int(status)
    istanbul = pytz.timezone('Europe/Istanbul')
    if not stamp_str:
        return tdelta

    stamp_str = stamp_str.split(".")[0]
    db_time = datetime.strptime(stamp_str, '%Y-%m-%d %H:%M:%S')
    db_time = istanbul.localize(db_time)
    rl_time = datetime.now(istanbul)
    if status == 2:
        tdelta = rl_time - db_time
        tdelta = str(tdelta.seconds//60 + 1)
    elif status == 3:
        tdelta = rl_time - db_time
        tdelta = str(tdelta.seconds//60 + 45 + 1)
    elif status == 10:
        tdelta = "DA"

    return tdelta

