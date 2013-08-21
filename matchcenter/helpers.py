# -*- coding: utf-8 -*-
"""
Helper functions for match center views

author: Caner Turkmen
"""
from datetime import datetime
LEAGUE_ID = 1
SEASON_ID = 9064

from .utils import service_request

def get_match_narration(mid):
    """
    Fetches a python list of narration entries in a match

    :param mid: match id requested
    """
    data = {"matchId": mid}
    datalist = service_request("GetMatchNarration", data)
    narrationList = []
    for i in datalist:
        team_id = i.get("team")
        type_ = i.get("typeInt")
        text_ = i.get("text")
        minute_ = int(i.get("minute"))

        if text_ is not None:
            narrationList.append({'min':minute_,'teamId':team_id,'type':type_,'text':text_})

    return narrationList

def get_match_week(match_id):
    """
    Get week of a match

    :param match_id: self-explanatory
    """
    a = service_request("GetMatchInfo", {"matchId": match_id})

    try:
        return a[0][0]
    except: # match not found
        return None

def get_fixture(league_id, season_id, match_id):
    #data for fixture, used for all views in match center
    data = {"leagueId": league_id, "seasonId": season_id}
    weeklist = service_request("GetFixture", data) # returns "data" field in response

    weekDict = [] # holds all fixture data
    currentWeek = get_match_week(match_id) if get_match_week(match_id) else 34

    if len(weeklist) > 0 :
        for weekId in weeklist:
            week = weeklist[weekId]
            matches = [] #holds matches in week
            for matchId in week:
                if matchId == "weekStatus":
                    status = week[matchId]
                else:
                    matches.append({'matchId':matchId,'matchStatus':week[matchId][0],'homeTeam':week[matchId][1], 'homeTeamCond':week[matchId][2], 'homeTeamInt':week[matchId][3],'awayTeam':week[matchId][4],'awayTeamCond':week[matchId][5], 'awayTeamInt':week[matchId][6],'homeTeamId':week[matchId][7],'awayTeamId':week[matchId][8],'homeScore':week[matchId][9],'awayScore':week[matchId][10],'date':week[matchId][11],'liveTime':week[matchId][12],'referee':week[matchId][13],'stadium':week[matchId][14]})
                    #add weeks
            weekDict.append({'weekId':int(weekId),'status':status,'matches':matches})

    return weekDict, currentWeek

def get_match_info(match_id):
    data = {"matchId":match_id}
    datalist = service_request("GetMatchInfo", data) # returns "data" field in response

    homeTeamId = 0 # home team id of current match
    awayTeamId = 0 # away team id of current match
    if len(datalist) ==  0 :
        return homeTeamId, awayTeamId, []

    x = datalist[0]
    homeTeamId = x[5] #set home team id
    awayTeamId = x[6] #set away team id
    infoDict = {'weekId':x[0],'matchId':x[1],'status':x[2],'homeTeam':x[3],'awayTeam':x[4],'homeTeamId':x[5],'awayTeamId':x[6],'homeTeamScore':int(x[7] or 0),'awayTeamScore':int(x[8] or 0),'date':x[9],'time':x[10],'liveTime':x[11],'referee':x[12],'stadium':x[13]}

    return homeTeamId, awayTeamId, infoDict

def get_goal_videos(match_id):

    data = {"matchId":match_id}
    datalist = service_request("GetGoalVideos", data) # returns "data" field in response
    goalDict = [] #holds goal video data
    if len(datalist) > 0 :
        for x in datalist:
            goalDict.append({'teamId':x[0],'playerId':x[1],'playerName':x[2],'min':x[3],'goalLink':x[4]})

    return goalDict

