# -*- coding: utf-8 -*-
from django import template
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson as json
from matchcenter.helpers import *
from matchcenter.templatetags.match_center_tags import sl_fixture, sl_center_narration
from matchcenter.utils import service_request
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# DEFINE ALL CONSTANTS HERE

LEAGUE_ID = 1
SEASON_ID = 9064
WEEK_LIST = range(1,35)

# VIEW CONTROLLERS

def turkify_date(date):
    """
    Takes a string as date (format 2013-08-24) and prints out Turkified date: '24 Ağu 2013'

    **Doctests**
    >>> turkify_date('2013-08-24')
    "24 Ağu 2013"
    """
    dt = datetime.strptime(date, '%Y-%m-%d')
    turk_month = {1: u"Oca", 2: u"Şub", 3: u"Mar", 4: u"Nis", 5: u"May", 6: u"Haz",
                  7: u"Tem", 8: u"Ağu", 9: u"Eyl", 10: u"Eki", 11: u"Kas", 12: u"Ara"}.get(dt.month)
    return u"%s %s %s" % (dt.day, turk_month, dt.year)

def prep_common_context(reqid):

    # must take currentWeek and weekDict here
    weekDict, currentWeek = get_fixture(LEAGUE_ID, SEASON_ID, reqid)

    # data for match info, used for all views in match center
    homeTeamId, awayTeamId, infoDict = get_match_info(reqid)

    # data for match goals, used for all views in match center
    goalDict = get_goal_videos(reqid)

    colorDict = get_team_colors(homeTeamId,awayTeamId)

    # TODO: maç özeti ve diğer maç videoları buraya eklenmeli, yapı değişikliği olacak.

    # data for team squads, used in all views in match center
    # TODO: not good practice to pass in homeTeamId here
    squad = get_team_squads(reqid, homeTeamId, awayTeamId)
    homeSquadDict, awaySquadDict, matchSquadDict = [], [], []
    isVotingActive = False
    if len(squad)>3:
        homeSquadDict = squad[0]
        awaySquadDict = squad[1]
        matchSquadDict = squad[2]
        isVotingActive = squad[3]

    homeManager, awayManager = get_team_manager(homeTeamId,awayTeamId)

    teamStatsDict, matchDataDict, homeDataDict, awayDataDict = get_match_stats(reqid, homeTeamId, awayTeamId)

    infoDict['date'] = turkify_date(infoDict.get("date"))
    print goalDict
    common_context = {'leagueId': LEAGUE_ID,
                      'seasonId': SEASON_ID,
                      'teamStats':teamStatsDict,
                      'currentWeek': currentWeek,
                      'awayData':awayDataDict,
                      'homeData':homeDataDict,
                      'matchData':matchDataDict,
                      'homeTeamId':homeTeamId,
                      'awayTeamId':awayTeamId,
                      'homeManager':homeManager,
                      'awayManager':awayManager,
                      'homeSquad':homeSquadDict,
                      'awaySquad':awaySquadDict,
                      'weeklist': WEEK_LIST,
                      'weeks': weekDict,
                      'teamColors': colorDict,
                      'goals':goalDict,
                      'matchInfo':infoDict,
                      'matchSquad':matchSquadDict,
                      'votingActive':isVotingActive,
                      'selectedMatch':str(reqid)}

    return common_context

@ensure_csrf_cookie
def before(request, reqid):
    context = prep_common_context(reqid)

    homeTeamId = context.get("homeTeamId")
    awayTeamId = context.get("awayTeamId")
    currentWeek = context.get("currentWeek")

    # data for history of two team, used in "before" view only
    historicDict = get_history(homeTeamId, awayTeamId)

    #data for home team form, used in "before" view only
    homeFormDict, awayFormDict = get_team_forms(homeTeamId, awayTeamId, currentWeek)

    context.update({
        'homeForm':homeFormDict,
        'awayForm':awayFormDict,
        'history':historicDict
    })

    return render_to_response('vs_before.html', context)

@ensure_csrf_cookie
def center(request, reqid):
    context = prep_common_context(reqid)

    #data for match events in the game, used in "center" and "table" views

    #data of all match(distance,pass,shot,cross,faul, etc..), used in all views
    #data for match narrations, used in "center" and "table" views
    #narrationDict = get_match_narration(reqid)
    gk_dict = get_team_gk_ids(reqid)


    context.update({
        #'narrations':narrationDict,
        'gks': gk_dict
    })

    return render_to_response('vs_radar.html', context)

