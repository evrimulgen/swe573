# -*- coding: utf-8 -*-
import mimetypes

from django.shortcuts import render_to_response
from random import randint
from django.http import HttpRequest, HttpResponse
import urllib2, urllib
from django.views.decorators.csrf import ensure_csrf_cookie

def home(request):
    a = []
    for x in range(1, 35):
        a.append(x)

    b = []
    b.append({'teamId': int(1), 'teamName': 'Beşiktaş','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(58), 'change': int(1)})
    b.append({'teamId': int(2), 'teamName': 'Bursaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(55), 'change': int(-1)})
    b.append({'teamId': int(3), 'teamName': 'Eskişehirspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(8), 'points':int(46), 'change': int(2)})
    b.append({'teamId': int(4), 'teamName': 'Fenerbahçe','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(61), 'change': int(3)})
    b.append({'teamId': int(5), 'teamName': 'Galatasaray','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(71), 'change': int(0)})
    b.append({'teamId': int(6), 'teamName': 'Gaziantepspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-7), 'points':int(46), 'change': int(0)})
    b.append({'teamId': int(7), 'teamName': 'Gençlerbirliği','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(45), 'change': int(-1)})
    b.append({'teamId': int(8), 'teamName': 'İstanbul BŞB','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(36), 'change': int(1)})
    b.append({'teamId': int(9), 'teamName': 'KDÇ Karabükspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(40), 'change': int(-2)})
    b.append({'teamId': int(10), 'teamName': 'Antalyaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(47), 'change': int(1)})
    b.append({'teamId': int(11), 'teamName': 'Akhisar Belediye','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(42), 'change': int(1)})
    b.append({'teamId': int(12), 'teamName': 'Sivasspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(44), 'change': int(1)})
    b.append({'teamId': int(13), 'teamName': 'S.B. Elazığspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(43), 'change': int(0)})
    b.append({'teamId': int(14), 'teamName': 'Orduspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(29), 'change': int(0)})
    b.append({'teamId': int(15), 'teamName': 'Mersin İY','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(22), 'change': int(0)})
    b.append({'teamId': int(16), 'teamName': 'Trabzonspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(-1), 'points':int(46), 'change': int(1)})
    b.append({'teamId': int(17), 'teamName': 'Kasımpaşa','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(50), 'change': int(0)})
    b.append({'teamId': int(18), 'teamName': 'Kayserispor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':int(63), 'conceded' : int(49), 'average':int(14), 'points':int(52), 'change': int(1)})

    c = []
    c.append({'teamId': int(18), 'playerId': int(13),'playerName':'Onur Kıvrak', 'jerseyNumber':int(1), 'rating':float(7.5), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'passTotalMatch' : int(14), 'passTotalLeague':float(13.2), 'passSuccessfulMatch':int(11), 'passSuccessfulLeague': float(8.3), 'savesMatch':int(11), 'savesLeague': float(8.3), '1on1TotalMatch':int(3), '1on1TotalLeague': float(2.8), '1on1SuccessfulMatch':int(3), '1on1SuccessfulLeague': float(1.7), 'concededMatch':int(0), 'concededLeague': int(18), 'penaltySaveMatch':int(0), 'penaltySaveLeague': int(3), 'playPosition': int(0)})
    c.append({'teamId': int(1), 'playerId': int(14),'playerName':'Tomas Sivok', 'jerseyNumber':int(3), 'rating':float(7.6), 'distanceMatch':int(9897), 'distanceLeague':int(9753), 'HIRMatch':int(74), 'HIRLeague':int(90), 'sprintMatch':int(25), 'sprintLeague':int(38), 'passTotalMatch' : int(25), 'passTotalLeague':float(19.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(2), 'goalMatch': int(0), 'goalLeague': int(4), 'assistMatch': int(0), 'assistLeague': int(1)})
    c.append({'teamId': int(5), 'playerId': int(15),'playerName':'Alber Riera', 'jerseyNumber':int(4), 'rating':float(7.6), 'distanceMatch':int(12467), 'distanceLeague':int(10432), 'HIRMatch':int(244), 'HIRLeague':int(157), 'sprintMatch':int(72), 'sprintLeague':int(58), 'passTotalMatch' : int(32), 'passTotalLeague':float(24.3), 'passSuccessfulMatch':int(26), 'passSuccessfulLeague': float(19.1), 'shotTotalMatch':int(1), 'shotTotalLeague': float(1.1), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(0.6), 'crossTotalMatch':int(7), 'crossTotalLeague': float(5.4), 'crossSuccessfulMatch':int(3), 'crossSuccessfulLeague': float(3.4), 'faulCommittedMatch':int(9), 'faulCommittedLeague': float(5.1), 'faulAgainstMatch':int(5), 'faulAgainstLeague': float(4.2), 'stealMatch':int(7), 'stealLeague': int(3.1), 'turnoverMatch':int(2), 'turnoverLeague': int(5.4), 'playPosition': int(1), 'goalMatch': int(0), 'goalLeague': int(2), 'assistMatch': int(1), 'assistLeague': int(6)})
    c.append({'teamId': int(3), 'playerId': int(16),'playerName':'Jerry Akaminko', 'jerseyNumber':int(30), 'rating':float(7.6), 'distanceMatch':int(9948), 'distanceLeague':int(9654), 'HIRMatch':int(40), 'HIRLeague':int(55), 'sprintMatch':int(0), 'sprintLeague':int(22), 'passTotalMatch' : int(17), 'passTotalLeague':float(18.1), 'passSuccessfulMatch':int(13), 'passSuccessfulLeague': float(13.1), 'shotTotalMatch':int(1), 'shotTotalLeague': float(0.2), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(0.1), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.2), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.1), 'faulCommittedMatch':int(7), 'faulCommittedLeague': float(7.1), 'faulAgainstMatch':int(4), 'faulAgainstLeague': float(3.1), 'stealMatch':int(4), 'stealLeague': int(6.1), 'turnoverMatch':int(6), 'turnoverLeague': int(2.2), 'playPosition': int(3), 'goalMatch': int(1), 'goalLeague': int(4), 'assistMatch': int(0), 'assistLeague': int(1)})
    c.append({'teamId': int(4), 'playerId': int(17),'playerName':'Gökhan Gönül', 'jerseyNumber':int(77), 'rating':float(7.6), 'distanceMatch':int(11456), 'distanceLeague':int(10324), 'HIRMatch':int(113), 'HIRLeague':int(99), 'sprintMatch':int(10), 'sprintLeague':int(23), 'passTotalMatch' : int(31), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(24), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.3), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(4), 'crossTotalLeague': float(5.2), 'crossSuccessfulMatch':int(2), 'crossSuccessfulLeague': float(3.3), 'faulCommittedMatch':int(3), 'faulCommittedLeague': float(4.4), 'faulAgainstMatch':int(2), 'faulAgainstLeague': float(2.7), 'stealMatch':int(3), 'stealLeague': int(2.1), 'turnoverMatch':int(3), 'turnoverLeague': int(2.4), 'playPosition': int(4), 'goalMatch': int(0), 'goalLeague': int(2), 'assistMatch': int(0), 'assistLeague': int(0)})
    c.append({'teamId': int(18), 'playerId': int(18),'playerName':'Olcan Adın', 'jerseyNumber':int(9), 'rating':float(7.6), 'distanceMatch':int(10952), 'distanceLeague':int(9342), 'HIRMatch':int(80), 'HIRLeague':int(132), 'sprintMatch':int(32), 'sprintLeague':int(45), 'passTotalMatch' : int(42), 'passTotalLeague':float(34.5), 'passSuccessfulMatch':int(34), 'passSuccessfulLeague': float(26.4), 'shotTotalMatch':int(2), 'shotTotalLeague': float(1.1), 'shotSuccessfulMatch':int(2), 'shotSuccessfulLeague': float(0.7), 'crossTotalMatch':int(2), 'crossTotalLeague': float(3.1), 'crossSuccessfulMatch':int(1), 'crossSuccessfulLeague': float(2.1), 'faulCommittedMatch':int(2), 'faulCommittedLeague': float(2.7), 'faulAgainstMatch':int(5), 'faulAgainstLeague': float(3.7), 'stealMatch':int(2), 'stealLeague': int(3), 'turnoverMatch':int(4), 'turnoverLeague': int(3.2), 'playPosition': int(5), 'goalMatch': int(0), 'goalLeague': int(3), 'assistMatch': int(1), 'assistLeague': int(4)})
    c.append({'teamId': int(4), 'playerId': int(19),'playerName':'Emre Belözoğlu', 'jerseyNumber':int(25), 'rating':float(7.6), 'distanceMatch':int(10032), 'distanceLeague':int(9553), 'HIRMatch':int(176), 'HIRLeague':int(154), 'sprintMatch':int(45), 'sprintLeague':int(61), 'passTotalMatch' : int(46), 'passTotalLeague':float(38.9), 'passSuccessfulMatch':int(38), 'passSuccessfulLeague': float(27.9), 'shotTotalMatch':int(1), 'shotTotalLeague': float(2.3), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(1.1), 'crossTotalMatch':int(3), 'crossTotalLeague': float(2.1), 'crossSuccessfulMatch':int(2), 'crossSuccessfulLeague': float(1.3), 'faulCommittedMatch':int(6), 'faulCommittedLeague': float(4.5), 'faulAgainstMatch':int(4), 'faulAgainstLeague': float(4.1), 'stealMatch':int(0), 'stealLeague': int(1.7), 'turnoverMatch':int(2), 'turnoverLeague': int(4.2), 'playPosition': int(6), 'goalMatch': int(1), 'goalLeague': int(4), 'assistMatch': int(1), 'assistLeague': int(3)})
    c.append({'teamId': int(2), 'playerId': int(20),'playerName':'Pablo Batalla', 'jerseyNumber':int(10), 'rating':float(7.6), 'distanceMatch':int(9245), 'distanceLeague':int(9031), 'HIRMatch':int(182), 'HIRLeague':int(195), 'sprintMatch':int(62), 'sprintLeague':int(71), 'passTotalMatch' : int(54), 'passTotalLeague':float(42.3), 'passSuccessfulMatch':int(44), 'passSuccessfulLeague': float(34.3), 'shotTotalMatch':int(2), 'shotTotalLeague': float(3.1), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(2), 'crossTotalMatch':int(4), 'crossTotalLeague': float(3.3), 'crossSuccessfulMatch':int(4), 'crossSuccessfulLeague': float(2.5), 'faulCommittedMatch':int(4), 'faulCommittedLeague': float(7.2), 'faulAgainstMatch':int(7), 'faulAgainstLeague': float(1.1), 'stealMatch':int(5), 'stealLeague': int(3.4), 'turnoverMatch':int(4), 'turnoverLeague': int(3.5), 'playPosition': int(7), 'goalMatch': int(0), 'goalLeague': int(6), 'assistMatch': int(0), 'assistLeague': int(6)})
    c.append({'teamId': int(1), 'playerId': int(21),'playerName':'Filip Holosko', 'jerseyNumber':int(11), 'rating':float(7.6), 'distanceMatch':int(11003), 'distanceLeague':int(10523), 'HIRMatch':int(221), 'HIRLeague':int(201), 'sprintMatch':int(71), 'sprintLeague':int(56), 'passTotalMatch' : int(36), 'passTotalLeague':float(27.6), 'passSuccessfulMatch':int(31), 'passSuccessfulLeague': float(21.7), 'shotTotalMatch':int(3), 'shotTotalLeague': float(2.1), 'shotSuccessfulMatch':int(2), 'shotSuccessfulLeague': float(1.3), 'crossTotalMatch':int(3), 'crossTotalLeague': float(2.7), 'crossSuccessfulMatch':int(2), 'crossSuccessfulLeague': float(1.2), 'faulCommittedMatch':int(2), 'faulCommittedLeague': float(2.1), 'faulAgainstMatch':int(2), 'faulAgainstLeague': float(2), 'stealMatch':int(3), 'stealLeague': int(2.1), 'turnoverMatch':int(2), 'turnoverLeague': int(4.1), 'playPosition': int(8), 'goalMatch': int(1), 'goalLeague': int(11), 'assistMatch': int(2), 'assistLeague': int(7)})
    c.append({'teamId': int(19), 'playerId': int(22),'playerName':'Kalu Uche', 'jerseyNumber':int(9), 'rating':float(7.6), 'distanceMatch':int(10211), 'distanceLeague':int(9743), 'HIRMatch':int(164), 'HIRLeague':int(152), 'sprintMatch':int(54), 'sprintLeague':int(34), 'passTotalMatch' : int(24), 'passTotalLeague':float(17.2), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(12.3), 'shotTotalMatch':int(7), 'shotTotalLeague': float(5.2), 'shotSuccessfulMatch':int(4), 'shotSuccessfulLeague': float(2.5), 'crossTotalMatch':int(1), 'crossTotalLeague': float(0.8), 'crossSuccessfulMatch':int(1), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(1), 'faulCommittedLeague': float(3.1), 'faulAgainstMatch':int(5), 'faulAgainstLeague': float(1.7), 'stealMatch':int(2), 'stealLeague': int(1.2), 'turnoverMatch':int(4), 'turnoverLeague': int(3.2), 'playPosition': int(10), 'goalMatch': int(2), 'goalLeague': int(13), 'assistMatch': int(0), 'assistLeague': int(4)})
    c.append({'teamId': int(5), 'playerId': int(23),'playerName':'Didier Drogba', 'jerseyNumber':int(14), 'rating':float(7.6), 'distanceMatch':int(98999), 'distanceLeague':int(9643), 'HIRMatch':int(122), 'HIRLeague':int(135), 'sprintMatch':int(33), 'sprintLeague':int(41), 'passTotalMatch' : int(22), 'passTotalLeague':float(18.5), 'passSuccessfulMatch':int(17), 'passSuccessfulLeague': float(12.6), 'shotTotalMatch':int(5), 'shotTotalLeague': float(4.4), 'shotSuccessfulMatch':int(3), 'shotSuccessfulLeague': float(1.9), 'crossTotalMatch':int(1), 'crossTotalLeague': float(0.4), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.1), 'faulCommittedMatch':int(0), 'faulCommittedLeague': float(0.9), 'faulAgainstMatch':int(4), 'faulAgainstLeague': float(2.9), 'stealMatch':int(1), 'stealLeague': int(1.4), 'turnoverMatch':int(5), 'turnoverLeague': int(2.8), 'playPosition': int(11), 'goalMatch': int(2), 'goalLeague': int(12), 'assistMatch': int(0), 'assistLeague': int(5)})
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
    c = []
    for x in range(1, 35):
        c.append(x)
    return render_to_response('virtual_stadium_before_match.html', {'weeklist': c})
def center(request):
    c = []
    for x in range(1, 35):
        c.append(x)
    return render_to_response('virtual_stadium.html', {'weeklist': c})
def summary(request):
    return render_to_response('matchsummary.html')
def player(request):
    return render_to_response('playerstats.html')
def table(request):
    c = []
    for x in range(1, 35):
        c.append(x)
    return render_to_response('virtual_stadium_board.html', {'weeklist': c})

@ensure_csrf_cookie
def chalkboard(request):
    return render_to_response('chalkboard.html')

def router(request, path):
    target_url = "http://sentio.cloudapp.net:8080/api/"
    url = '%s%s' % (target_url, path)
    if request.META.has_key('QUERY_STRING'):
        url += '?' + request.META['QUERY_STRING']
    try:
        if request.body:
            proxied_request = urllib2.urlopen(url, request.body)
        else:
            proxied_request = urllib2.urlopen(url)
        status_code = proxied_request.code
        mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        content = proxied_request.read()
    except urllib2.HTTPError as e:
        return HttpResponse(e.msg, status=e.code, mimetype='text/plain')
    else:
        return HttpResponse(content, status=status_code, mimetype=mimetype)
