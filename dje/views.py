# -*- coding: utf-8 -*-
import mimetypes

from django.shortcuts import render_to_response
from random import randint
from django.http import HttpRequest, HttpResponse
import urllib2, urllib
from django.views.decorators.csrf import ensure_csrf_cookie
from dje.helpers import get_match_narration
from .utils import service_request
import django.utils.simplejson as json
from django.http import HttpResponseRedirect
from datetime import datetime


leagueId = 1
seasonId = 9064

weekList = []
for x in range(1, 35):
    weekList.append(x)

bestList = [
    {'teamId': int(18), 'playerId': int(13),'playerName':'Onur Kıvrak', 'jerseyNumber':int(1), 'rating':float(7.5), 'distanceMatch':int(4489), 'TotalPassLeague':int(3997), 'passTotalMatch' : int(14), 'passTotalLeague':float(13.2), 'passSuccessfulMatch':int(11), 'passSuccessfulLeague': float(8.3), 'savesMatch':int(11), 'savesLeague': float(8.3), '1on1TotalMatch':int(3), '1on1TotalLeague': float(2.8), '1on1SuccessfulMatch':int(3), '1on1SuccessfulLeague': float(1.7), 'concededMatch':int(0), 'concededLeague': int(18), 'penaltySaveMatch':int(0), 'penaltySaveLeague': int(3), 'playPosition': int(0),'goalLeague': int(0),'goalList': []},
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

#match center "Maç Öncesi"
def before(request,reqid):

    #data for fixture, used for all views in match center
    data = {"leagueId": leagueId, "seasonId": seasonId}
    weeklist = service_request("GetFixture", data) # returns "data" field in response
    weekDict = [] # holds all fixture data
    currentWeek = 34 # if reqid(selected match id) not found current week is 34
    if len(weeklist) > 0 :
        for weekId in weeklist:
            week = weeklist[weekId]
            matches = [] #holds matches in week
            for matchId in week:
                if matchId == "weekStatus":
                    status = week[matchId]
                else:
                    #if requested match is found, that week is current week
                    if(matchId==str(reqid)):
                        currentWeek = weekId
                        #add matches
                    matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':week[matchId][7],'awayTeamId':week[matchId][8],'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
                #add weeks
            weekDict.append({'weekId':int(weekId),'status':status,'matches':matches})

    #data for match info, used for all views in match center
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchInfo", data) # returns "data" field in response
    infoDict = [] #holds match info data
    homeTeamId = 0 # home team id of current match
    awayTeamId = 0 # away team id of current match
    if len(datalist) > 0 :
        for x in datalist: #this list is single item list which holds match info only
            homeTeamId = x[5] #set home team id
            awayTeamId = x[6] #set away team id
            infoDict.append({'weekId':x[0],'matchId':x[1],'status':x[2],'homeTeam':x[3],'awayTeam':x[4],'homeTeamId':x[5],'awayTeamId':x[6],'homeTeamScore':int(x[7] or 0),'awayTeamScore':int(x[8] or 0),'date':x[9],'time':x[10],'liveTime':x[11],'referee':x[12],'stadium':x[13]})

    #   data for match goals, used for all views in match center
    #
    #   maç özeti ve diğer maç videoları buraya eklenmeli, yapı değişikliği olacak.
    #
    data = {"matchId":reqid}
    datalist = service_request("GetGoalVideos", data) # returns "data" field in response
    goalDict = [] #holds goal video data
    if len(datalist) > 0 :
        for x in datalist:
            goalDict.append({'teamId':x[0],'playerId':x[1],'playerName':x[2],'min':x[3],'goalLink':x[4]})

    # data for team squads, used in all views in match center
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchSquad", data)

    homeSquadDict = [] #holds home team squad
    awaySquadDict = [] #holds away team squad

    if len(datalist) > 0 :
        for playerId in datalist:
            playerEvents = [] #holds player events
            playerData = [] #holds player data(name,number, etc..)
            for x in datalist[playerId]:
                if x == "data":
                    playerData = datalist[playerId][x]
                elif x == "events":
                    playerEvents = datalist[playerId][x]

            eventDict = [] #holds player events
            for event in playerEvents:
                #add events
                eventDict.append({'eventType':event[0],'matchTime':event[1],'teamId':event[2],'playerId':int(event[3]),'playerIdIn':event[4],'jerseyNumber':event[5],'jerseyNumberIn':event[6]})

            #add player into corresponding team squads
            if(playerData[3] == homeTeamId):
                homeSquadDict.append({'playerId':int(playerId),'playerName':playerData[0],'jerseyNumber':playerData[1],'eleven':playerData[2],'playPosition':playerData[4],'playerEvents':eventDict})
            elif(playerData[3] == awayTeamId):
                awaySquadDict.append({'playerId':int(playerId),'playerName':playerData[0],'jerseyNumber':playerData[1],'eleven':playerData[2],'playPosition':playerData[4],'playerEvents':eventDict})

    # data for history of two team, used in "before" view only
    data = {"team1":homeTeamId,"team2":awayTeamId}
    datalist = service_request("GetHistoricData", data)

    pastMatches =[] #holds past matches
    if len(datalist) > 0 :
        #add past matches
        for match in datalist["pastMatches"]:
            pastMatches.append({'homeTeam':match[0],'awayTeam':match[1],'homeScore':match[2],'awayScore':match[3],'date':datetime.strptime(match[4],'%Y-%m-%d %H:%M:%S.0000000'),'referee':match[5],'stadium':match[6],'homeTeamId':match[8],'awayTeamId':match[9]})

        homeWin = 0 #home team win count
        awayWin = 0 #away team win count
        homeGoal = 0 #home team goal count
        awayGoal = 0 #away team goal count

        # for better visualisation 0 values interpreted as 1 in ratio calculations
        if datalist["homeWins"] == 0:
            homeWin = 1
        else:
            homeWin = datalist["homeWins"]

        if datalist["awayWins"] == 0:
            awayWin = 1
        else:
            awayWin = datalist["awayWins"]

        if datalist["homeGoals"] == 0:
            homeGoal = 1
        else:
            homeGoal = datalist["homeGoals"]

        if datalist["awayGoals"] == 0:
            awayGoal = 1
        else:
            awayGoal = datalist["awayGoals"]

        # ratio calculations for history graph
        # calculations made on 99 percent because graph borders causes problem on sizing
        homeWinRatio = int(99*homeWin/(homeWin+awayWin+datalist["draws"]))
        drawRatio = int(99*datalist["draws"]/(homeWin+awayWin+datalist["draws"]))
        awayWinRatio = 99 -(homeWinRatio+drawRatio)
        homeGoalRatio = int(99*homeGoal/(homeGoal+awayGoal))
        awayGoalRatio = 99-homeGoalRatio
        historicDict = [{'homeWins':datalist["homeWins"],'awayWins':datalist["awayWins"],'draws':datalist["draws"],'homeGoals':datalist["homeGoals"],'awayGoals':datalist["awayGoals"],'awayWinRatio':awayWinRatio,'homeWinRatio':homeWinRatio,'drawRatio':drawRatio,'homeGoalRatio':homeGoalRatio,'awayGoalRatio':awayGoalRatio,'pastMatches':pastMatches}]

    #data for home team form, used in "before" view only
    data = {"leagueId":leagueId,"seasonId":seasonId,"teamId":homeTeamId,"type":0,"weekId":currentWeek}
    datalist = service_request("GetTeamForm", data)

    homeFormDict = [] #holds home team form

    if len(datalist) > 0 :
        for match in datalist:
            win = 0 # 0-draw 1-win 2-lose
            #if home score > away score and the team is home team it is a win
            # also if away score > home score and the team is away team it is a win
            if (match[2] > match [3] and homeTeamId==match[4]) or (match[3] > match [2] and homeTeamId==match[5]):
                win=1
            # if score levels it is a draw
            elif match[2] == match [3]:
                win=0
            #else it is a lose
            else:
                win=2
            homeFormDict.append({'matchId':match[0],'matchName':match[1],'homeScore':match[2],'awayScore':match[3],'homeTeamId':match[4],'awayTeamId':match[5],'homeTeam':match[6],'awayTeam':match[7],'win':win})

    #data for away team form, used in "before" view only
    data = {"leagueId":leagueId,"seasonId":seasonId,"teamId":awayTeamId,"type":0,"weekId":currentWeek}
    datalist = service_request("GetTeamForm", data)

    awayFormDict = [] #holds away team form
    if len(datalist) > 0 :
        for match in datalist:
            win = 0 # 0-draw 1-win 2-lose
            #if home score > away score and the team is home team it is a win
            # also if away score > home score and the team is away team it is a win
            if (match[2] > match [3] and awayTeamId==match[4]) or (match[3] > match [2] and awayTeamId==match[5]):
                win=1
            # if score levels it is a draw
            elif match[2] == match [3]:
                win=0
            #else it is a lose
            else:
                win=2
            awayFormDict.append({'matchId':match[0],'matchName':match[1],'homeScore':match[2],'awayScore':match[3],'homeTeamId':match[4],'awayTeamId':match[5],'homeTeam':match[6],'awayTeam':match[7],'win':win})

    #data for match events in the game, used in "center" and "table" views
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchEvents", data)

    eventDict = [] #holds match events
    if len(datalist) > 0 :
        for event in datalist:
            eventDict.append({'type':event[0],'min':event[1],'teamId':int(event[2]),'playerId':event[3],'playerIdIn':event[4],'jerseyNumber':event[5],'jerseyNumberIn':event[6]})

    #data of all match(distance,pass,shot,cross,faul, etc..), used in all views
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchData", data)

    matchDataDict = [] #stores all players in the match
    homeDataDict = []  #stores only home players
    awayDataDict = [] #stores only away players

    #self explanatory
    #corners, offsides, penalties and cards should be added
    homeDistance = 0
    awayDistance = 0
    homeSpeed = 0
    awaySpeed = 0
    homeHIR = 0
    awayHIR = 0
    homeTotalPass = 0
    awayTotalPass = 0
    homeSuccessfulPass = 0
    awaySuccessfulPass = 0

    homeTotalShot = 0
    awayTotalShot = 0
    homeSuccessfulShot = 0
    awaySuccessfulShot = 0

    homeTotalCross = 0
    awayTotalCross = 0
    homeSuccessfulCross = 0
    awaySuccessfulCross = 0

    homeFoul = 0
    awayFoul = 0

    if len(datalist) > 0 :
        for dat in datalist:
            #add all data into match data
            matchDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
            if dat[0] == homeTeamId:

                #calculate home team totals
                homeDistance += int(dat[4] or 0)
                homeSpeed += int(dat[5] or 0)
                homeHIR += int(dat[6] or 0)
                homeTotalPass += int(dat[7] or 0)
                homeSuccessfulPass += int(dat[8] or 0)
                homeTotalShot += int(dat[9] or 0)
                homeSuccessfulShot += int(dat[10] or 0)
                homeTotalCross += int(dat[11] or 0)
                homeSuccessfulCross += int(dat[12] or 0)
                homeFoul += int(dat[13] or 0)

                #add home team players
                homeDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
            elif dat[0] == awayTeamId:

                #calculate away team totals
                awayDistance += int(dat[4] or 0)
                awaySpeed += int(dat[5] or 0)
                awayHIR += int(dat[6] or 0)
                awayTotalPass += int(dat[7] or 0)
                awaySuccessfulPass += int(dat[8] or 0)
                awayTotalShot += int(dat[9] or 0)
                awaySuccessfulShot += int(dat[10] or 0)
                awayTotalCross += int(dat[11] or 0)
                awaySuccessfulCross += int(dat[12] or 0)
                awayFoul += int(dat[13] or 0)
                #add away team players
                awayDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})

    #speed should be divided by player count
    #! this will not be displayed
    homeSpeed /= int(len(homeDataDict) or 1)
    awaySpeed /= int(len(awayDataDict) or 1)

    #ratios calculations
    homePassRatio = int(homeSuccessfulPass/float(homeTotalPass or 1) * 100)
    awayPassRatio = int(awaySuccessfulPass/float(awayTotalPass or 1) * 100)

    homeShotRatio = int(homeSuccessfulShot/float(homeTotalShot or 1) * 100)
    awayShotRatio = int(awaySuccessfulShot/float(awayTotalShot or 1) * 100)

    homeCrossRatio = int(homeSuccessfulCross/float(homeTotalCross or 1) * 100)
    awayCrossRatio = int(awaySuccessfulCross/float(awayTotalCross or 1) * 100)

    #percent calculations made for graphs,
    #this graphs will be changed due to last Lig Tv meeting
    #most of the percents will be not necessary
    #if data is zero percents are set to 50%

    homeDistancePercent = 0
    awayDistancePercent = 0
    if homeDistance+awayDistance < 1:
        homeDistancePercent = 50
    else:
        homeDistancePercent = int(homeDistance/float(homeDistance+awayDistance)*100)
    awayDistancePercent = 100 - homeDistancePercent

    homeSpeedPercent = 0
    awaySpeedPercent = 0
    if homeSpeed+awaySpeed < 1:
        homeSpeedPercent = 50
    else:
        homeSpeedPercent = int(homeSpeed/float(homeSpeed+awaySpeed)*100)
    awaySpeedPercent = 100 - homeSpeedPercent

    homeHIRPercent = 0
    awayHIRPercent = 0
    if homeHIR+awayHIR < 1:
        homeHIRPercent = 50
    else:
        homeHIRPercent = int(homeHIR/float(homeHIR+awayHIR)*100)
    awayHIRPercent = 100 - homeHIRPercent

    homeTotalPassPercent = 0
    awayTotalPassPercent = 0
    if homeTotalPass+awayTotalPass < 1:
        homeTotalPassPercent = 50
    else:
        homeTotalPassPercent = int(homeTotalPass/float(homeTotalPass+awayTotalPass)*100)
    awayTotalPassPercent = 100 - homeTotalPassPercent

    homeSuccessfulPassPercent = 0
    awaySuccessfulPassPercent = 0
    if homeSuccessfulPass+awaySuccessfulPass < 1:
        homeSuccessfulPassPercent = 50
    else:
        homeSuccessfulPassPercent = int(homeSuccessfulPass/float(homeSuccessfulPass+awaySuccessfulPass)*100)
    awaySuccessfulPassPercent = 100 - homeSuccessfulPassPercent

    homePassRatioPercent = 0
    awayPassRatioPercent = 0
    if homePassRatio+awayPassRatio < 1:
        homePassRatioPercent = 50
    else:
        homePassRatioPercent = int(homePassRatio/float(homePassRatio+awayPassRatio)*100)
    awayPassRatioPercent = 100 - homePassRatioPercent

    homeTotalShotPercent = 0
    awayTotalShotPercent = 0
    if homeTotalShot+awayTotalShot < 1:
        homeTotalShotPercent = 50
    else:
        homeTotalShotPercent = int(homeTotalShot/float(homeTotalShot+awayTotalShot)*100)
    awayTotalShotPercent = 100 - homeTotalShotPercent

    homeSuccessfulShotPercent = 0
    awaySuccessfulShotPercent = 0
    if homeSuccessfulShot+awaySuccessfulShot < 1:
        homeSuccessfulShotPercent = 50
    else:
        homeSuccessfulShotPercent = int((homeSuccessfulShot/float(homeSuccessfulShot+awaySuccessfulShot))*100)
    awaySuccessfulShotPercent = 100 - homeSuccessfulShotPercent

    homeShotRatioPercent = 0
    awayShotRatioPercent = 0
    if homeShotRatio+awayShotRatio < 1:
        homeShotRatioPercent = 50
    else:
        homeShotRatioPercent = int(homeShotRatio/float(homeShotRatio+awayShotRatio)*100)
    awayShotRatioPercent = 100 - homeShotRatioPercent

    homeTotalCrossPercent = 0
    awayTotalCrossPercent = 0
    if homeTotalCross+awayTotalCross < 1:
        homeTotalCrossPercent = 50
    else:
        homeTotalCrossPercent = int(homeTotalCross/float(homeTotalCross+awayTotalCross)*100)
    awayTotalCrossPercent = 100 - homeTotalCrossPercent

    homeSuccessfulCrossPercent = 0
    awaySuccessfulCrossPercent = 0
    if homeSuccessfulCross+awaySuccessfulCross < 1:
        homeSuccessfulCrossPercent = 50
    else:
        homeSuccessfulCrossPercent = int(homeSuccessfulCross/float(homeSuccessfulCross+awaySuccessfulCross)*100)
    awaySuccessfulCrossPercent = 100 - homeSuccessfulCrossPercent

    homeCrossRatioPercent = 0
    awayCrossRatioPercent = 0
    if homeCrossRatio+awayCrossRatio < 1:
        homeCrossRatioPercent = 50
    else:
        homeCrossRatioPercent = int(homeCrossRatio/float(homeCrossRatio+awayCrossRatio)*100)
    awayCrossRatioPercent = 100 - homeCrossRatioPercent

    homeFoulPercent = 0
    awayFoulPercent = 0
    if homeFoul+awayFoul < 1:
        homeFoulPercent = 50
    else:
        homeFoulPercent = int(homeFoul/float(homeFoul+awayFoul)*100)
    awayFoulPercent = 100 - homeFoulPercent

    teamStatsDict = [] #holds team stats for team summaries
    dist = {} #temp array for storing

    dist = {'name':"Toplam Mesafe",'homeValue':homeDistance,'awayValue':awayDistance,'homePercent':homeDistancePercent,'awayPercent':awayDistancePercent,'addition':" m"}
    teamStatsDict.append(dist);

    dist = {'name':"Ortalama Hız",'homeValue':homeSpeed,'awayValue':awaySpeed,'homePercent':homeSpeedPercent,'awayPercent':awaySpeedPercent,'addition':" km/s"}
    teamStatsDict.append(dist);

    dist = {'name':"Şiddetli Koşu",'homeValue':homeHIR,'awayValue':awayHIR,'homePercent':homeHIRPercent,'awayPercent':awayHIRPercent,'addition':" m"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Pas",'homeValue':homeTotalPass,'awayValue':awayTotalPass,'homePercent':homeTotalPassPercent,'awayPercent':awayTotalPassPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Pas",'homeValue':homeSuccessfulPass,'awayValue':awaySuccessfulPass,'homePercent':homeSuccessfulPassPercent,'awayPercent':awaySuccessfulPassPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Pas Yüzdesi",'homeValue':homePassRatio,'awayValue':awayPassRatio,'homePercent':homePassRatioPercent,'awayPercent':awayPassRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Şut",'homeValue':homeTotalShot,'awayValue':awayTotalShot,'homePercent':homeTotalShotPercent,'awayPercent':awayTotalShotPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Şut",'homeValue':homeSuccessfulShot,'awayValue':awaySuccessfulShot,'homePercent':homeSuccessfulShotPercent,'awayPercent':awaySuccessfulShotPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Şut Yüzdesi",'homeValue':homeShotRatio,'awayValue':awayShotRatio,'homePercent':homeShotRatioPercent,'awayPercent':awayShotRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Orta",'homeValue':homeTotalCross,'awayValue':awayTotalCross,'homePercent':homeTotalCrossPercent,'awayPercent':awayTotalCrossPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Orta",'homeValue':homeSuccessfulCross,'awayValue':awaySuccessfulCross,'homePercent':homeSuccessfulCrossPercent,'awayPercent':awaySuccessfulCrossPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Orta Yüzdesi",'homeValue':homeCrossRatio,'awayValue':awayCrossRatio,'homePercent':homeCrossRatioPercent,'awayPercent':awayCrossRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Faul",'homeValue':homeFoul,'awayValue':awayFoul,'homePercent':homeFoulPercent,'awayPercent':awayFoulPercent,'addition':" %"}
    teamStatsDict.append(dist);

    #data for match narrations, used in "center" and "table" views
    narrationDict = get_match_narration(reqid)


    return render_to_response('virtual_stadium_before_match.html', {'teamStats':teamStatsDict,'narrations':narrationDict,'awayData':awayDataDict,'homeData':homeDataDict,'matchData':matchDataDict,'homeTeamId':homeTeamId,'awayTeamId':awayTeamId,'events':eventDict,'homeForm':homeFormDict,'awayForm':awayFormDict,'history':historicDict,'homeSquad':homeSquadDict,'awaySquad':awaySquadDict,'weeklist': weekList,'goals':goalDict,'matchInfo':infoDict,'weeks':weekDict,'currentWeek':currentWeek,'selectedMatch':str(reqid)})

