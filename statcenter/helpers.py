# coding=utf-8
"""
Helper functions for frequently used Stats Center code
"""
from statcenter.utils import service_request
from dje2.settings import LEAGUE_ID, SEASON_ID

def get_standings():
    standingDict = []
    current_week = get_week_details()[0][1]
    datalist =  service_request("GetStandings",{"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"type":0})
    if len(datalist) == 0:
        return []

    current_week_tuples = [x for x in datalist if x[0] == current_week]

    for item in current_week_tuples:
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

def get_all_team_data():
    team_list = get_teams()
    run_list = get_team_run()
    goal_list = get_team_goal()
    pass_list = get_team_pass()
    shot_list = get_team_shot()
    foul_list = get_team_foul()
    team_data = []
    for team in team_list:
        tid = team["teamId"]
        team_data.append({"teamId":tid,
                          "teamName":team["teamName"],
                          "matches":get_team_from_dict(run_list,tid)["matches"],
                          "totalDistance":get_team_from_dict(run_list,tid)["totalDistance"],
                          "averageSpeed":get_team_from_dict(run_list,tid)["averageSpeed"],
                          "HIRDistance":get_team_from_dict(run_list,tid)["HIRDistance"],
                          "sprintDistance":get_team_from_dict(run_list,tid)["sprintDistance"],
                          "HIRNumber":get_team_from_dict(run_list,tid)["HIRNumber"],
                          "sprintNumber":get_team_from_dict(run_list,tid)["sprintNumber"],
                          "scored":get_team_from_dict(goal_list,tid)["scored"],
                          "conceded":get_team_from_dict(goal_list,tid)["conceded"],
                          "penaltyGoal":get_team_from_dict(goal_list,tid)["penaltyGoal"],
                          "passTotal":get_team_from_dict(pass_list,tid)["passTotal"],
                          "passSuccessful":get_team_from_dict(pass_list,tid)["passSuccessful"],
                          "crossTotal":get_team_from_dict(pass_list,tid)["crossTotal"],
                          "crossSuccessful":get_team_from_dict(pass_list,tid)["crossSuccessful"],
                          "shotTotal":get_team_from_dict(shot_list,tid)["shotTotal"],
                          "shotSuccessful":get_team_from_dict(shot_list,tid)["shotSuccessful"],
                          "foulCommitted":get_team_from_dict(foul_list,tid)["foulCommitted"],
                          "foulSuffered":get_team_from_dict(foul_list,tid)["foulSuffered"],
                          "yellow":get_team_from_dict(foul_list,tid)["yellow"],
                          "red":get_team_from_dict(foul_list,tid)["red"]
                          })
    return team_data

def get_team_run():
    runList = service_request("GetTeamRun", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})
    runDict = []
    for run in runList:
        runDict.append({run[0]:{"matches":run[1],"totalDistance":run[2],"averageSpeed":run[3],"HIRDistance":run[4],"sprintDistance":run[5],"HIRNumber":run[6],"sprintNumber":run[7]}})
    return runDict

def get_team_goal():
    goalList = service_request("GetTeamGoal", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})
    goalDict = []
    for goal in goalList:
        goalDict.append({goal[0]:{"scored":goal[1],"conceded":goal[2],"penaltyGoal":goal[3]}})
    return goalDict

def get_team_pass():
    passList = service_request("GetTeamPass", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})
    passDict = []
    for pas in passList:
        passDict.append({pas[0]:{"passTotal":pas[1],"passSuccessful":pas[2],"crossTotal":pas[3],"crossSuccessful":pas[3]}})
    return passDict

def get_team_shot():
    shotList = service_request("GetTeamShot", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})
    shotDict = []
    for shot in shotList:
        shotDict.append({shot[0]:{"shotTotal":shot[1],"shotSuccessful":shot[2]}})
    return shotDict

def get_team_foul():
    foulList = service_request("GetTeamFoul", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID})
    foulDict = []
    for foul in foulList:
        foulDict.append({foul[0]:{"foulCommitted":foul[1],"foulSuffered":foul[2],"yellow":foul[3],"red":foul[4]}})
    return foulDict

def get_team_from_dict(diction,teamId):
    for team in diction:
        for id in team:
            if id == teamId:
                return team[id]

def get_best_scorers(weekid,count):
    week = 0
    weeks = []
    while week < weekid:
        weeks.append(week)
    bestList = service_request("GetBestScorers", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID,"weekList":weeks,"count":count})

def get_team_form(teamId):
    data = {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"teamId":teamId,"type":0,"weekId":40}
    teamlist = service_request("GetTeamForm", data)

    getwin = lambda x, team: 1 if (int(x[2]) > int(x[3]) and int(x[4]) == team) or (int(x[2]) < int(x[3]) and int(x[5]) == team) \
                        else (0 if int(x[2]) == int(x[3]) else 2)

    # TODO: Verinin cogunu kullanmiyoruz neden template e pasliyoruz?
    getlist = lambda x, team: [{'matchId':match[0],
                         'matchName':match[1],
                         'homeScore':match[2],
                         'awayScore':match[3],
                         'homeTeamId':match[4],
                         'awayTeamId':match[5],
                         'homeTeam':match[6],
                         'awayTeam':match[7],
                         'weekId':match[8],
                         'win':getwin(match, team)} for match in x]

    return getlist(teamlist, teamId)

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