def get_team_squads(match_id, homeTeamId, awayTeamId):
    data = {"matchId":match_id}
    datalist = service_request("GetMatchSquad", data)

    # if the list returns empty, return empty lists
    if len(datalist) == 0:
        return [], []

    homeSquadDict, awaySquadDict = [], [] #holds home team squad

    for playerId in datalist:
        playerEvents = datalist.get(playerId).get("events") #holds player events
        playerData = datalist.get(playerId).get("data") #holds player data (name,number, etc..)

        if playerEvents:
            eventDict = [{'eventType':event[0],
                          'matchTime':event[1],
                          'teamId':event[2],
                          'playerId':int(event[3]),
                          'playerIdIn':event[4],
                          'jerseyNumber':event[5],
                          'jerseyNumberIn':event[6]} for event in playerEvents]
        else:
            eventDict = []

        #add player into corresponding team squads
        playerTuple = {'playerId':int(playerId),
                       'playerName':playerData[0],
                       'jerseyNumber':playerData[1],
                       'eleven':playerData[2],
                       'playPosition':playerData[4],
                       'playerEvents':eventDict}

        if playerData[3] == homeTeamId:
            homeSquadDict.append(playerTuple)
        elif playerData[3] == awayTeamId:
            awaySquadDict.append(playerTuple)

    return homeSquadDict, awaySquadDict

def get_history(homeTeamId, awayTeamId):
    data = {"team1":homeTeamId,"team2":awayTeamId}
    datalist = service_request("GetHistoricData", data)

    if len(datalist) == 0 :
        return []

    #add past matches
    pastMatches = [{'homeTeam':match[0],
                    'awayTeam':match[1],
                    'homeScore':match[2],
                    'awayScore':match[3],
                    'date':datetime.strptime(match[4],'%Y-%m-%d %H:%M:%S.0000000'),
                    'referee':match[5],
                    'stadium':match[6],
                    'homeTeamId':match[8],
                    'awayTeamId':match[9]} for match in datalist.get("pastMatches")]

    # lambda function for making ==0 then 1 check on homewin/awaywin comparison
    beautify_matchup = lambda x : datalist.get(x) if datalist.get(x) > 0 else 1

    homeWin = beautify_matchup("homeWins") #home team win count
    awayWin = beautify_matchup("awayWins") #away team win count
    homeGoal = beautify_matchup("homeGoals") #home team goal count
    awayGoal = beautify_matchup("awayGoals") #away team goal count

    # ratio calculations for history graph
    # calculations made on 99 percent because graph borders causes problem on sizing

    homeWinRatio = int(99*homeWin/(homeWin+awayWin+datalist["draws"]))
    drawRatio = int(99*datalist["draws"]/(homeWin+awayWin+datalist["draws"]))
    awayWinRatio = 99 - (homeWinRatio+drawRatio)

    homeGoalRatio = int(99*homeGoal/(homeGoal+awayGoal))
    awayGoalRatio = 99-homeGoalRatio

    historicDict = {'homeWins':datalist.get("homeWins"),
                     'awayWins':datalist.get("awayWins"),
                     'draws':datalist.get("draws"),
                     'homeGoals':datalist.get("homeGoals"),
                     'awayGoals':datalist.get("awayGoals"),
                     'awayWinRatio':awayWinRatio,
                     'homeWinRatio':homeWinRatio,
                     'drawRatio':drawRatio,
                     'homeGoalRatio':homeGoalRatio,
                     'awayGoalRatio':awayGoalRatio,
                     'pastMatches':pastMatches}

    return historicDict

def get_team_forms(homeTeamId, awayTeamId, currentWeek):
    data = {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"teamId":homeTeamId,"type":0,"weekId":currentWeek}
    homelist = service_request("GetTeamForm", data)

    data["teamId"] = awayTeamId
    awaylist = service_request("GetTeamForm", data)

    getwin = lambda x, team: 1 if (int(x[2]) > int(x[3]) and int(x[4])==team) or (int(x[2]) < int(x[3]) and int(x[5])==team) \
                        else (0 if int(x[2])==int(x[3]) else 2)

    # TODO: Verinin cogunu kullanmiyoruz neden template e pasliyoruz?
    getlist = lambda x, team: [{'matchId':match[0],
                         'matchName':match[1],
                         'homeScore':match[2],
                         'awayScore':match[3],
                         'homeTeamId':match[4],
                         'awayTeamId':match[5],
                         'homeTeam':match[6],
                         'awayTeam':match[7],
                         'win':getwin(match, team)} for match in x]

    return getlist(homelist, homeTeamId), getlist(awaylist, awayTeamId)