@ensure_csrf_cookie
def center(request,reqid):
    #data for fixture, used for all views in match center
    data = {"leagueId": leagueId, "seasonId": seasonId}
    weeklist = service_request("GetFixture", data) # returns "data" field in response
    weekDict = [] # holds all fixture data
    currentWeek = 34 # if reqid(selected match id) not found current week is 34
    if len(weeklist) > 0 :
        for weekId in weeklist:
            week = weeklist[weekId]
            matches = [] #holds matches in week
            for matchId in week:
                if matchId == "weekStatus":
                    status = week[matchId]
                else:
                    #if requested match is found, that week is current week
                    if(matchId==str(reqid)):
                        currentWeek = weekId
                        #add matches
                    matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':week[matchId][7],'awayTeamId':week[matchId][8],'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
                #add weeks
            weekDict.append({'weekId':int(weekId),'status':status,'matches':matches})

    #data for match info, used for all views in match center
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchInfo", data) # returns "data" field in response
    infoDict = [] #holds match info data
    homeTeamId = 0 # home team id of current match
    awayTeamId = 0 # away team id of current match
    if len(datalist) > 0 :
        for x in datalist: #this list is single item list which holds match info only
            homeTeamId = x[5] #set home team id
            awayTeamId = x[6] #set away team id
            infoDict.append({'weekId':x[0],'matchId':x[1],'status':x[2],'homeTeam':x[3],'awayTeam':x[4],'homeTeamId':x[5],'awayTeamId':x[6],'homeTeamScore':int(x[7] or 0),'awayTeamScore':int(x[8] or 0),'date':x[9],'time':x[10],'liveTime':x[11],'referee':x[12],'stadium':x[13]})

    #   data for match goals, used for all views in match center
    #
    #   maç özeti ve diğer maç videoları buraya eklenmeli, yapı değişikliği olacak.
    #
    data = {"matchId":reqid}
    datalist = service_request("GetGoalVideos", data) # returns "data" field in response
    goalDict = [] #holds goal video data
    if len(datalist) > 0 :
        for x in datalist:
            goalDict.append({'teamId':x[0],'playerId':x[1],'playerName':x[2],'min':x[3],'goalLink':x[4]})

    # data for team squads, used in all views in match center
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchSquad", data)

    homeSquadDict = [] #holds home team squad
    awaySquadDict = [] #holds away team squad

    if len(datalist) > 0 :
        for playerId in datalist:
            playerEvents = [] #holds player events
            playerData = [] #holds player data(name,number, etc..)
            for x in datalist[playerId]:
                if x == "data":
                    playerData = datalist[playerId][x]
                elif x == "events":
                    playerEvents = datalist[playerId][x]

            eventDict = [] #holds player events
            for event in playerEvents:
                #add events
                eventDict.append({'eventType':event[0],'matchTime':event[1],'teamId':event[2],'playerId':int(event[3]),'playerIdIn':event[4],'jerseyNumber':event[5],'jerseyNumberIn':event[6]})

            #add player into corresponding team squads
            if(playerData[3] == homeTeamId):
                homeSquadDict.append({'playerId':int(playerId),'playerName':playerData[0],'jerseyNumber':playerData[1],'eleven':playerData[2],'playPosition':playerData[4],'playerEvents':eventDict})
            elif(playerData[3] == awayTeamId):
                awaySquadDict.append({'playerId':int(playerId),'playerName':playerData[0],'jerseyNumber':playerData[1],'eleven':playerData[2],'playPosition':playerData[4],'playerEvents':eventDict})

    # data for history of two team, used in "before" view only
    data = {"team1":homeTeamId,"team2":awayTeamId}
    datalist = service_request("GetHistoricData", data)

    pastMatches =[] #holds past matches
    if len(datalist) > 0 :
        #add past matches
        for match in datalist["pastMatches"]:
            pastMatches.append({'homeTeam':match[0],'awayTeam':match[1],'homeScore':match[2],'awayScore':match[3],'date':datetime.strptime(match[4],'%Y-%m-%d %H:%M:%S.0000000'),'referee':match[5],'stadium':match[6],'homeTeamId':match[8],'awayTeamId':match[9]})

        homeWin = 0 #home team win count
        awayWin = 0 #away team win count
        homeGoal = 0 #home team goal count
        awayGoal = 0 #away team goal count

        # for better visualisation 0 values interpreted as 1 in ratio calculations
        if datalist["homeWins"] == 0:
            homeWin = 1
        else:
            homeWin = datalist["homeWins"]

        if datalist["awayWins"] == 0:
            awayWin = 1
        else:
            awayWin = datalist["awayWins"]

        if datalist["homeGoals"] == 0:
            homeGoal = 1
        else:
            homeGoal = datalist["homeGoals"]

        if datalist["awayGoals"] == 0:
            awayGoal = 1
        else:
            awayGoal = datalist["awayGoals"]

        # ratio calculations for history graph
        # calculations made on 99 percent because graph borders causes problem on sizing
        homeWinRatio = int(99*homeWin/(homeWin+awayWin+datalist["draws"]))
        drawRatio = int(99*datalist["draws"]/(homeWin+awayWin+datalist["draws"]))
        awayWinRatio = 99 -(homeWinRatio+drawRatio)
        homeGoalRatio = int(99*homeGoal/(homeGoal+awayGoal))
        awayGoalRatio = 99-homeGoalRatio
        historicDict = [{'homeWins':datalist["homeWins"],'awayWins':datalist["awayWins"],'draws':datalist["draws"],'homeGoals':datalist["homeGoals"],'awayGoals':datalist["awayGoals"],'awayWinRatio':awayWinRatio,'homeWinRatio':homeWinRatio,'drawRatio':drawRatio,'homeGoalRatio':homeGoalRatio,'awayGoalRatio':awayGoalRatio,'pastMatches':pastMatches}]

    #data for home team form, used in "before" view only
    data = {"leagueId":leagueId,"seasonId":seasonId,"teamId":homeTeamId,"type":0,"weekId":currentWeek}
    datalist = service_request("GetTeamForm", data)

    homeFormDict = [] #holds home team form

    if len(datalist) > 0 :
        for match in datalist:
            win = 0 # 0-draw 1-win 2-lose
            #if home score > away score and the team is home team it is a win
            # also if away score > home score and the team is away team it is a win
            if (match[2] > match [3] and homeTeamId==match[4]) or (match[3] > match [2] and homeTeamId==match[5]):
                win=1
            # if score levels it is a draw
            elif match[2] == match [3]:
                win=0
            #else it is a lose
            else:
                win=2
            homeFormDict.append({'matchId':match[0],'matchName':match[1],'homeScore':match[2],'awayScore':match[3],'homeTeamId':match[4],'awayTeamId':match[5],'homeTeam':match[6],'awayTeam':match[7],'win':win})

    #data for away team form, used in "before" view only
    data = {"leagueId":leagueId,"seasonId":seasonId,"teamId":awayTeamId,"type":0,"weekId":currentWeek}
    datalist = service_request("GetTeamForm", data)

    awayFormDict = [] #holds away team form
    if len(datalist) > 0 :
        for match in datalist:
            win = 0 # 0-draw 1-win 2-lose
            #if home score > away score and the team is home team it is a win
            # also if away score > home score and the team is away team it is a win
            if (match[2] > match [3] and awayTeamId==match[4]) or (match[3] > match [2] and awayTeamId==match[5]):
                win=1
            # if score levels it is a draw
            elif match[2] == match [3]:
                win=0
            #else it is a lose
            else:
                win=2
            awayFormDict.append({'matchId':match[0],'matchName':match[1],'homeScore':match[2],'awayScore':match[3],'homeTeamId':match[4],'awayTeamId':match[5],'homeTeam':match[6],'awayTeam':match[7],'win':win})

    #data for match events in the game, used in "center" and "table" views
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchEvents", data)

    eventDict = [] #holds match events
    if len(datalist) > 0 :
        for event in datalist:
            eventDict.append({'type':event[0],'min':event[1],'teamId':int(event[2]),'playerId':event[3],'playerIdIn':event[4],'jerseyNumber':event[5],'jerseyNumberIn':event[6]})

    #data of all match(distance,pass,shot,cross,faul, etc..), used in all views
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchData", data)

    matchDataDict = [] #stores all players in the match
    homeDataDict = []  #stores only home players
    awayDataDict = [] #stores only away players

    #self explanatory
    #corners, offsides, penalties and cards should be added
    homeDistance = 0
    awayDistance = 0
    homeSpeed = 0
    awaySpeed = 0
    homeHIR = 0
    awayHIR = 0
    homeTotalPass = 0
    awayTotalPass = 0
    homeSuccessfulPass = 0
    awaySuccessfulPass = 0

    homeTotalShot = 0
    awayTotalShot = 0
    homeSuccessfulShot = 0
    awaySuccessfulShot = 0

    homeTotalCross = 0
    awayTotalCross = 0
    homeSuccessfulCross = 0
    awaySuccessfulCross = 0

    homeFoul = 0
    awayFoul = 0

    if len(datalist) > 0 :
        for dat in datalist:
            #add all data into match data
            matchDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
            if dat[0] == homeTeamId:

                #calculate home team totals
                homeDistance += int(dat[4] or 0)
                homeSpeed += int(dat[5] or 0)
                homeHIR += int(dat[6] or 0)
                homeTotalPass += int(dat[7] or 0)
                homeSuccessfulPass += int(dat[8] or 0)
                homeTotalShot += int(dat[9] or 0)
                homeSuccessfulShot += int(dat[10] or 0)
                homeTotalCross += int(dat[11] or 0)
                homeSuccessfulCross += int(dat[12] or 0)
                homeFoul += int(dat[13] or 0)

                #add home team players
                homeDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
            elif dat[0] == awayTeamId:

                #calculate away team totals
                awayDistance += int(dat[4] or 0)
                awaySpeed += int(dat[5] or 0)
                awayHIR += int(dat[6] or 0)
                awayTotalPass += int(dat[7] or 0)
                awaySuccessfulPass += int(dat[8] or 0)
                awayTotalShot += int(dat[9] or 0)
                awaySuccessfulShot += int(dat[10] or 0)
                awayTotalCross += int(dat[11] or 0)
                awaySuccessfulCross += int(dat[12] or 0)
                awayFoul += int(dat[13] or 0)
                #add away team players
                awayDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})

    #speed should be divided by player count
    #! this will not be displayed
    homeSpeed /= int(len(homeDataDict) or 1)
    awaySpeed /= int(len(awayDataDict) or 1)

    #ratios calculations
    homePassRatio = int(homeSuccessfulPass/float(homeTotalPass or 1) * 100)
    awayPassRatio = int(awaySuccessfulPass/float(awayTotalPass or 1) * 100)

    homeShotRatio = int(homeSuccessfulShot/float(homeTotalShot or 1) * 100)
    awayShotRatio = int(awaySuccessfulShot/float(awayTotalShot or 1) * 100)

    homeCrossRatio = int(homeSuccessfulCross/float(homeTotalCross or 1) * 100)
    awayCrossRatio = int(awaySuccessfulCross/float(awayTotalCross or 1) * 100)

    #percent calculations made for graphs,
    #this graphs will be changed due to last Lig Tv meeting
    #most of the percents will be not necessary
    #if data is zero percents are set to 50%

    homeDistancePercent = 0
    awayDistancePercent = 0
    if homeDistance+awayDistance < 1:
        homeDistancePercent = 50
    else:
        homeDistancePercent = int(homeDistance/float(homeDistance+awayDistance)*100)
    awayDistancePercent = 100 - homeDistancePercent

    homeSpeedPercent = 0
    awaySpeedPercent = 0
    if homeSpeed+awaySpeed < 1:
        homeSpeedPercent = 50
    else:
        homeSpeedPercent = int(homeSpeed/float(homeSpeed+awaySpeed)*100)
    awaySpeedPercent = 100 - homeSpeedPercent

    homeHIRPercent = 0
    awayHIRPercent = 0
    if homeHIR+awayHIR < 1:
        homeHIRPercent = 50
    else:
        homeHIRPercent = int(homeHIR/float(homeHIR+awayHIR)*100)
    awayHIRPercent = 100 - homeHIRPercent

    homeTotalPassPercent = 0
    awayTotalPassPercent = 0
    if homeTotalPass+awayTotalPass < 1:
        homeTotalPassPercent = 50
    else:
        homeTotalPassPercent = int(homeTotalPass/float(homeTotalPass+awayTotalPass)*100)
    awayTotalPassPercent = 100 - homeTotalPassPercent

    homeSuccessfulPassPercent = 0
    awaySuccessfulPassPercent = 0
    if homeSuccessfulPass+awaySuccessfulPass < 1:
        homeSuccessfulPassPercent = 50
    else:
        homeSuccessfulPassPercent = int(homeSuccessfulPass/float(homeSuccessfulPass+awaySuccessfulPass)*100)
    awaySuccessfulPassPercent = 100 - homeSuccessfulPassPercent

    homePassRatioPercent = 0
    awayPassRatioPercent = 0
    if homePassRatio+awayPassRatio < 1:
        homePassRatioPercent = 50
    else:
        homePassRatioPercent = int(homePassRatio/float(homePassRatio+awayPassRatio)*100)
    awayPassRatioPercent = 100 - homePassRatioPercent

    homeTotalShotPercent = 0
    awayTotalShotPercent = 0
    if homeTotalShot+awayTotalShot < 1:
        homeTotalShotPercent = 50
    else:
        homeTotalShotPercent = int(homeTotalShot/float(homeTotalShot+awayTotalShot)*100)
    awayTotalShotPercent = 100 - homeTotalShotPercent

    homeSuccessfulShotPercent = 0
    awaySuccessfulShotPercent = 0
    if homeSuccessfulShot+awaySuccessfulShot < 1:
        homeSuccessfulShotPercent = 50
    else:
        homeSuccessfulShotPercent = int((homeSuccessfulShot/float(homeSuccessfulShot+awaySuccessfulShot))*100)
    awaySuccessfulShotPercent = 100 - homeSuccessfulShotPercent

    homeShotRatioPercent = 0
    awayShotRatioPercent = 0
    if homeShotRatio+awayShotRatio < 1:
        homeShotRatioPercent = 50
    else:
        homeShotRatioPercent = int(homeShotRatio/float(homeShotRatio+awayShotRatio)*100)
    awayShotRatioPercent = 100 - homeShotRatioPercent

    homeTotalCrossPercent = 0
    awayTotalCrossPercent = 0
    if homeTotalCross+awayTotalCross < 1:
        homeTotalCrossPercent = 50
    else:
        homeTotalCrossPercent = int(homeTotalCross/float(homeTotalCross+awayTotalCross)*100)
    awayTotalCrossPercent = 100 - homeTotalCrossPercent

    homeSuccessfulCrossPercent = 0
    awaySuccessfulCrossPercent = 0
    if homeSuccessfulCross+awaySuccessfulCross < 1:
        homeSuccessfulCrossPercent = 50
    else:
        homeSuccessfulCrossPercent = int(homeSuccessfulCross/float(homeSuccessfulCross+awaySuccessfulCross)*100)
    awaySuccessfulCrossPercent = 100 - homeSuccessfulCrossPercent

    homeCrossRatioPercent = 0
    awayCrossRatioPercent = 0
    if homeCrossRatio+awayCrossRatio < 1:
        homeCrossRatioPercent = 50
    else:
        homeCrossRatioPercent = int(homeCrossRatio/float(homeCrossRatio+awayCrossRatio)*100)
    awayCrossRatioPercent = 100 - homeCrossRatioPercent

    homeFoulPercent = 0
    awayFoulPercent = 0
    if homeFoul+awayFoul < 1:
        homeFoulPercent = 50
    else:
        homeFoulPercent = int(homeFoul/float(homeFoul+awayFoul)*100)
    awayFoulPercent = 100 - homeFoulPercent

    teamStatsDict = [] #holds team stats for team summaries
    dist = {} #temp array for storing

    dist = {'name':"Toplam Mesafe",'homeValue':homeDistance,'awayValue':awayDistance,'homePercent':homeDistancePercent,'awayPercent':awayDistancePercent,'addition':" m"}
    teamStatsDict.append(dist);

    dist = {'name':"Ortalama Hız",'homeValue':homeSpeed,'awayValue':awaySpeed,'homePercent':homeSpeedPercent,'awayPercent':awaySpeedPercent,'addition':" km/s"}
    teamStatsDict.append(dist);

    dist = {'name':"Şiddetli Koşu",'homeValue':homeHIR,'awayValue':awayHIR,'homePercent':homeHIRPercent,'awayPercent':awayHIRPercent,'addition':" m"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Pas",'homeValue':homeTotalPass,'awayValue':awayTotalPass,'homePercent':homeTotalPassPercent,'awayPercent':awayTotalPassPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Pas",'homeValue':homeSuccessfulPass,'awayValue':awaySuccessfulPass,'homePercent':homeSuccessfulPassPercent,'awayPercent':awaySuccessfulPassPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Pas Yüzdesi",'homeValue':homePassRatio,'awayValue':awayPassRatio,'homePercent':homePassRatioPercent,'awayPercent':awayPassRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Şut",'homeValue':homeTotalShot,'awayValue':awayTotalShot,'homePercent':homeTotalShotPercent,'awayPercent':awayTotalShotPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Şut",'homeValue':homeSuccessfulShot,'awayValue':awaySuccessfulShot,'homePercent':homeSuccessfulShotPercent,'awayPercent':awaySuccessfulShotPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Şut Yüzdesi",'homeValue':homeShotRatio,'awayValue':awayShotRatio,'homePercent':homeShotRatioPercent,'awayPercent':awayShotRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Orta",'homeValue':homeTotalCross,'awayValue':awayTotalCross,'homePercent':homeTotalCrossPercent,'awayPercent':awayTotalCrossPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Orta",'homeValue':homeSuccessfulCross,'awayValue':awaySuccessfulCross,'homePercent':homeSuccessfulCrossPercent,'awayPercent':awaySuccessfulCrossPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Orta Yüzdesi",'homeValue':homeCrossRatio,'awayValue':awayCrossRatio,'homePercent':homeCrossRatioPercent,'awayPercent':awayCrossRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Faul",'homeValue':homeFoul,'awayValue':awayFoul,'homePercent':homeFoulPercent,'awayPercent':awayFoulPercent,'addition':" %"}
    teamStatsDict.append(dist);

    #data for match narrations, used in "center" and "table" views

    narrationDict = get_match_narration(reqid)


    return render_to_response('virtual_stadium.html', {'teamStats':teamStatsDict,'narrations':narrationDict,'awayData':awayDataDict,'homeData':homeDataDict,'matchData':matchDataDict,'homeTeamId':homeTeamId,'awayTeamId':awayTeamId,'events':eventDict,'homeForm':homeFormDict,'awayForm':awayFormDict,'history':historicDict,'homeSquad':homeSquadDict,'awaySquad':awaySquadDict,'weeklist': weekList,'goals':goalDict,'matchInfo':infoDict,'weeks':weekDict,'currentWeek':currentWeek,'selectedMatch':str(reqid)})

