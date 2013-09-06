"""
Django View Controllers for Stat Center
"""
from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from statcenter.helpers import get_standings, get_teams, get_fixture
from statcenter.utils import service_request

LEAGUE_ID = 1
SEASON_ID = 9064

weekList = range(1, 35)

def stats_common_context():
    """
    Prepare the common context for stats center views
    """
    pass


def statscenter(request):
    data = {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID}
    week = service_request("GetWeeks", data)
    return HttpResponseRedirect('week/%s' % week[0][1]) # Roll to current week

def home(request,weekId):
    weeks = service_request("GetWeeks", {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID})
    weekNumber, lastPlayed  = weeks[0][0], weeks[0][1]

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

def team(request, num):
    """
    View controller for the Stats Center Team view
    """
    # TODO: Sag paneldeki "best list" entegre edilmeli
    # TODO: Takimin pozisyonlari degisimi daha iyi bi grafikte ve gercek datayla verilecek

    datalist = service_request("GetTeamDetails", {"teamId": num})

    detailDict = []
    if len(datalist) > 0:
        obj = datalist[0]
        detailDict.append( {'teamName':obj[0],'stadium':obj[1],'foundation':obj[2],'president':obj[3],'capacity':obj[4],'manager':obj[5],'website':obj[6],'leaguechamp':obj[7],'cupchamp':obj[8]})

    standingDict = []
    datalist =  service_request("GetStandings",{"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"type":0})
    if len(datalist) > 0:
        for item in datalist:
            if int(item[0]) == 34:
                standingDict.append({'teamId': int(item[1]), 'teamName': item[2],'played':int(item[3]), 'win':int(item[4]), 'draw':int(item[5]), 'lose':int(item[6]), 'score':int(item[7]), 'conceded' : int(item[8]), 'average':int(item[9]), 'points':int(item[10]), 'change': int(item[11])})

    datalist = service_request("GetTeamPlayers", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID, "teamId": num})
    playerDict =[]
    if len(datalist) > 0:
        for x in datalist:
            playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})

    return render_to_response('sc_team.html', {'fixture':get_fixture(),
                                                 'try_list':get_teams(),
                                                 'details':detailDict,
                                                 'players':playerDict,
                                                 'standing_list':standingDict,
                                                 'team_selected': int(num)})

def teamselect(request):
    return render_to_response('sc_teamselect.html',{'standing_list':get_standings(),
                                                    'weeklist':weekList,
                                                    'try_list':get_teams()} )

def playerselect(request, num):
    """
    Base player selection
    """
    data = {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID, "teamId": num}
    datalist = service_request("GetTeamPlayers", data)

    playerDict =[]
    if len(datalist) > 0:
        for x in datalist:
            playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})

    data = {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID}
    datalist = service_request("GetTeams", data)

    teamDict = []
    if len(datalist) > 0:
        for x in datalist:
            teamDict.append({'teamId':x[0],'teamName':x[1]})

    return render_to_response('playerselection.html', { 'team_selected': int(num),
                                                        'try_list':teamDict,
                                                        #'team_list': teamList,
                                                        'players':playerDict,
                                                        #'player_list':playerList,
                                                        #"best_eleven_list":bestList,
                                                        'weeklist': weekList})

def player_teamselect(request):
    datalist = service_request("GetTeams", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})

    teamDict = []
    if len(datalist) > 0:
        for x in datalist:
            teamDict.append({'teamId':x[0],'teamName':x[1]})

    return render_to_response('sc_player_teamselect.html',{ #'best_eleven_list':bestList,
                                                           'weeklist': weekList,
                                                           'try_list':teamDict} )

@ensure_csrf_cookie
def player(request, num, player_id):

    data = {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID,"playerId": player_id}
    datalist = service_request("GetPlayerDetails", data)

    detailDict = []
    if len(datalist) > 0:
        for obj in datalist:
            detailDict.append({'playerName':obj[0],'date':obj[1],'height':obj[2],'nation':obj[3],'cap':obj[4],'goal':obj[5],'teamId':obj[6],'teamName':obj[7]})

    data = {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID, "teamId": num}
    datalist = service_request("GetTeamPlayers", data)

    playerDict =[]
    if len(datalist) > 0:
        for x in datalist:
            playerDict.append({'playerId':x[0],'playerName':x[1],'jerseyNumber':x[2],'position':x[3],'match':x[4],'minutes':x[5],'goals':x[6],'assists':x[7],'yellowCards':x[8],'redCards':x[9]})


    return render_to_response('sc_player.html', {'p_id': int(player_id),
                                                   'details':detailDict,
                                                   'try_list':get_teams(),
                                                   'players':playerDict,
                                                   'team_selected': int(num),
                                                   #'team_list': teamList,
                                                   #'player_list':playerList,
                                                   #"best_eleven_list":bestList,
                                                   'weeklist': weekList})

def compare(request):
    return render_to_response('sc_compare.html')