"""
Django View Controllers for Stat Center
"""
from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from statcenter.helpers import get_standings, get_teams, get_fixture, get_team_players, get_player_details, get_team_details, get_standings_by_week
from statcenter.utils import service_request
from dje2.settings import LEAGUE_ID, SEASON_ID

weekList = range(1, 35)

@ensure_csrf_cookie
def statscenter(request):
    week = service_request("GetWeeks", {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID})
    return HttpResponseRedirect('week/%s' % week[0][1]) # Roll to current week

@ensure_csrf_cookie
def home(request,weekId):
    weeks = service_request("GetWeeks", {"leagueId":LEAGUE_ID,"seasonId":SEASON_ID})
    weekNumber, lastPlayed  = weeks[0][0], weeks[0][1]

    weekDict = range(1, weekNumber+1)

    return render_to_response('sc_home.html', {'fixture':get_fixture(),
                                               'weekList':weekDict,
                                               'weekSelected': int(weekId),
                                               'lastPlayedWeek':int(lastPlayed),
                                               'standing_list':get_standings_by_week(),
                                               'best_eleven_list':None})
@ensure_csrf_cookie
def team(request, num):
    """
    View controller for the Stats Center Team view
    """
    # TODO: Sag paneldeki "best list" entegre edilmeli
    # TODO: Takimin pozisyonlari degisimi daha iyi bi grafikte ve gercek datayla verilecek

    return render_to_response('sc_team.html', {'fixture':get_fixture(),
                                                 'try_list':get_teams(),
                                                 'details':get_team_details(num),
                                                 'players':get_team_players(num),
                                                 'standing_list':get_standings(),
                                                 'team_selected': int(num)})

@ensure_csrf_cookie
def teamselect(request):
    return render_to_response('sc_teamselect.html',{'standing_list':get_standings(),
                                                    'weeklist':weekList,
                                                    'try_list':get_teams()} )
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
                                                   #'team_list': teamList,
                                                   #'player_list':playerList,
                                                   #"best_eleven_list":bestList,
                                                   'weeklist': weekList})

def compare(request):
    return render_to_response('sc_compare.html')