#match center "Maç Tahtası"
@ensure_csrf_cookie
def table(request,reqid):
    #data for fixture, used for all views in match center
    data = {"leagueId": leagueId, "seasonId": seasonId}
    weeklist = service_request("GetFixture", data) # returns "data" field in response
    weekDict = [] # holds all fixture data
    currentWeek = 34 # if reqid(selected match id) not found current week is 34
    if len(weeklist) > 0 :
        for weekId in weeklist:
            week = weeklist[weekId]
            matches = [] #holds matches in week
            for matchId in week:
                if matchId == "weekStatus":
                    status = week[matchId]
                else:
                    #if requested match is found, that week is current week
                    if(matchId==str(reqid)):
                        currentWeek = weekId
                        #add matches
                    matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':week[matchId][7],'awayTeamId':week[matchId][8],'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
                #add weeks
            weekDict.append({'weekId':int(weekId),'status':status,'matches':matches})

    #data for match info, used for all views in match center
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchInfo", data) # returns "data" field in response
    infoDict = [] #holds match info data
    homeTeamId = 0 # home team id of current match
    awayTeamId = 0 # away team id of current match
    if len(datalist) > 0 :
        for x in datalist: #this list is single item list which holds match info only
            homeTeamId = x[5] #set home team id
            awayTeamId = x[6] #set away team id
            infoDict.append({'weekId':x[0],'matchId':x[1],'status':x[2],'homeTeam':x[3],'awayTeam':x[4],'homeTeamId':x[5],'awayTeamId':x[6],'homeTeamScore':int(x[7] or 0),'awayTeamScore':int(x[8] or 0),'date':x[9],'time':x[10],'liveTime':x[11],'referee':x[12],'stadium':x[13]})

    #   data for match goals, used for all views in match center
    #
    #   maç özeti ve diğer maç videoları buraya eklenmeli, yapı değişikliği olacak.
    #
    data = {"matchId":reqid}
    datalist = service_request("GetGoalVideos", data) # returns "data" field in response
    goalDict = [] #holds goal video data
    if len(datalist) > 0 :
        for x in datalist:
            goalDict.append({'teamId':x[0],'playerId':x[1],'playerName':x[2],'min':x[3],'goalLink':x[4]})

    # data for team squads, used in all views in match center
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchSquad", data)

    homeSquadDict = [] #holds home team squad
    awaySquadDict = [] #holds away team squad

    if len(datalist) > 0 :
        for playerId in datalist:
            playerEvents = [] #holds player events
            playerData = [] #holds player data(name,number, etc..)
            for x in datalist[playerId]:
                if x == "data":
                    playerData = datalist[playerId][x]
                elif x == "events":
                    playerEvents = datalist[playerId][x]

            eventDict = [] #holds player events
            for event in playerEvents:
                #add events
                eventDict.append({'eventType':event[0],'matchTime':event[1],'teamId':event[2],'playerId':int(event[3]),'playerIdIn':event[4],'jerseyNumber':event[5],'jerseyNumberIn':event[6]})

            #add player into corresponding team squads
            if(playerData[3] == homeTeamId):
                homeSquadDict.append({'playerId':int(playerId),'playerName':playerData[0],'jerseyNumber':playerData[1],'eleven':playerData[2],'playPosition':playerData[4],'playerEvents':eventDict})
            elif(playerData[3] == awayTeamId):
                awaySquadDict.append({'playerId':int(playerId),'playerName':playerData[0],'jerseyNumber':playerData[1],'eleven':playerData[2],'playPosition':playerData[4],'playerEvents':eventDict})

    # data for history of two team, used in "before" view only
    data = {"team1":homeTeamId,"team2":awayTeamId}
    datalist = service_request("GetHistoricData", data)

    pastMatches =[] #holds past matches
    if len(datalist) > 0 :
        #add past matches
        for match in datalist["pastMatches"]:
            pastMatches.append({'homeTeam':match[0],'awayTeam':match[1],'homeScore':match[2],'awayScore':match[3],'date':datetime.strptime(match[4],'%Y-%m-%d %H:%M:%S.0000000'),'referee':match[5],'stadium':match[6],'homeTeamId':match[8],'awayTeamId':match[9]})

        homeWin = 0 #home team win count
        awayWin = 0 #away team win count
        homeGoal = 0 #home team goal count
        awayGoal = 0 #away team goal count

        # for better visualisation 0 values interpreted as 1 in ratio calculations
        if datalist["homeWins"] == 0:
            homeWin = 1
        else:
            homeWin = datalist["homeWins"]

        if datalist["awayWins"] == 0:
            awayWin = 1
        else:
            awayWin = datalist["awayWins"]

        if datalist["homeGoals"] == 0:
            homeGoal = 1
        else:
            homeGoal = datalist["homeGoals"]

        if datalist["awayGoals"] == 0:
            awayGoal = 1
        else:
            awayGoal = datalist["awayGoals"]

        # ratio calculations for history graph
        # calculations made on 99 percent because graph borders causes problem on sizing
        homeWinRatio = int(99*homeWin/(homeWin+awayWin+datalist["draws"]))
        drawRatio = int(99*datalist["draws"]/(homeWin+awayWin+datalist["draws"]))
        awayWinRatio = 99 -(homeWinRatio+drawRatio)
        homeGoalRatio = int(99*homeGoal/(homeGoal+awayGoal))
        awayGoalRatio = 99-homeGoalRatio
        historicDict = [{'homeWins':datalist["homeWins"],'awayWins':datalist["awayWins"],'draws':datalist["draws"],'homeGoals':datalist["homeGoals"],'awayGoals':datalist["awayGoals"],'awayWinRatio':awayWinRatio,'homeWinRatio':homeWinRatio,'drawRatio':drawRatio,'homeGoalRatio':homeGoalRatio,'awayGoalRatio':awayGoalRatio,'pastMatches':pastMatches}]

    #data for home team form, used in "before" view only
    data = {"leagueId":leagueId,"seasonId":seasonId,"teamId":homeTeamId,"type":0,"weekId":currentWeek}
    datalist = service_request("GetTeamForm", data)

    homeFormDict = [] #holds home team form

    if len(datalist) > 0 :
        for match in datalist:
            win = 0 # 0-draw 1-win 2-lose
            #if home score > away score and the team is home team it is a win
            # also if away score > home score and the team is away team it is a win
            if (match[2] > match [3] and homeTeamId==match[4]) or (match[3] > match [2] and homeTeamId==match[5]):
                win=1
            # if score levels it is a draw
            elif match[2] == match [3]:
                win=0
            #else it is a lose
            else:
                win=2
            homeFormDict.append({'matchId':match[0],'matchName':match[1],'homeScore':match[2],'awayScore':match[3],'homeTeamId':match[4],'awayTeamId':match[5],'homeTeam':match[6],'awayTeam':match[7],'win':win})

    #data for away team form, used in "before" view only
    data = {"leagueId":leagueId,"seasonId":seasonId,"teamId":awayTeamId,"type":0,"weekId":currentWeek}
    datalist = service_request("GetTeamForm", data)

    awayFormDict = [] #holds away team form
    if len(datalist) > 0 :
        for match in datalist:
            win = 0 # 0-draw 1-win 2-lose
            #if home score > away score and the team is home team it is a win
            # also if away score > home score and the team is away team it is a win
            if (match[2] > match [3] and awayTeamId==match[4]) or (match[3] > match [2] and awayTeamId==match[5]):
                win=1
            # if score levels it is a draw
            elif match[2] == match [3]:
                win=0
            #else it is a lose
            else:
                win=2
            awayFormDict.append({'matchId':match[0],'matchName':match[1],'homeScore':match[2],'awayScore':match[3],'homeTeamId':match[4],'awayTeamId':match[5],'homeTeam':match[6],'awayTeam':match[7],'win':win})

    #data for match events in the game, used in "center" and "table" views
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchEvents", data)

    eventDict = [] #holds match events
    if len(datalist) > 0 :
        for event in datalist:
            eventDict.append({'type':event[0],'min':event[1],'teamId':int(event[2]),'playerId':event[3],'playerIdIn':event[4],'jerseyNumber':event[5],'jerseyNumberIn':event[6]})

    #data of all match(distance,pass,shot,cross,faul, etc..), used in all views
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":reqid}
    datalist = service_request("GetMatchData", data)

    matchDataDict = [] #stores all players in the match
    homeDataDict = []  #stores only home players
    awayDataDict = [] #stores only away players

    #self explanatory
    #corners, offsides, penalties and cards should be added
    homeDistance = 0
    awayDistance = 0
    homeSpeed = 0
    awaySpeed = 0
    homeHIR = 0
    awayHIR = 0
    homeTotalPass = 0
    awayTotalPass = 0
    homeSuccessfulPass = 0
    awaySuccessfulPass = 0

    homeTotalShot = 0
    awayTotalShot = 0
    homeSuccessfulShot = 0
    awaySuccessfulShot = 0

    homeTotalCross = 0
    awayTotalCross = 0
    homeSuccessfulCross = 0
    awaySuccessfulCross = 0

    homeFoul = 0
    awayFoul = 0

    if len(datalist) > 0 :
        for dat in datalist:
            #add all data into match data
            matchDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
            if dat[0] == homeTeamId:

                #calculate home team totals
                homeDistance += int(dat[4] or 0)
                homeSpeed += int(dat[5] or 0)
                homeHIR += int(dat[6] or 0)
                homeTotalPass += int(dat[7] or 0)
                homeSuccessfulPass += int(dat[8] or 0)
                homeTotalShot += int(dat[9] or 0)
                homeSuccessfulShot += int(dat[10] or 0)
                homeTotalCross += int(dat[11] or 0)
                homeSuccessfulCross += int(dat[12] or 0)
                homeFoul += int(dat[13] or 0)

                #add home team players
                homeDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
            elif dat[0] == awayTeamId:

                #calculate away team totals
                awayDistance += int(dat[4] or 0)
                awaySpeed += int(dat[5] or 0)
                awayHIR += int(dat[6] or 0)
                awayTotalPass += int(dat[7] or 0)
                awaySuccessfulPass += int(dat[8] or 0)
                awayTotalShot += int(dat[9] or 0)
                awaySuccessfulShot += int(dat[10] or 0)
                awayTotalCross += int(dat[11] or 0)
                awaySuccessfulCross += int(dat[12] or 0)
                awayFoul += int(dat[13] or 0)
                #add away team players
                awayDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})

    #speed should be divided by player count
    #! this will not be displayed
    homeSpeed /= int(len(homeDataDict) or 1)
    awaySpeed /= int(len(awayDataDict) or 1)

    #ratios calculations
    homePassRatio = int(homeSuccessfulPass/float(homeTotalPass or 1) * 100)
    awayPassRatio = int(awaySuccessfulPass/float(awayTotalPass or 1) * 100)

    homeShotRatio = int(homeSuccessfulShot/float(homeTotalShot or 1) * 100)
    awayShotRatio = int(awaySuccessfulShot/float(awayTotalShot or 1) * 100)

    homeCrossRatio = int(homeSuccessfulCross/float(homeTotalCross or 1) * 100)
    awayCrossRatio = int(awaySuccessfulCross/float(awayTotalCross or 1) * 100)

    #percent calculations made for graphs,
    #this graphs will be changed due to last Lig Tv meeting
    #most of the percents will be not necessary
    #if data is zero percents are set to 50%

    homeDistancePercent = 0
    awayDistancePercent = 0
    if homeDistance+awayDistance < 1:
        homeDistancePercent = 50
    else:
        homeDistancePercent = int(homeDistance/float(homeDistance+awayDistance)*100)
    awayDistancePercent = 100 - homeDistancePercent

    homeSpeedPercent = 0
    awaySpeedPercent = 0
    if homeSpeed+awaySpeed < 1:
        homeSpeedPercent = 50
    else:
        homeSpeedPercent = int(homeSpeed/float(homeSpeed+awaySpeed)*100)
    awaySpeedPercent = 100 - homeSpeedPercent

    homeHIRPercent = 0
    awayHIRPercent = 0
    if homeHIR+awayHIR < 1:
        homeHIRPercent = 50
    else:
        homeHIRPercent = int(homeHIR/float(homeHIR+awayHIR)*100)
    awayHIRPercent = 100 - homeHIRPercent

    homeTotalPassPercent = 0
    awayTotalPassPercent = 0
    if homeTotalPass+awayTotalPass < 1:
        homeTotalPassPercent = 50
    else:
        homeTotalPassPercent = int(homeTotalPass/float(homeTotalPass+awayTotalPass)*100)
    awayTotalPassPercent = 100 - homeTotalPassPercent

    homeSuccessfulPassPercent = 0
    awaySuccessfulPassPercent = 0
    if homeSuccessfulPass+awaySuccessfulPass < 1:
        homeSuccessfulPassPercent = 50
    else:
        homeSuccessfulPassPercent = int(homeSuccessfulPass/float(homeSuccessfulPass+awaySuccessfulPass)*100)
    awaySuccessfulPassPercent = 100 - homeSuccessfulPassPercent

    homePassRatioPercent = 0
    awayPassRatioPercent = 0
    if homePassRatio+awayPassRatio < 1:
        homePassRatioPercent = 50
    else:
        homePassRatioPercent = int(homePassRatio/float(homePassRatio+awayPassRatio)*100)
    awayPassRatioPercent = 100 - homePassRatioPercent

    homeTotalShotPercent = 0
    awayTotalShotPercent = 0
    if homeTotalShot+awayTotalShot < 1:
        homeTotalShotPercent = 50
    else:
        homeTotalShotPercent = int(homeTotalShot/float(homeTotalShot+awayTotalShot)*100)
    awayTotalShotPercent = 100 - homeTotalShotPercent

    homeSuccessfulShotPercent = 0
    awaySuccessfulShotPercent = 0
    if homeSuccessfulShot+awaySuccessfulShot < 1:
        homeSuccessfulShotPercent = 50
    else:
        homeSuccessfulShotPercent = int((homeSuccessfulShot/float(homeSuccessfulShot+awaySuccessfulShot))*100)
    awaySuccessfulShotPercent = 100 - homeSuccessfulShotPercent

    homeShotRatioPercent = 0
    awayShotRatioPercent = 0
    if homeShotRatio+awayShotRatio < 1:
        homeShotRatioPercent = 50
    else:
        homeShotRatioPercent = int(homeShotRatio/float(homeShotRatio+awayShotRatio)*100)
    awayShotRatioPercent = 100 - homeShotRatioPercent

    homeTotalCrossPercent = 0
    awayTotalCrossPercent = 0
    if homeTotalCross+awayTotalCross < 1:
        homeTotalCrossPercent = 50
    else:
        homeTotalCrossPercent = int(homeTotalCross/float(homeTotalCross+awayTotalCross)*100)
    awayTotalCrossPercent = 100 - homeTotalCrossPercent

    homeSuccessfulCrossPercent = 0
    awaySuccessfulCrossPercent = 0
    if homeSuccessfulCross+awaySuccessfulCross < 1:
        homeSuccessfulCrossPercent = 50
    else:
        homeSuccessfulCrossPercent = int(homeSuccessfulCross/float(homeSuccessfulCross+awaySuccessfulCross)*100)
    awaySuccessfulCrossPercent = 100 - homeSuccessfulCrossPercent

    homeCrossRatioPercent = 0
    awayCrossRatioPercent = 0
    if homeCrossRatio+awayCrossRatio < 1:
        homeCrossRatioPercent = 50
    else:
        homeCrossRatioPercent = int(homeCrossRatio/float(homeCrossRatio+awayCrossRatio)*100)
    awayCrossRatioPercent = 100 - homeCrossRatioPercent

    homeFoulPercent = 0
    awayFoulPercent = 0
    if homeFoul+awayFoul < 1:
        homeFoulPercent = 50
    else:
        homeFoulPercent = int(homeFoul/float(homeFoul+awayFoul)*100)
    awayFoulPercent = 100 - homeFoulPercent

    teamStatsDict = [] #holds team stats for team summaries
    dist = {} #temp array for storing

    dist = {'name':"Toplam Mesafe",'homeValue':homeDistance,'awayValue':awayDistance,'homePercent':homeDistancePercent,'awayPercent':awayDistancePercent,'addition':" m"}
    teamStatsDict.append(dist);

    dist = {'name':"Ortalama Hız",'homeValue':homeSpeed,'awayValue':awaySpeed,'homePercent':homeSpeedPercent,'awayPercent':awaySpeedPercent,'addition':" km/s"}
    teamStatsDict.append(dist);

    dist = {'name':"Şiddetli Koşu",'homeValue':homeHIR,'awayValue':awayHIR,'homePercent':homeHIRPercent,'awayPercent':awayHIRPercent,'addition':" m"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Pas",'homeValue':homeTotalPass,'awayValue':awayTotalPass,'homePercent':homeTotalPassPercent,'awayPercent':awayTotalPassPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Pas",'homeValue':homeSuccessfulPass,'awayValue':awaySuccessfulPass,'homePercent':homeSuccessfulPassPercent,'awayPercent':awaySuccessfulPassPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Pas Yüzdesi",'homeValue':homePassRatio,'awayValue':awayPassRatio,'homePercent':homePassRatioPercent,'awayPercent':awayPassRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Şut",'homeValue':homeTotalShot,'awayValue':awayTotalShot,'homePercent':homeTotalShotPercent,'awayPercent':awayTotalShotPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Şut",'homeValue':homeSuccessfulShot,'awayValue':awaySuccessfulShot,'homePercent':homeSuccessfulShotPercent,'awayPercent':awaySuccessfulShotPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Şut Yüzdesi",'homeValue':homeShotRatio,'awayValue':awayShotRatio,'homePercent':homeShotRatioPercent,'awayPercent':awayShotRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Toplam Orta",'homeValue':homeTotalCross,'awayValue':awayTotalCross,'homePercent':homeTotalCrossPercent,'awayPercent':awayTotalCrossPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Başarılı Orta",'homeValue':homeSuccessfulCross,'awayValue':awaySuccessfulCross,'homePercent':homeSuccessfulCrossPercent,'awayPercent':awaySuccessfulCrossPercent,'addition':""}
    teamStatsDict.append(dist);

    dist = {'name':"Orta Yüzdesi",'homeValue':homeCrossRatio,'awayValue':awayCrossRatio,'homePercent':homeCrossRatioPercent,'awayPercent':awayCrossRatioPercent,'addition':" %"}
    teamStatsDict.append(dist);

    dist = {'name':"Faul",'homeValue':homeFoul,'awayValue':awayFoul,'homePercent':homeFoulPercent,'awayPercent':awayFoulPercent,'addition':" %"}
    teamStatsDict.append(dist);

    #data for match narrations, used in "center" and "table" views
    narrationDict = get_match_narration(reqid)

    return render_to_response('virtual_stadium_board.html', {'teamStats':teamStatsDict,'narrations':narrationDict,'awayData':awayDataDict,'homeData':homeDataDict,'matchData':matchDataDict,'homeTeamId':homeTeamId,'awayTeamId':awayTeamId,'events':eventDict,'homeForm':homeFormDict,'awayForm':awayFormDict,'history':historicDict,'homeSquad':homeSquadDict,'awaySquad':awaySquadDict,'weeklist': weekList,'goals':goalDict,'matchInfo':infoDict,'weeks':weekDict,'currentWeek':currentWeek,'selectedMatch':str(reqid)})



