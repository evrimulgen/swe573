"""
Django View Controllers for Stat Center
"""
from random import randint
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from statcenter.helpers import *
from statcenter.utils import service_request, prune_dicts, prune_lists
from dje2.settings import LEAGUE_ID, SEASON_ID

weekList = range(1, 35)

@ensure_csrf_cookie
def statscenter(request):
    week = get_week_details()
    return HttpResponseRedirect('week/%s' % week[0][1]) # Roll to current week

@ensure_csrf_cookie
def home(request,weekId):
    weeks = service_request("GetWeeks", {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID})
    weekNumber, lastPlayed  = weeks[0][0], weeks[0][1]

    weekDict = range(1, weekNumber+1)

    top_passers = get_top5("pass", weekId)
    map(lambda x: x.append("%%%s"%int(float(x[4])*100/float(x[3]))), top_passers)

    best_eleven = get_besteleven(weekId)
    print best_eleven

    return render_to_response('sc_home.html', {'fixture':get_fixture(),
                                               'weekList':weekDict,
                                               'leagueId':LEAGUE_ID,
                                               'seasonId':SEASON_ID,
                                               'weekSelected': int(weekId),
                                               'lastPlayedWeek':int(lastPlayed),
                                               'standing_list':get_standings_by_week(int(weekId)),
                                               'best_eleven_list':None,
                                               'top_passers': top_passers,
                                               'top_scorers': get_top5("goal", weekId),
                                               'top_runners': get_top5("distance", weekId),
                                               'quad_ace': get_quadace(weekId),
                                               'best_eleven': best_eleven})

@ensure_csrf_cookie
def team(request, num):
    """
    View controller for the Stats Center Team view
    """
    # TODO: Sag paneldeki "best list" entegre edilmeli
    # TODO: Takimin pozisyonlari degisimi daha iyi bi grafikte ve gercek datayla verilecek

    slist = [x[1] for x in get_team_past_standings(num)]
    slist = simplejson.dumps(slist)

    return render_to_response('sc_team.html', {'fixture':get_fixture(),
                                                 'card': get_team_card(num),
                                                 'try_list':get_teams(),
                                                 'details':get_team_details(num),
                                                 'players':get_team_players(num),
                                                 'standing_list':get_standings(),
                                                 's_list': slist,
                                                 'team_data':get_all_team_data(),
                                                 'form':get_team_form(num),
                                                 'team_selected': int(num)})

@ensure_csrf_cookie
def teamselect(request):

    return render_to_response('sc_teamselect.html',{'standing_list':get_standings(),
                                                    'weeklist':weekList,
                                                    'try_list':get_teams(),
                                                    'team_data':get_all_team_data()} )
@ensure_csrf_cookie
def playerselect(request, num):
    """
    Base player selection

    :param num: team id passed in by the route config
    """
    return render_to_response('sc_playerselect.html', { 'team_selected': int(num),
                                                        'try_list':get_teams(),
                                                        #'team_list': teamList,
                                                        'players':get_team_players(num),
                                                        #'player_list':playerList,
                                                        #"best_eleven_list":bestList,
                                                        'weeklist': weekList})

@ensure_csrf_cookie
def player_teamselect(request):
    return render_to_response('sc_player_teamselect.html',{ #'best_eleven_list':bestList,
                                                           'weeklist': weekList,
                                                           'try_list':get_teams()} )

@ensure_csrf_cookie
def player(request, num, player_id):
    return render_to_response('sc_player.html', {'p_id': int(player_id),
                                                   'details':get_player_details(player_id),
                                                   'try_list':get_teams(),
                                                   'players':get_team_players(num),
                                                   'team_selected': int(num),
                                                   'player_stats': get_player_stats(player_id),
                                                   #'team_list': teamList,
                                                   #'player_list':playerList,
                                                   #"best_eleven_list":bestList,
                                                   'lastMatches': get_player_last_matches(player_id),
                                                   'lastGoals': get_player_last_goals(player_id),
                                                   'weeklist': weekList})

@ensure_csrf_cookie
def compare(request):
    return render_to_response('sc_compare.html')

@ensure_csrf_cookie
def compareplayer(request):
    return render_to_response('sc_player_compare.html')

@csrf_exempt
def partial_teamsidestats(request):
    data = simplejson.loads(request.body)

    code = data.get("stat")
    common_param = {"leagueId": LEAGUE_ID, "seasonId": SEASON_ID}

    # if the said statistics can be retreived from the get_standings method (TF_STANDINGS)
    if code in ["score", "conceded", "average"]:
        a = prune_dicts(["teamId", code], get_standings())
    elif code == "pass":
        a = service_request("GetTeamPass", common_param)
    elif code in ["shot", "shoton"]:
        a = service_request("GetTeamShot", common_param)
        ix = 1 if code=="shot" else 2
        a = prune_lists([0,ix], a)
    elif code == "distance":
        a = service_request("GetTeamRun", common_param)
        a = prune_lists([0,2], a)
    elif code in ["foul", "yellow", "red"]:
        ix = {"foul": 1, "yellow": 3, "red": 4}.get(code)
        a = service_request("GetTeamFoul", common_param)
        a = prune_lists([0, ix], a)
    else:
        return HttpResponse()

    # return HttpResponse(simplejson.dumps(a), mimetype="application/json")
    return render_to_response('_sc_team_sidebar.html', {"slist": a})