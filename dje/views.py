# -*- coding: utf-8 -*-
import mimetypes

from django.shortcuts import render_to_response
from random import randint
from django.http import HttpRequest, HttpResponse
import urllib2, urllib
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import service_request
import django.utils.simplejson as json
from django.http import HttpResponseRedirect

standlist = [
    {'teamId': int(1), 'teamName': 'Beşiktaş','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(58), 'change': int(1)},
    {'teamId': int(2), 'teamName': 'Bursaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(55), 'change': int(-1)},
    {'teamId': int(3), 'teamName': 'Eskişehirspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(8), 'points':int(46), 'change': int(2)},
    {'teamId': int(4), 'teamName': 'Fenerbahçe','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(61), 'change': int(3)},
    {'teamId': int(5), 'teamName': 'Galatasaray','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(71), 'change': int(-4)},
    {'teamId': int(6), 'teamName': 'Gaziantepspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(-7), 'points':int(46), 'change': int(0)},
    {'teamId': int(7), 'teamName': 'Gençlerbirliği','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(45), 'change': int(1)},
    {'teamId': int(8), 'teamName': 'İstanbul BŞB','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(36), 'change': int(1)},
    {'teamId': int(9), 'teamName': 'KDÇ Karabük','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(40), 'change': int(1)},
    {'teamId': int(12), 'teamName': 'Antalyaspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(47), 'change': int(1)},
    {'teamId': int(11), 'teamName': 'Akhisar Bel.','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(42), 'change': int(1)},
    {'teamId': int(17), 'teamName': 'Sivasspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(44), 'change': int(1)},
    {'teamId': int(14), 'teamName': 'S.B. Elazığspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(43), 'change': int(1)},
    {'teamId': int(15), 'teamName': 'Orduspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(29), 'change': int(1)},
    {'teamId': int(13), 'teamName': 'Mersin İY','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(22), 'change': int(1)},
    {'teamId': int(18), 'teamName': 'Trabzonspor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(-1), 'points':int(46), 'change': int(1)},
    {'teamId': int(16), 'teamName': 'Kasımpaşa','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(50), 'change': int(1)},
    {'teamId': int(10), 'teamName': 'Kayserispor','played':int(34), 'win':int(16), 'draw':int(10), 'lose':int(8), 'score':randint(18,71), 'conceded' : int(49), 'average':int(14), 'points':int(52), 'change': int(1)}]


weekList = []
for x in range(1, 35):
    weekList.append(x)

bestList = [
    {'teamId': int(18), 'playerId': int(13),'playerName':'Onur Kıvrak', 'jerseyNumber':int(1), 'rating':float(7.5), 'distanceMatch':int(4489), 'distanceLeague':int(3997), 'passTotalMatch' : int(14), 'passTotalLeague':float(13.2), 'passSuccessfulMatch':int(11), 'passSuccessfulLeague': float(8.3), 'savesMatch':int(11), 'savesLeague': float(8.3), '1on1TotalMatch':int(3), '1on1TotalLeague': float(2.8), '1on1SuccessfulMatch':int(3), '1on1SuccessfulLeague': float(1.7), 'concededMatch':int(0), 'concededLeague': int(18), 'penaltySaveMatch':int(0), 'penaltySaveLeague': int(3), 'playPosition': int(0),'goalLeague': int(0),'goalList': []},
    {'teamId': int(1), 'playerId': int(14),'playerName':'Tomas Sivok', 'jerseyNumber':int(3), 'rating':float(7.6), 'distanceMatch':int(9897), 'distanceLeague':int(9753), 'HIRMatch':int(74), 'HIRLeague':int(90), 'sprintMatch':int(25), 'sprintLeague':int(38), 'passTotalMatch' : int(25), 'passTotalLeague':float(19.4), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.4), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.6), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(5), 'faulCommittedLeague': float(6.4), 'faulAgainstMatch':int(3), 'faulAgainstLeague': float(2.7), 'stealMatch':int(4), 'stealLeague': int(5.6), 'turnoverMatch':int(3), 'turnoverLeague': int(2.2), 'playPosition': int(2), 'goalMatch': int(0), 'goalLeague': int(4), 'assistMatch': int(0), 'assistLeague': int(1),'goalList': [1,2,3,4]},
    {'teamId': int(5), 'playerId': int(15),'playerName':'Alber Riera', 'jerseyNumber':int(4), 'rating':float(7.6), 'distanceMatch':int(12467), 'distanceLeague':int(10432), 'HIRMatch':int(244), 'HIRLeague':int(157), 'sprintMatch':int(72), 'sprintLeague':int(58), 'passTotalMatch' : int(32), 'passTotalLeague':float(24.3), 'passSuccessfulMatch':int(26), 'passSuccessfulLeague': float(19.1), 'shotTotalMatch':int(1), 'shotTotalLeague': float(1.1), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(0.6), 'crossTotalMatch':int(7), 'crossTotalLeague': float(5.4), 'crossSuccessfulMatch':int(3), 'crossSuccessfulLeague': float(3.4), 'faulCommittedMatch':int(9), 'faulCommittedLeague': float(5.1), 'faulAgainstMatch':int(5), 'faulAgainstLeague': float(4.2), 'stealMatch':int(7), 'stealLeague': int(3.1), 'turnoverMatch':int(2), 'turnoverLeague': int(5.4), 'playPosition': int(1), 'goalMatch': int(0), 'goalLeague': int(2), 'assistMatch': int(1), 'assistLeague': int(6), 'goalList': [1,2]},
    {'teamId': int(3), 'playerId': int(16),'playerName':'Jerry Akaminko', 'jerseyNumber':int(30), 'rating':float(7.6), 'distanceMatch':int(9948), 'distanceLeague':int(9654), 'HIRMatch':int(40), 'HIRLeague':int(55), 'sprintMatch':int(0), 'sprintLeague':int(22), 'passTotalMatch' : int(17), 'passTotalLeague':float(18.1), 'passSuccessfulMatch':int(13), 'passSuccessfulLeague': float(13.1), 'shotTotalMatch':int(1), 'shotTotalLeague': float(0.2), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(0.1), 'crossTotalMatch':int(0), 'crossTotalLeague': float(0.2), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.1), 'faulCommittedMatch':int(7), 'faulCommittedLeague': float(7.1), 'faulAgainstMatch':int(4), 'faulAgainstLeague': float(3.1), 'stealMatch':int(4), 'stealLeague': int(6.1), 'turnoverMatch':int(6), 'turnoverLeague': int(2.2), 'playPosition': int(3), 'goalMatch': int(1), 'goalLeague': int(4), 'assistMatch': int(0), 'assistLeague': int(1), 'goalList': [1,2,3,4]},
    {'teamId': int(4), 'playerId': int(17),'playerName':'Gökhan Gönül', 'jerseyNumber':int(77), 'rating':float(7.6), 'distanceMatch':int(11456), 'distanceLeague':int(10324), 'HIRMatch':int(113), 'HIRLeague':int(99), 'sprintMatch':int(10), 'sprintLeague':int(23), 'passTotalMatch' : int(31), 'passTotalLeague':float(22.4), 'passSuccessfulMatch':int(24), 'passSuccessfulLeague': float(14.3), 'shotTotalMatch':int(0), 'shotTotalLeague': float(0.3), 'shotSuccessfulMatch':int(0), 'shotSuccessfulLeague': float(0.25), 'crossTotalMatch':int(4), 'crossTotalLeague': float(5.2), 'crossSuccessfulMatch':int(2), 'crossSuccessfulLeague': float(3.3), 'faulCommittedMatch':int(3), 'faulCommittedLeague': float(4.4), 'faulAgainstMatch':int(2), 'faulAgainstLeague': float(2.7), 'stealMatch':int(3), 'stealLeague': int(2.1), 'turnoverMatch':int(3), 'turnoverLeague': int(2.4), 'playPosition': int(4), 'goalMatch': int(0), 'goalLeague': int(2), 'assistMatch': int(0), 'assistLeague': int(0), 'goalList': [1,2]},
    {'teamId': int(18), 'playerId': int(18),'playerName':'Olcan Adın', 'jerseyNumber':int(9), 'rating':float(7.6), 'distanceMatch':int(10952), 'distanceLeague':int(9342), 'HIRMatch':int(80), 'HIRLeague':int(132), 'sprintMatch':int(32), 'sprintLeague':int(45), 'passTotalMatch' : int(42), 'passTotalLeague':float(34.5), 'passSuccessfulMatch':int(34), 'passSuccessfulLeague': float(26.4), 'shotTotalMatch':int(2), 'shotTotalLeague': float(1.1), 'shotSuccessfulMatch':int(2), 'shotSuccessfulLeague': float(0.7), 'crossTotalMatch':int(2), 'crossTotalLeague': float(3.1), 'crossSuccessfulMatch':int(1), 'crossSuccessfulLeague': float(2.1), 'faulCommittedMatch':int(2), 'faulCommittedLeague': float(2.7), 'faulAgainstMatch':int(5), 'faulAgainstLeague': float(3.7), 'stealMatch':int(2), 'stealLeague': int(3), 'turnoverMatch':int(4), 'turnoverLeague': int(3.2), 'playPosition': int(5), 'goalMatch': int(0), 'goalLeague': int(3), 'assistMatch': int(1), 'assistLeague': int(4),'goalList': [1,2,3]},
    {'teamId': int(4), 'playerId': int(19),'playerName':'Emre Belözoğlu', 'jerseyNumber':int(25), 'rating':float(7.6), 'distanceMatch':int(10032), 'distanceLeague':int(9553), 'HIRMatch':int(176), 'HIRLeague':int(154), 'sprintMatch':int(45), 'sprintLeague':int(61), 'passTotalMatch' : int(46), 'passTotalLeague':float(38.9), 'passSuccessfulMatch':int(38), 'passSuccessfulLeague': float(27.9), 'shotTotalMatch':int(1), 'shotTotalLeague': float(2.3), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(1.1), 'crossTotalMatch':int(3), 'crossTotalLeague': float(2.1), 'crossSuccessfulMatch':int(2), 'crossSuccessfulLeague': float(1.3), 'faulCommittedMatch':int(6), 'faulCommittedLeague': float(4.5), 'faulAgainstMatch':int(4), 'faulAgainstLeague': float(4.1), 'stealMatch':int(0), 'stealLeague': int(1.7), 'turnoverMatch':int(2), 'turnoverLeague': int(4.2), 'playPosition': int(6), 'goalMatch': int(1), 'goalLeague': int(4), 'assistMatch': int(1), 'assistLeague': int(3),'goalList': [1,2,3,4]},
    {'teamId': int(2), 'playerId': int(20),'playerName':'Pablo Batalla', 'jerseyNumber':int(10), 'rating':float(7.6), 'distanceMatch':int(9245), 'distanceLeague':int(9031), 'HIRMatch':int(182), 'HIRLeague':int(195), 'sprintMatch':int(62), 'sprintLeague':int(71), 'passTotalMatch' : int(54), 'passTotalLeague':float(42.3), 'passSuccessfulMatch':int(44), 'passSuccessfulLeague': float(34.3), 'shotTotalMatch':int(2), 'shotTotalLeague': float(3.1), 'shotSuccessfulMatch':int(1), 'shotSuccessfulLeague': float(2), 'crossTotalMatch':int(4), 'crossTotalLeague': float(3.3), 'crossSuccessfulMatch':int(4), 'crossSuccessfulLeague': float(2.5), 'faulCommittedMatch':int(4), 'faulCommittedLeague': float(7.2), 'faulAgainstMatch':int(7), 'faulAgainstLeague': float(1.1), 'stealMatch':int(5), 'stealLeague': int(3.4), 'turnoverMatch':int(4), 'turnoverLeague': int(3.5), 'playPosition': int(7), 'goalMatch': int(0), 'goalLeague': int(6), 'assistMatch': int(0), 'assistLeague': int(6), 'goalList': [1,2,3,4,5,6]},
    {'teamId': int(1), 'playerId': int(21),'playerName':'Filip Holosko', 'jerseyNumber':int(11), 'rating':float(7.6), 'distanceMatch':int(11003), 'distanceLeague':int(10523), 'HIRMatch':int(221), 'HIRLeague':int(201), 'sprintMatch':int(71), 'sprintLeague':int(56), 'passTotalMatch' : int(36), 'passTotalLeague':float(27.6), 'passSuccessfulMatch':int(31), 'passSuccessfulLeague': float(21.7), 'shotTotalMatch':int(3), 'shotTotalLeague': float(2.1), 'shotSuccessfulMatch':int(2), 'shotSuccessfulLeague': float(1.3), 'crossTotalMatch':int(3), 'crossTotalLeague': float(2.7), 'crossSuccessfulMatch':int(2), 'crossSuccessfulLeague': float(1.2), 'faulCommittedMatch':int(2), 'faulCommittedLeague': float(2.1), 'faulAgainstMatch':int(2), 'faulAgainstLeague': float(2), 'stealMatch':int(3), 'stealLeague': int(2.1), 'turnoverMatch':int(2), 'turnoverLeague': int(4.1), 'playPosition': int(8), 'goalMatch': int(1), 'goalLeague': int(11), 'assistMatch': int(2), 'assistLeague': int(7), 'goalList': [1,2,3,4,5,6,7,8,9,10,11]},
    {'teamId': int(19), 'playerId': int(22),'playerName':'Kalu Uche', 'jerseyNumber':int(9), 'rating':float(7.6), 'distanceMatch':int(10211), 'distanceLeague':int(9743), 'HIRMatch':int(164), 'HIRLeague':int(152), 'sprintMatch':int(54), 'sprintLeague':int(34), 'passTotalMatch' : int(24), 'passTotalLeague':float(17.2), 'passSuccessfulMatch':int(20), 'passSuccessfulLeague': float(12.3), 'shotTotalMatch':int(7), 'shotTotalLeague': float(5.2), 'shotSuccessfulMatch':int(4), 'shotSuccessfulLeague': float(2.5), 'crossTotalMatch':int(1), 'crossTotalLeague': float(0.8), 'crossSuccessfulMatch':int(1), 'crossSuccessfulLeague': float(0.3), 'faulCommittedMatch':int(1), 'faulCommittedLeague': float(3.1), 'faulAgainstMatch':int(5), 'faulAgainstLeague': float(1.7), 'stealMatch':int(2), 'stealLeague': int(1.2), 'turnoverMatch':int(4), 'turnoverLeague': int(3.2), 'playPosition': int(10), 'goalMatch': int(2), 'goalLeague': int(13), 'assistMatch': int(0), 'assistLeague': int(4), 'goalList': [1,2,3,4,5,6,7,8,9,10,11,12,13]},
    {'teamId': int(5), 'playerId': int(23),'playerName':'Didier Drogba', 'jerseyNumber':int(14), 'rating':float(7.6), 'distanceMatch':int(98999), 'distanceLeague':int(9643), 'HIRMatch':int(122), 'HIRLeague':int(135), 'sprintMatch':int(33), 'sprintLeague':int(41), 'passTotalMatch' : int(22), 'passTotalLeague':float(18.5), 'passSuccessfulMatch':int(17), 'passSuccessfulLeague': float(12.6), 'shotTotalMatch':int(5), 'shotTotalLeague': float(4.4), 'shotSuccessfulMatch':int(3), 'shotSuccessfulLeague': float(1.9), 'crossTotalMatch':int(1), 'crossTotalLeague': float(0.4), 'crossSuccessfulMatch':int(0), 'crossSuccessfulLeague': float(0.1), 'faulCommittedMatch':int(0), 'faulCommittedLeague': float(0.9), 'faulAgainstMatch':int(4), 'faulAgainstLeague': float(2.9), 'stealMatch':int(1), 'stealLeague': int(1.4), 'turnoverMatch':int(5), 'turnoverLeague': int(2.8), 'playPosition': int(11), 'goalMatch': int(2), 'goalLeague': int(12), 'assistMatch': int(0), 'assistLeague': int(5) ,'goalList': [1,2,3,4,5,6,7,8,9,10,11,12]}]

teamList =[]
for x in range(1, 19):
    teamList.append(x)

playerList = []
for x in range(1, 24):
    id = x
    match = randint(0,34)
    min = randint(0,12432)
    goal = randint(0,25)
    assist = randint(0,16)
    yellow = randint(0,8)
    red = randint(0,4)
    run = randint(0,11300)
    playerList.append({'id': id, 'jersey': "%s"%x, 'name': 'Serhat Kurtulus', 'match': int(match), 'min': int(min), 'goal': int(goal), 'assist': int(assist), 'yellow': int(yellow), 'red': int(red), 'run': int(run)})


def home(request):
    return render_to_response('statshome.html', {'weeklist': weekList, 'standing_list':standlist, 'best_eleven_list':bestList})

def team(request, num):


    #    post_data = [('name','Gladys'),]     # a sequence of two element tuples
    #    result = urllib2.urlopen('http://example.com', urllib.urlencode(post_data))
    #    content = result.read()

    s = []
    q = randint(1, 18)
    s.append(q)
    for x in range(1, 34):
        if q == 18:
            q += randint(-2, 0)
        elif q == 17:
            q += randint(-2, 1)
        elif q == 2:
            q += randint(-1, 2)
        elif q == 1:
            q += randint(0, 2)
        else:
            q += randint(-2, 2)
        s.append(q)

        #    post_data = '{"team_ids":["1"]}'
        #    result = urllib2.urlopen('http://sentio.cloudapp.net:8080/api/GetTeamsInformation', post_data)
        #    content = result.read()
    data = {"leagueId": 1, "seasonId": 8918}
    teams = service_request("GetTeams", data)
    j_obj = json.loads(teams)
    datalist = j_obj["data"]
    teamDict = []
    for x in datalist:
        teamDict.append({'teamId':x[0],'teamName':x[1]})

    data = {"teamId": num}
    details = service_request("GetTeamDetails", data)
    j_obj = json.loads(details)
    datalist = j_obj["data"]
    detailDict = []
    for obj in datalist:
        detailDict.append( {'teamName':obj[0],'stadium':obj[1],'foundation':obj[2],'president':obj[3],'capacity':obj[4],'manager':obj[5],'website':obj[6],'leaguechamp':obj[7],'cupchamp':obj[8]})

    data = {"leagueId": 1, "seasonId": 8918, "teamId": num}
    players = service_request("GetTeamPlayers", data)
    j_obj = json.loads(players)
    datalist = j_obj["data"]
    playerDict =[]
    for x in datalist:
        playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})

    return render_to_response('statsteam.html', {'s_list': s,'team_list': teamList, 'try_list':teamDict, 'details':detailDict,'players':playerDict, 'standing_list':standlist, 'team_selected': int(num), 'player_list':playerList, 'weeklist': weekList,'best_eleven_list':bestList})


def league(request):
    return render_to_response('statsleague.html', {'weeklist': weekList , 'standing_list':standlist, 'team_list': teamList, 'weeklist': weekList,'best_eleven_list':bestList})

@ensure_csrf_cookie
def playerx(request, num, player_id):

    data = {"leagueId": 1, "seasonId": 8918,"playerId": player_id}
    details = service_request("GetPlayerDetails", data)
    j_obj = json.loads(details)
    datalist = j_obj["data"]
    detailDict = []
    for obj in datalist:
        detailDict.append({'playerName':obj[0],'date':obj[1],'height':obj[2],'nation':obj[3],'cap':obj[4],'goal':obj[5],'teamId':obj[6],'teamName':obj[7]})

    data = {"leagueId": 1, "seasonId": 8918, "teamId": num}
    players = service_request("GetTeamPlayers", data)
    j_obj = json.loads(players)
    datalist = j_obj["data"]
    playerDict =[]
    for x in datalist:
        playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})

    data = {"leagueId": 1, "seasonId": 8918}
    teams = service_request("GetTeams", data)
    j_obj = json.loads(teams)
    datalist = j_obj["data"]
    teamDict = []
    for x in datalist:
        teamDict.append({'teamId':x[0],'teamName':x[1]})

    return render_to_response('statsplayer.html', {'p_id': int(player_id), 'details':detailDict, 'try_list':teamDict,'players':playerDict, 'team_selected': int(num), 'team_list': teamList, 'standing_list': standlist, 'player_list':playerList, "best_eleven_list":bestList, 'weeklist': weekList})

def player3(request, num):

    data = {"leagueId": 1, "seasonId": 8918, "teamId": num}
    players = service_request("GetTeamPlayers", data)
    j_obj = json.loads(players)
    datalist = j_obj["data"]
    playerDict =[]
    for x in datalist:
        playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})
    data = {"leagueId": 1, "seasonId": 8918}
    teams = service_request("GetTeams", data)
    j_obj = json.loads(teams)
    datalist = j_obj["data"]
    teamDict = []
    for x in datalist:
        teamDict.append({'teamId':x[0],'teamName':x[1]})
    return render_to_response('playerselection.html', { 'team_selected': int(num), 'try_list':teamDict, 'team_list': teamList, 'standing_list': standlist,'players':playerDict, 'player_list':playerList, "best_eleven_list":bestList, 'weeklist': weekList})

def before(request,reqid):
    data = {"leagueId": 1, "seasonId": 8918}
    matches = service_request("GetFixture", data)
    j_obj = json.loads(matches)
    weeklist = j_obj["data"]
    weekDict = []
    currentWeek = 34
    for weekId in weeklist:
        week = weeklist[weekId]
        matches = []
        for matchId in week:
            if matchId == "weekStatus":
                status = week[matchId]
            else:
                print(matchId)
                if(matchId==str(reqid)):
                    currentWeek = weekId
                matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':week[matchId][7],'awayTeamId':week[matchId][8],'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
        weekDict.append({'weekId':int(weekId),'status':status,'matches':matches})

    data = {"leagueId":1,"seasonId":8918,"matchId":reqid}
    teams = service_request("GetMatchInfo", data)
    j_obj = json.loads(teams)
    list = j_obj["data"]
    infoDict = []
    for x in list:
        infoDict.append({'weekId':x[0],'matchId':x[1],'status':x[2],'homeTeam':x[3],'awayTeam':x[4],'homeTeamId':x[5],'awayTeamId':x[6],'homeTeamScore':x[7],'awayTeamScore':x[8],'date':x[9],'time':x[10],'liveTime':x[11],'referee':x[12],'stadium':x[13]})
    return render_to_response('virtual_stadium_before_match.html', {'weeklist': weekList,'matchInfo':infoDict,'weeks':weekDict,'currentWeek':currentWeek,'selectedMatch':str(reqid)})
def center(request,reqid):
    data = {"leagueId": 1, "seasonId": 8918}
    matches = service_request("GetFixture", data)
    j_obj = json.loads(matches)
    weeklist = j_obj["data"]
    weekDict = []
    currentWeek = 34
    for weekId in weeklist:
        week = weeklist[weekId]
        matches = []
        for matchId in week:
            if matchId == "weekStatus":
                status = week[matchId]
            else:
                print(matchId)
                if(matchId==str(reqid)):
                    currentWeek = weekId
                matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':week[matchId][7],'awayTeamId':week[matchId][8],'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
        weekDict.append({'weekId':int(weekId),'status':status,'matches':matches})
    data = {"leagueId":1,"seasonId":8918,"matchId":reqid}
    teams = service_request("GetMatchInfo", data)
    j_obj = json.loads(teams)
    list = j_obj["data"]
    infoDict = []
    for x in list:
        infoDict.append({'weekId':x[0],'matchId':x[1],'status':x[2],'homeTeam':x[3],'awayTeam':x[4],'homeTeamId':x[5],'awayTeamId':x[6],'homeTeamScore':x[7],'awayTeamScore':x[8],'date':x[9],'time':x[10],'liveTime':x[11],'referee':x[12],'stadium':x[13]})
    return render_to_response('virtual_stadium.html', {'weeklist': weekList,'weeks':weekDict,'matchInfo':infoDict,'currentWeek':currentWeek,'selectedMatch':str(reqid)})
def summary(request):
    return render_to_response('matchsummary.html')
def compare(request):
    return render_to_response('statscompare.html')
def player(request):
    data = {"leagueId": 1, "seasonId": 8918}
    teams = service_request("GetTeams", data)
    j_obj = json.loads(teams)
    list = j_obj["data"]
    teamDict = []
    for x in list:
        teamDict.append({'teamId':x[0],'teamName':x[1]})
    return render_to_response('playerteamselection.html',{'standing_list':standlist, 'best_eleven_list':bestList, 'weeklist': weekList, 'try_list':teamDict} )

@ensure_csrf_cookie
def table(request):
    c = []
    for x in range(1, 35):
        c.append(x)
    return render_to_response('virtual_stadium_board.html', {'weeklist': c})

@ensure_csrf_cookie
def chalkboard(request):
    return render_to_response('chalkboard.html')


def team2(request):
    data = {"leagueId": 1, "seasonId": 8918}
    teams = service_request("GetTeams", data)
    j_obj = json.loads(teams)
    list = j_obj["data"]
    teamDict = []
    for x in list:
        teamDict.append({'teamId':x[0],'teamName':x[1]})
    return render_to_response('teamselection.html',{'standing_list':standlist, 'weeklist':weekList,'try_list':teamDict} )

@ensure_csrf_cookie
def radar(request):
    return render_to_response('radar.html')

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

def matchcenter(request,match_id):
    data = {"leagueId":1,"seasonId":8918,"matchId":match_id}
    teams = service_request("GetMatchInfo", data)
    j_obj = json.loads(teams)
    list = j_obj["data"]
    for x in list:
        if(x[1]=="1"):
            return HttpResponseRedirect("before")
        else:
            return HttpResponseRedirect("before")