def home(request,weekId):
    data = {"leagueId":leagueId,"seasonId":seasonId}
    list = service_request("GetWeeks", data)
    weekNumber = 0
    lastPlayed = 0
    for x in list:
        weekNumber = x[0]
        lastPlayed = x[1]
    i=1
    weekDict = []
    while(i<=weekNumber):
        weekDict.append(int(i))
        i = i+1

    standingDict = []
    data = {"leagueId":leagueId,"seasonId":seasonId,"type":0}
    datalist =  service_request("GetStandings",data)
    if len(datalist) > 0:
        for item in datalist:
            if int(item[0]) == int(weekId):
                standingDict.append({'teamId': int(item[1]), 'teamName': item[2],'played':int(item[3]), 'win':int(item[4]), 'draw':int(item[5]), 'lose':int(item[6]), 'score':int(item[7]), 'conceded' : int(item[8]), 'average':int(item[9]), 'points':int(item[10]), 'change': int(item[11])})

    data = {"leagueId": leagueId, "seasonId":seasonId}
    weeklist = service_request("GetFixture", data)
    fixtureDict = []
    if len(weeklist) > 0 :
        for week_id in weeklist:
            week = weeklist[week_id]
            matches = []
            for matchId in week:
                if matchId == "weekStatus":
                    status = week[matchId]
                else:
                    matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':week[matchId][7],'awayTeamId':week[matchId][8],'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
            fixtureDict.append({'weekId':int(week_id),'status':status,'matches':matches})

    return render_to_response('statshome.html', {'fixture':fixtureDict,'weekList':weekDict,'weekSelected': int(weekId),'lastPlayedWeek':int(lastPlayed), 'standing_list':standingDict, 'best_eleven_list':bestList})

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
    data = {"leagueId": leagueId, "seasonId": seasonId}
    datalist = service_request("GetTeams", data)
    teamDict = []
    if len(datalist) > 0:
        for x in datalist:
            teamDict.append({'teamId':x[0],'teamName':x[1]})

    data = {"teamId": num}
    datalist = service_request("GetTeamDetails", data)

    detailDict = []
    if len(datalist) > 0:
        for obj in datalist:
            detailDict.append( {'teamName':obj[0],'stadium':obj[1],'foundation':obj[2],'president':obj[3],'capacity':obj[4],'manager':obj[5],'website':obj[6],'leaguechamp':obj[7],'cupchamp':obj[8]})

    standingDict = []
    data = {"leagueId":leagueId,"seasonId":seasonId,"type":0}
    datalist =  service_request("GetStandings",data)
    if len(datalist) > 0:
        for item in datalist:
            if int(item[0]) == 34:
                standingDict.append({'teamId': int(item[1]), 'teamName': item[2],'played':int(item[3]), 'win':int(item[4]), 'draw':int(item[5]), 'lose':int(item[6]), 'score':int(item[7]), 'conceded' : int(item[8]), 'average':int(item[9]), 'points':int(item[10]), 'change': int(item[11])})

    data = {"leagueId": leagueId, "seasonId": seasonId, "teamId": num}
    datalist = service_request("GetTeamPlayers", data)
    playerDict =[]
    if len(datalist) > 0:
        for x in datalist:
            playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})

    data = {"leagueId": leagueId, "seasonId": seasonId}
    weeklist = service_request("GetFixture", data)
    fixtureDict = []
    if len(weeklist) > 0 :
        for week_id in weeklist:
            week = weeklist[week_id]
            matches = []
            for matchId in week:
                if matchId == "weekStatus":
                    status = week[matchId]
                else:
                    matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':int(week[matchId][7]),'awayTeamId':int(week[matchId][8]),'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
            fixtureDict.append({'weekId':int(week_id),'status':status,'matches':matches})

    return render_to_response('statsteam.html', {'fixture':fixtureDict,'s_list': s,'team_list': teamList, 'try_list':teamDict, 'details':detailDict,'players':playerDict, 'standing_list':standingDict, 'team_selected': int(num), 'player_list':playerList, 'weeklist': weekList,'best_eleven_list':bestList})


