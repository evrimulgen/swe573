"""
Helper functions for match center views

author: Caner Turkmen
"""

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

    infoDict = [] #holds match info data
    homeTeamId = 0 # home team id of current match
    awayTeamId = 0 # away team id of current match
    if len(datalist) > 0 :
        x = datalist[0]
        homeTeamId = x[5] #set home team id
        awayTeamId = x[6] #set away team id
        infoDict.append({'weekId':x[0],'matchId':x[1],'status':x[2],'homeTeam':x[3],'awayTeam':x[4],'homeTeamId':x[5],'awayTeamId':x[6],'homeTeamScore':int(x[7] or 0),'awayTeamScore':int(x[8] or 0),'date':x[9],'time':x[10],'liveTime':x[11],'referee':x[12],'stadium':x[13]})

    return homeTeamId, awayTeamId, infoDict

def get_goal_videos(match_id):

    data = {"matchId":match_id}
    goalDict = [] #holds goal video data
    datalist = service_request("GetMatchVideos", data) # returns "data" field in response

    if len(datalist) > 0 :
        for x in datalist:
            goalDict.append({'awayTeamId':x[0],'text':"Maç Özeti",'awayTeamId':x[2],'min':x[3],'goalLink':x[4]})

    datalist = service_request("GetGoalVideos", data) # returns "data" field in response
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
