# -*- coding: utf-8 -*-
from django import template
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from matchcenter.helpers import *
from matchcenter.templatetags.match_center_tags import sl_fixture
from matchcenter.utils import service_request

# DEFINE ALL CONSTANTS HERE

LEAGUE_ID = 1
SEASON_ID = 9064
WEEK_LIST = range(1,35)

# VIEW CONTROLLERS

def prep_common_context(reqid):

    # must take currentWeek and weekDict here
    # weekDict, currentWeek = get_fixture(LEAGUE_ID, SEASON_ID, reqid)

    # data for match info, used for all views in match center
    homeTeamId, awayTeamId, infoDict = get_match_info(reqid)

    # data for match goals, used for all views in match center
    goalDict = get_goal_videos(reqid)

    # TODO: maç özeti ve diğer maç videoları buraya eklenmeli, yapı değişikliği olacak.

    # data for team squads, used in all views in match center
    # TODO: not good practice to pass in homeTeamId here
    homeSquadDict, awaySquadDict = get_team_squads(reqid, homeTeamId, awayTeamId)

    teamStatsDict, matchDataDict, homeDataDict, awayDataDict = get_match_stats(reqid, homeTeamId, awayTeamId)

    common_context = {'teamStats':teamStatsDict,
                      'awayData':awayDataDict,
                      'homeData':homeDataDict,
                      'matchData':matchDataDict,
                      'homeTeamId':homeTeamId,
                      'awayTeamId':awayTeamId,
                      'homeSquad':homeSquadDict,
                      'awaySquad':awaySquadDict,
                      'weeklist': WEEK_LIST,
                      'goals':goalDict,
                      'matchInfo':infoDict,
                      'selectedMatch':str(reqid)}

    return common_context

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

def center(request, reqid):
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

    return render_to_response('vs_radar.html', context)

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

def partial_fixture(request,match_id):
    return render_to_response('_vs_fixture.html', sl_fixture(match_id))