def league(request):
    return render_to_response('statsleague.html', {'weeklist': weekList , 'team_list': teamList, 'weeklist': weekList,'best_eleven_list':bestList})

@ensure_csrf_cookie
def playerx(request, num, player_id):

    data = {"leagueId": leagueId, "seasonId": seasonId,"playerId": player_id}
    datalist = service_request("GetPlayerDetails", data)

    detailDict = []
    if len(datalist) > 0:
        for obj in datalist:
            detailDict.append({'playerName':obj[0],'date':obj[1],'height':obj[2],'nation':obj[3],'cap':obj[4],'goal':obj[5],'teamId':obj[6],'teamName':obj[7]})

    data = {"leagueId": leagueId, "seasonId": seasonId, "teamId": num}
    datalist = service_request("GetTeamPlayers", data)

    playerDict =[]
    if len(datalist) > 0:
        for x in datalist:
            playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})

    data = {"leagueId": leagueId, "seasonId": seasonId}
    datalist = service_request("GetTeams", data)

    teamDict = []
    if len(datalist) > 0:
        for x in datalist:
            teamDict.append({'teamId':x[0],'teamName':x[1]})

    return render_to_response('statsplayer.html', {'p_id': int(player_id), 'details':detailDict, 'try_list':teamDict,'players':playerDict, 'team_selected': int(num), 'team_list': teamList, 'player_list':playerList, "best_eleven_list":bestList, 'weeklist': weekList})

