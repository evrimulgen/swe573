# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from random import randint
from django.http import HttpRequest
import urllib2, urllib

def home(request):
    a = []
    for x in range(1, 35):
        a.append(x)

    b = []
    b.append({'teamId': int(1), 'teamName': 'Beşiktaş','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(58), 'change': int(1)})
    b.append({'teamId': int(2), 'teamName': 'Bursaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(55), 'change': int(-1)})
    b.append({'teamId': int(3), 'teamName': 'Eskişehirspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(8), 'points':int(46), 'change': int(2)})
    b.append({'teamId': int(4), 'teamName': 'Fenerbahçe','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(61), 'change': int(3)})
    b.append({'teamId': int(5), 'teamName': 'Galatasaray','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(71), 'change': int(-4)})
    b.append({'teamId': int(6), 'teamName': 'Gaziantepspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-7), 'points':int(46), 'change': int(0)})
    b.append({'teamId': int(7), 'teamName': 'Gençlerbirliği','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(45), 'change': int(1)})
    b.append({'teamId': int(8), 'teamName': 'İstanbul BŞB','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(36), 'change': int(1)})
    b.append({'teamId': int(9), 'teamName': 'KDÇ Karabükspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(40), 'change': int(1)})
    b.append({'teamId': int(10), 'teamName': 'Antalyaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(47), 'change': int(1)})
    b.append({'teamId': int(11), 'teamName': 'Akhisar Belediye','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(42), 'change': int(1)})
    b.append({'teamId': int(12), 'teamName': 'Sivasspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(44), 'change': int(1)})
    b.append({'teamId': int(13), 'teamName': 'S.B. Elazığspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(43), 'change': int(1)})
    b.append({'teamId': int(14), 'teamName': 'Orduspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(29), 'change': int(1)})
    b.append({'teamId': int(15), 'teamName': 'Mersin İY','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(22), 'change': int(1)})
    b.append({'teamId': int(16), 'teamName': 'Trabzonspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-1), 'points':int(46), 'change': int(1)})
    b.append({'teamId': int(17), 'teamName': 'Kasımpaşa','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(50), 'change': int(1)})
    b.append({'teamId': int(18), 'teamName': 'Kayserispor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(52), 'change': int(1)})

    c = []
    c.append({'teamId': int(18), 'playerId': int(13),'playerName':'Onur Kıvrak', 'jerseyNumber':int(1), 'rating':float(7.5), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'passTotalMatch' : int(14), 'passTotalLeague':float(13.2), 'passSuccessfulMatch':int(11), 'passSuccessfulLeague': float(8.3), 'savesMatch':int(11), 'savesLeague': float(8.3), '1on1TotalMatch':int(3), '1on1TotalLeague': float(2.8), '1on1SuccessfulMatch':int(3), '1on1SuccessfulLeague': float(1.7), 'concededMatch':int(0), 'concededLeague': int(18), 'penaltySaveMatch':int(0), 'penaltySaveLeague': int(3), 'playPosition': int(0)})
    c.append({'teamId': int(1), 'playerId': int(14),'playerName':'Tomas Sivok', 'jerseyNumber':int(3), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(2), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(5), 'playerId': int(15),'playerName':'Alber Riera', 'jerseyNumber':int(4), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(1), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(3), 'playerId': int(16),'playerName':'Jerry Akaminko', 'jerseyNumber':int(30), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(3), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(4), 'playerId': int(17),'playerName':'Gökhan Gönül', 'jerseyNumber':int(77), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(4), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(18), 'playerId': int(18),'playerName':'Olcan Adın', 'jerseyNumber':int(9), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(5), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(4), 'playerId': int(19),'playerName':'Emre Belözoğlu', 'jerseyNumber':int(25), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(6), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(2), 'playerId': int(20),'playerName':'Pablo Batalla', 'jerseyNumber':int(10), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(7), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(1), 'playerId': int(21),'playerName':'Filip Holosko', 'jerseyNumber':int(11), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(8), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(19), 'playerId': int(22),'playerName':'Kalu Uche', 'jerseyNumber':int(9), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(10), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    c.append({'teamId': int(5), 'playerId': int(23),'playerName':'Didier Drogba', 'jerseyNumber':int(14), 'rating':float(7.6), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'HIRMatch':int(113), 'HIRLeague':int(100), 'sprintMatch':int(40), 'sprintLeague':int(20), 'passTotalMatch' : int(25), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(11), 'goalMatch': int(0), 'goalLeague': int(9), 'assistMatch': int(1), 'assistLeague': int(11)})
    return render_to_response('statshome.html', {'weeklist': a, 'standing_list':b, 'best_eleven_list':c})

def team(request, num):
    from random import randint
    a =[]
    for x in range(1, 19):
        a.append(x)

#    post_data = [('name','Gladys'),]     # a sequence of two element tuples
#    result = urllib2.urlopen('http://example.com', urllib.urlencode(post_data))
#    content = result.read()

    post_data = '{"team_ids":["1"]}'
    result = urllib2.urlopen('http://sentio.cloudapp.net:8080/api/GetTeamsInformation', post_data)
    content = result.read()
    b = []
    b.append({'teamId': int(1), 'teamName': 'Beşiktaş','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(58), 'change': int(1)})
    b.append({'teamId': int(2), 'teamName': 'Bursaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(55), 'change': int(-1)})
    b.append({'teamId': int(3), 'teamName': 'Eskişehirspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(8), 'points':int(46), 'change': int(2)})
    b.append({'teamId': int(4), 'teamName': 'Fenerbahçe','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(61), 'change': int(3)})
    b.append({'teamId': int(5), 'teamName': 'Galatasaray','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(71), 'change': int(-4)})
    b.append({'teamId': int(6), 'teamName': 'Gaziantepspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-7), 'points':int(46), 'change': int(0)})
    b.append({'teamId': int(7), 'teamName': 'Gençlerbirliği','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(45), 'change': int(1)})
    b.append({'teamId': int(8), 'teamName': 'İstanbul BŞB','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(36), 'change': int(1)})
    b.append({'teamId': int(9), 'teamName': 'KDÇ Karabükspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(40), 'change': int(1)})
    b.append({'teamId': int(12), 'teamName': 'Antalyaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(47), 'change': int(1)})
    b.append({'teamId': int(11), 'teamName': 'Akhisar Belediye','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(42), 'change': int(1)})
    b.append({'teamId': int(17), 'teamName': 'Sivasspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(44), 'change': int(1)})
    b.append({'teamId': int(14), 'teamName': 'S.B. Elazığspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(43), 'change': int(1)})
    b.append({'teamId': int(15), 'teamName': 'Orduspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(29), 'change': int(1)})
    b.append({'teamId': int(13), 'teamName': 'Mersin İY','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(22), 'change': int(1)})
    b.append({'teamId': int(18), 'teamName': 'Trabzonspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-1), 'points':int(46), 'change': int(1)})
    b.append({'teamId': int(16), 'teamName': 'Kasımpaşa','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(50), 'change': int(1)})
    b.append({'teamId': int(10), 'teamName': 'Kayserispor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(52), 'change': int(1)})
    c = []
    for x in range(1, 35):
        match = randint(0,34)
        min = randint(0,12432)
        goal = randint(0,25)
        assist = randint(0,16)
        yellow = randint(0,8)
        red = randint(0,4)
        run = randint(0,11300)
        c.append({'jersey': "%s"%x, 'name': 'Serhat Kurtulus', 'match': int(match), 'min': int(min), 'goal': int(goal), 'assist': int(assist), 'yellow': int(yellow), 'red': int(red), 'run': int(run)})


    return render_to_response('statsteam.html', {'team_list': a, 'standing_list':b, 'team_selected': int(num), 'player_list':c})


def league(request):
    a =[]
    for x in range(1, 19):
        a.append(x)
    b = []
    b.append({'teamId': int(1), 'teamName': 'Beşiktaş','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(58), 'change': int(1)})
    b.append({'teamId': int(2), 'teamName': 'Bursaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(55), 'change': int(-1)})
    b.append({'teamId': int(3), 'teamName': 'Eskişehirspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(8), 'points':int(46), 'change': int(2)})
    b.append({'teamId': int(4), 'teamName': 'Fenerbahçe','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(61), 'change': int(3)})
    b.append({'teamId': int(5), 'teamName': 'Galatasaray','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(71), 'change': int(-4)})
    b.append({'teamId': int(6), 'teamName': 'Gaziantepspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-7), 'points':int(46), 'change': int(0)})
    b.append({'teamId': int(7), 'teamName': 'Gençlerbirliği','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(45), 'change': int(1)})
    b.append({'teamId': int(8), 'teamName': 'İstanbul BŞB','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(36), 'change': int(1)})
    b.append({'teamId': int(9), 'teamName': 'KDÇ Karabükspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(40), 'change': int(1)})
    b.append({'teamId': int(12), 'teamName': 'Antalyaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(47), 'change': int(1)})
    b.append({'teamId': int(11), 'teamName': 'Akhisar Belediye','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(42), 'change': int(1)})
    b.append({'teamId': int(17), 'teamName': 'Sivasspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(44), 'change': int(1)})
    b.append({'teamId': int(14), 'teamName': 'S.B. Elazığspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(43), 'change': int(1)})
    b.append({'teamId': int(15), 'teamName': 'Orduspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(29), 'change': int(1)})
    b.append({'teamId': int(13), 'teamName': 'Mersin İY','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(22), 'change': int(1)})
    b.append({'teamId': int(18), 'teamName': 'Trabzonspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-1), 'points':int(46), 'change': int(1)})
    b.append({'teamId': int(16), 'teamName': 'Kasımpaşa','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(50), 'change': int(1)})
    b.append({'teamId': int(10), 'teamName': 'Kayserispor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(52), 'change': int(1)})


    c = []
    for x in range(1, 35):
        c.append(x)

    return render_to_response('statsleague.html', {'weeklist': c , 'standing_list':b, 'team_list': a})


def before(request):
    return render_to_response('beforematch.html')
def center(request):
    return render_to_response('matchcenter.html', {'homeTeam': u"Fenerbahçe", 'awayTeam': u"Galatasaray", 'stadiumName': u"ŞÜKRÜ SARAÇOĞLU STADI", 'homeLogo': "images/logo4.png", 'awayLogo':"images/logo5.png"})
def summary(request):
    return render_to_response('matchsummary.html')
def player(request):
    return render_to_response('playerstats.html')
def table(request):
    return render_to_response('matchtable.html')