@ensure_csrf_cookie
def table(request, reqid):
    context = prep_common_context(reqid)

    #data for match events in the game, used in "center" and "table" views
    eventDict = get_match_events(reqid)

    #data of all match(distance,pass,shot,cross,faul, etc..), used in all views
    #data for match narrations, used in "center" and "table" views
    narrationDict = get_match_narration(reqid)

    context.update({
        'events':eventDict,
        'narrations':narrationDict
    })

    return render_to_response('vs_board.html', context)

def partial_renderer(request, partial, match_id):
    sl_fixture
    return render_to_response('_vs_fixture.html', sl_fixture(match_id))

@csrf_exempt
def partial_fixture(request,match_id):
    return render_to_response('_vs_fixture.html', sl_fixture(match_id))

@csrf_exempt
def partial_events(request, match_id):
    home_team, away_team, match_info = get_match_info(match_id)

    eventDict = get_match_events(match_id)

    return render_to_response('_vs_radar_tabs_events.html', {"homeTeamId": home_team,
                                                             "awayTeamId": away_team,
                                                             "events": eventDict})

def partial_narration(request, match_id):
    narrations = get_match_narration(match_id)
    return render_to_response('_vs_radar_tabs_narration.html', sl_center_narration(narrations))

def partial_teamstats(request, match_id):
    homeid, awayid, all = get_match_info(match_id)
    teamStats, a, b, c = get_match_stats(match_id, homeid, awayid)
    colors = get_team_colors(homeid, awayid)

    return render_to_response('_vs_center_team_data.html', {"teamStats": teamStats, "colors": colors})

def partial_teamstats_dump(request, match_id):
    """
    dump the team stats in JSON format
    """
    homeid, awayid, all = get_match_info(match_id)
    teamStats, a, b, c = get_match_stats(match_id, homeid, awayid)
    colors = get_team_colors(homeid, awayid)

    data = json.dumps({"teamStats": teamStats, "colors": colors})

    return HttpResponse(data, mimetype="application/json")


def partial_playerstats(request, match_id):
    homeid, awayid, all = get_match_info(match_id)
    teamStats, matchData, homeData, awayData = get_match_stats(match_id, homeid, awayid)

    return render_to_response('_vs_center_player_data.html', {'homeData': homeData,
                                                              'awayData': awayData,
                                                              'matchInfo': all})

def radar_webview(request):
    pass

def partial_score(request, match_id):
    homeid, awayid, alli = get_match_info(match_id)

    context= {"home": alli.get("homeTeamScore"),
              "away": alli.get("awayTeamScore"),
              "mminute": alli.get("liveTime")}

    #print context
    return HttpResponse(json.dumps(context), mimetype="application/json")

def partial_sidestats(request, match_id):
    homeid, awayid, all = get_match_info(match_id)
    teamStatsDict, matchDataDict, homeDataDict, awayDataDict = get_match_stats(match_id, homeid, awayid)
    colorDict = get_team_colors(homeid,awayid)
    homeSquadDict, awaySquadDict, matchSquadDict = [], [], []
    isVotingActive = False
    squad = get_team_squads(match_id, homeid, awayid)
    if len(squad)>3:
        homeSquadDict = squad[0]
        awaySquadDict = squad[1]
        matchSquadDict = squad[2]
        isVotingActive = squad[3]

    context = {"matchData": matchDataDict,
               "teamColors" : colorDict,
               "homeTeamId" : homeid,
               "awayTeamId" : awayid,
               'matchStatus': all.get("status"),
               'matchSquad':matchSquadDict,
               'votingActive':isVotingActive,
               'selectedMatch':match_id
    }

    return render_to_response('_vs_sidestats.html', context)

def matchinfo(request,reqid):
    homeTeamId, awayTeamId, infoDict = get_match_info(reqid)
    return HttpResponse(json.dumps(infoDict))

def playerrate(request,matchid):
    return HttpResponse(json.dumps(get_player_ratings(matchid)))

def playervote(request,matchid,teamid,playerid):
    return HttpResponse(json.dumps(vote_match_player(matchid,teamid,playerid)))

def videos(request, match_id, videoId):
    goalDict = get_goal_videos(match_id)
    homeTeamId, awayTeamId, infoDict = get_match_info(match_id)
    return render_to_response('_vs_videos.html', {'goals': goalDict,
                                                  'videoId': int(videoId),
                                                  'matchInfoDict':infoDict})

@ensure_csrf_cookie
def d3_try(request):
    return render_to_response('_card_trial.html')

@ensure_csrf_cookie
def ozan(request):
    return render_to_response('_video_holder.html')