def player3(request, num):

    data = {"leagueId": leagueId, "seasonId": seasonId, "teamId": num}
    datalist = service_request("GetTeamPlayers", data)

    playerDict =[]
    if len(datalist) > 0:
        for x in datalist:
            playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})

    data = {"leagueId": leagueId, "seasonId": seasonId}
    datalist = service_request("GetTeams", data)

    teamDict = []
    if len(datalist) > 0:
        for x in datalist:
            teamDict.append({'teamId':x[0],'teamName':x[1]})

    return render_to_response('playerselection.html', { 'team_selected': int(num), 'try_list':teamDict, 'team_list': teamList,'players':playerDict, 'player_list':playerList, "best_eleven_list":bestList, 'weeklist': weekList})

def summary(request):
    return render_to_response('matchsummary.html')

def compare(request):
    return render_to_response('statscompare.html')

def player(request):
    data = {"leagueId": leagueId, "seasonId": seasonId}
    datalist = service_request("GetTeams", data)

    teamDict = []
    if len(datalist) > 0:
        for x in datalist:
            teamDict.append({'teamId':x[0],'teamName':x[1]})

    return render_to_response('playerteamselection.html',{ 'best_eleven_list':bestList, 'weeklist': weekList, 'try_list':teamDict} )

@ensure_csrf_cookie
def chalkboard(request):
    return render_to_response('chalkboard.html')