def get_team_players(teamid):
    datalist = service_request("GetTeamPlayers", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID, "teamId": teamid})

    playerDict =[]
    if len(datalist) == 0:
        return []

    coal = lambda x: x if x is not None else 0

    for x in datalist:
        playerDict.append({'playerId':coal(x[0]),
                           'playerName':coal(x[1]),
                           'jerseyNumber':coal(x[2]),
                           'position':coal(x[3]),
                           'match':int(coal(x[4])),
                           'minutes':int(coal(x[5])),
                           'goals':int(coal(x[6])),
                           'assists':int(coal(x[7])),
                           'yellowCards':int(coal(x[8])),
                           'redCards':int(coal(x[9]))})

    return playerDict

def get_player_details(playerid):
    datalist = service_request("GetPlayerDetails", {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID,"playerId": playerid})

    detailDict = []
    if len(datalist) == 0:
        return []

    for obj in datalist:
        detailDict.append({'playerName':obj[0],
                           'date':obj[1],
                           'height':obj[2],
                           'nation':obj[3],
                           'cap':obj[4],
                           'goal':obj[5],
                           'teamId':obj[6],
                           'teamName':obj[7]})

    return detailDict

def get_team_details(teamid):

    datalist = service_request("GetTeamDetails", {"teamId": teamid})

    detailDict = []
    if len(datalist) == 0:
        return []

    obj = datalist[0]
    detailDict.append( {'teamName':obj[0],
                        'stadium':obj[1],
                        'foundation':obj[2],
                        'president':obj[3],
                        'capacity':obj[4],
                        'manager':obj[5],
                        'website':obj[6],
                        'leaguechamp':obj[7],
                        'cupchamp':obj[8]})

    return detailDict

def get_standings_by_week(weekid):
    standingDict = []
    datalist =  service_request("GetStandings",{"leagueId":LEAGUE_ID,"seasonId":SEASON_ID,"type":0})

    if len(datalist) == 0:
        return []

    for item in datalist:
        if int(item[0]) == int(weekid):
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

def get_week_details():
    data = service_request("GetWeeks", {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID})
    return data

def get_player_stats(playerid):
    """
    Invoke GetPlayerCard in api
    """

    weeks = get_week_details()
    data = service_request("GetPlayerCard", {"leagueId": LEAGUE_ID,
                                             "seasonId": SEASON_ID,
                                             "playerId": playerid,
                                             "weekId": weeks[0][1]})

    stats = data.get("statistics")

    if not stats:
        return []

    stat_lookup = lambda x: {"passes": "Toplam Pas",
                     "shotsOnTarget": "İsabetli Şut",
                     "crosses": "Toplam Orta",
                     "foulsSuffered": "Maruz Kalınan Faul",
                     "totalDistance": "Kat Edilen Mesafe",
                     "yellowCard": "Sarı Kart",
                     "corners": "Korner",
                     "redCard": "Kırmızı Kart",
                     "successfulCross": "İsabetli Orta",
                     "penalty": "Penaltı",
                     "assists": "Asist",
                     "goals": "Gol",
                     "shots": "Şut",
                     "foulsCommitted": "Yapılan Faul",
                     "matchesPlayed": "Oynadığı Maç Sayısı",
                     "successfulPass": "İsabetli Pas"}.get(x)

    result = {}
    for i in stats:
        result[stat_lookup(i)] = [stats[i][0], stats[i][1]]

    return result


def get_player_last_matches(pid):
    """
    :param pid: player id
    """

    return service_request("GetPlayerLastMatches", {"playerId": pid,
                                                    "count": 5,
                                                    "leagueId": LEAGUE_ID,
                                                    "seasonId": SEASON_ID})

def get_player_last_goals(pid):
    """
    :param pid: player id
    """

    return service_request("GetPlayerGoals", {"playerId": pid,
                                                    "count": 5,
                                                    "leagueId": LEAGUE_ID,
                                                    "seasonId": SEASON_ID})

def get_team_past_standings(tid):
    """
    :param tid: team id
    :param weekid: week id
    """

    return service_request("GetTeamPastPositions", {"teamId": tid,
                                                    "leagueId": LEAGUE_ID,
                                                    "seasonId": SEASON_ID})

def get_team_card(tid):
    """
    :param tid: team id
    """

    list = service_request("GetTeamCard", {"teamId": tid,
                                    "leagueId": LEAGUE_ID,
                                    "seasonId": SEASON_ID})

    turkify_stat = lambda x: {"CrossSuccess": (u"İsabetli Orta", 8),
                                "CrossTotal": (u"Toplam Orta", 7),
                                "Faul": (u"Yapılan Faul", 9),
                                "Goal": (u"Gol", 1),
                                "GoalConceded": (u"Yenilen Gol", 2),
                                "PassSuccess": (u"İsabetli Pas", 6),
                                "PassTotal": (u"Toplam Pas", 5),
                                "RedCard": (u"Kırmızı Kart", 11),
                                "ShotSuccess": (u"İsabetli Şut", 4),
                                "ShotTotal": (u"Toplam Şut", 3),
                                "YellowCard": (u"Sarı Kart", 10)}.get(x)

    res = [[turkify_stat(x[0])[0], turkify_stat(x[0])[1], int(x[1]), int(x[2])] for x in list]
    res = sorted(res, key=lambda x: x[1])

    return res