def get_match_events(match_id):
    data = {"matchId":match_id}
    datalist = service_request("GetMatchEvents", data)

    if len(datalist) == 0:
        return [] # no events in game

    return [{'type':event[0],
              'min':event[1],
              'teamId':int(event[2]),
              'playerId':event[3],
              'playerIdIn':event[4],
              'jerseyNumber':event[5],
              'jerseyNumberIn':event[6]} for event in datalist]

def calculate_percentage(x,y):
    xPercent = 0
    yPercent = 0
    if x+y < 1:
        xPercent = 50
    else:
        xPercent = int(x/float(x+y)*100)
    yPercent = 100 - xPercent

    return xPercent, yPercent

def get_match_stats(match_id, homeTeamId, awayTeamId):
    data = {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"matchId":match_id}
    datalist = service_request("GetMatchData", data)

    if len(datalist) == 0: # there is no data
        return [], [], [], []

    matchDataDict = [] #stores all players in the match
    homeDataDict = []  #stores only home players
    awayDataDict = [] #stores only away players

    #self explanatory
    #corners, offsides, penalties and cards should be added

    common_stats = {'distance': (4, 'Toplam Mesafe', ' m'),
                    'hir': (6, 'Şiddetli Koşu', ' m'),
                    'totalPass': (7, 'Toplam Pas', ''),
                    'successPass': (8, 'Başarılı Pas', ''),
                    'shot': (9, 'Toplam Şut', ''),
                    'successfulShot': (10, 'İsabetli Şut', ''),
                    'totalCross': (11, 'Toplam Orta', ''),
                    'successfulCross': (12, 'İsabetli Orta', ''),
                    'foulCommitted': (13, 'Yapılan Faul', '')}

    home_totals = {k:0 for k in common_stats}
    away_totals = {k:0 for k in common_stats}

    for dat in datalist:
        #add all data into match data

        player_tuple = {'teamId':dat[0],
                        'playerName':dat[1],
                        'playerId':dat[2],
                        'jerseyNumber':dat[3],
                        'totalDistance':int(dat[4] or 0),
                        'averageSpeed':int(dat[5] or 0),
                        'HIRDistance':int(dat[6] or 0),
                        'totalPass':int(dat[7] or 0),
                        'successfulPass':int(dat[8] or 0),
                        'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),
                        'totalShot':int(dat[9] or 0),
                        'successfulShot':int(dat[10] or 0),
                        'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),
                        'totalCross':int(dat[11] or 0),
                        'successfulCross':int(dat[12] or 0),
                        'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),
                        'foulCommitted':int(dat[13] or 0),
                        'foulAgainst':int(dat[14] or 0)}

        matchDataDict.append(player_tuple)

        if dat[0] == homeTeamId:

            for k in home_totals:
                home_totals[k] += int(dat[common_stats[k][0]] or 0)
            homeDataDict.append(player_tuple)

        elif dat[0] == awayTeamId:

            for k in away_totals:
                away_totals[k] += int(dat[common_stats[k][0]] or 0)
            awayDataDict.append(player_tuple)

    #ratios calculations TODO
#    homePassRatio = int(homeSuccessfulPass/float(homeTotalPass or 1) * 100)
#    awayPassRatio = int(awaySuccessfulPass/float(awayTotalPass or 1) * 100)
#
#    homeShotRatio = int(homeSuccessfulShot/float(homeTotalShot or 1) * 100)
#    awayShotRatio = int(awaySuccessfulShot/float(awayTotalShot or 1) * 100)
#
#    homeCrossRatio = int(homeSuccessfulCross/float(homeTotalCross or 1) * 100)
#    awayCrossRatio = int(awaySuccessfulCross/float(awayTotalCross or 1) * 100)

    home_percentages = {}
    away_percentages = {}

    for k in common_stats:
        home_percentages[k], away_percentages[k] = calculate_percentage(home_totals[k], away_totals[k])

    teamStatsDict = [
        {'name': common_stats[k][1],
         'homeValue': home_totals.get(k,0),
         'awayValue': away_totals.get(k,0),
         'homePercent': home_percentages.get(k,0),
         'awayPercent': away_percentages.get(k,0),
         'addition': common_stats[k][2]} for k in common_stats
    ] #holds team stats for team summaries

    return teamStatsDict, matchDataDict, homeDataDict, awayDataDict
