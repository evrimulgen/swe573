"""
Util functions for Stat Center
"""

import urllib2
from django.utils import simplejson as json


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

def prune_dicts(fields, idict):
    """
    Method for choosing only certain fields from a list of dicts.

    :param fields: a list of strings (field names) to filter for
    :param idict: the dictionary to be pruned
    """
    res = []
    for k in idict:
        res.append([k[key] for key in fields])

    res = sorted(res, key=lambda x: x[1], reverse=True)
    return res

def prune_lists(ices, ilist):
    """
    Method for choosing only certain indices from a list of lists.

    :param ices: a list of integers, corresponding to indices
    :param ilist: a list of lists, to be pruned
    """
    res = []
    for i in ilist:
        if i[0] != 0:
            res.append([i[x] for x in ices])

    return res