@ensure_csrf_cookie
def radar_vebview(request, matchId):
    return render_to_response('radar_vebview.html')

def team2(request):
    data = {"leagueId": leagueId, "seasonId": seasonId}
    datalist = service_request("GetTeams", data)

    teamDict = []
    if len(datalist) > 0:
        for x in datalist:
            teamDict.append({'teamId':x[0],'teamName':x[1]})

    standingDict = []
    data = {"leagueId":leagueId,"seasonId":seasonId,"type":0}
    datalist =  service_request("GetStandings",data)
    if len(datalist) > 0:
        for item in datalist:
            if int(item[0]) == 34:
                standingDict.append({'teamId': int(item[1]), 'teamName': item[2],'played':int(item[3]), 'win':int(item[4]), 'draw':int(item[5]), 'lose':int(item[6]), 'score':int(item[7]), 'conceded' : int(item[8]), 'average':int(item[9]), 'points':int(item[10]), 'change': int(item[11])})


    return render_to_response('teamselection.html',{'standing_list':standingDict, 'weeklist':weekList,'try_list':teamDict} )

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
    data = {"leagueId":leagueId,"seasonId":seasonId,"matchId":match_id}
    list = service_request("GetMatchInfo", data)
    for x in list:
        if(x[1]=="1"):
            return HttpResponseRedirect("before")
        else:
            return HttpResponseRedirect("before")

