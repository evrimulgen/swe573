"""
Helper functions for frequently used Stats Center code
"""
from statcenter.utils import service_request
from dje2.settings import LEAGUE_ID, SEASON_ID

def get_standings():
    standingDict = []
    datalist =  service_request("GetStandings",{"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"type":0})
    if len(datalist) == 0:
        return []

    for item in datalist:
        if int(item[0]) == 34: # TODO: Secilen hafta neyse o olacak
            standingDict.append({'teamId': int(item[1]),
                                 'teamName': item[2],
                                 'played':int(item[3]),
                                 'win':int(item[4]),
                                 'draw':int(item[5]),
                                 'lose':int(item[6]),
                                 'score':int(item[7]),
                                 'conceded' : int(item[8]),
                                 'average':int(item[9]),
                                 'points':int(item[10]),
                                 'change': int(item[11])})

    return standingDict

def get_teams():
    datalist = service_request("GetTeams", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})
    teamDict = []
    if len(datalist) == 0:
        return []

    for x in datalist:
        teamDict.append({'teamId':x[0],'teamName':x[1]})

    return teamDict

def get_fixture():
    weeklist = service_request("GetFixture", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})

    fixtureDict = []
    if len(weeklist) == 0:
        return []

    for week_id in weeklist:
        week = weeklist[week_id]
        matches = []
        for matchId in week:
            if matchId == "weekStatus":
                status = week[matchId]
            else:
                matches.append({'matchId':matchId,
                                'matchStatus':week[matchId][0],
                                'homeTeam':week[matchId][1],
                                'homeTeamCond':week[matchId][2],
                                'homeTeamInt':week[matchId][3],
                                'awayTeam':week[matchId][4],
                                'awayTeamCond':week[matchId][5],
                                'awayTeamInt':week[matchId][6],
                                'homeTeamId':int(week[matchId][7]),
                                'awayTeamId':int(week[matchId][8]),
                                'homeScore':week[matchId][9],
                                'awayScore':week[matchId][10],
                                'date':week[matchId][11],
                                'liveTime':week[matchId][12],
                                'referee':week[matchId][13],
                                'stadium':week[matchId][14]})

        fixtureDict.append({'weekId':int(week_id),'status':status,'matches':matches})

    return fixtureDict

