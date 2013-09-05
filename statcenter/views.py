"""
Django View Controllers for Stat Center
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from statcenter.utils import service_request

LEAGUE_ID = 1
SEASON_ID = 9064

def statscenter(request):
    data = {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID}
    week = service_request("GetWeeks", data)
    return HttpResponseRedirect('week/%s' % week[0][1]) # Roll to current week

def home(request,weekId):
    data = {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID}
    weeks = service_request("GetWeeks", data)
    weekNumber = weeks[0][0]
    lastPlayed = weeks[0][1]

    weekDict = range(1, weekNumber+1)

    standingDict = []
    datalist =  service_request("GetStandings",{"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"type":0})

    if len(datalist) > 0:
        for item in datalist:
            if int(item[0]) == int(weekId):
                standingDict.append({'teamId': int(item[1]), 'teamName': item[2],'played':int(item[3]), 'win':int(item[4]), 'draw':int(item[5]), 'lose':int(item[6]), 'score':int(item[7]), 'conceded' : int(item[8]), 'average':int(item[9]), 'points':int(item[10]), 'change': int(item[11])})

    weeklist = service_request("GetFixture", {"leagueId": LEAGUE_ID, "seasonId":SEASON_ID})

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

    return render_to_response('sc_home.html', {'fixture':fixtureDict,
                                               'weekList':weekDict,
                                               'weekSelected': int(weekId),
                                               'lastPlayedWeek':int(lastPlayed),
                                               'standing_list':standingDict,
                                               'best_eleven_list':None})


