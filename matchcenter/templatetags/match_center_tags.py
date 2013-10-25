from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe
from matchcenter.helpers import get_fixture

register = template.Library()

LEAGUE_ID = 1
SEASON_ID = 9064

@register.inclusion_tag('_vs_fixture.html')
def sl_fixture(match_id):
    weeks, currentWeek = get_fixture(LEAGUE_ID, SEASON_ID, int(match_id))
    return {"weeks": weeks, "currentWeek": currentWeek}

@register.inclusion_tag('_vs_before_playerlistitem.html')
def sl_before_playerlistitem(player, team, votingActive):
    return {
        "class": ('starting' if player.get('eleven')==1 else 'sub'),
        "player": player,
        "team" : team,
        "votingActive": votingActive
    }

@register.inclusion_tag('_vs_center_eventitem.html', takes_context=True)
def sl_center_eventitem(context, event, homeid, awayid):
    img_lookup = lambda x: {
        0: "goal.png",
        1: "own-goal.png",
        2: "penalty.png",
        3: "missed-pen.png",
        4: "yellow.png",
        5: "second-yellow.png",
        6: "red.png",
        7: "substitution.png"
    }.get(x)

    ctx = {
        "event": event,
        "homeTeamId": homeid,
        "awayTeamId": awayid,
        "eventImagePath": img_lookup(int(event.get("type"))) if event.get("type") is not None else ""
    }

    return ctx

@register.inclusion_tag('_vs_radar_tabs_narration.html')
def sl_center_narration(narrations):
    img_lookup = lambda x: {
        0: "goal.png",
        1: "own-goal.png",
        2: "penalty.png",
        3: "missed-pen.png",
        4: "yellow.png",
        5: "second-yellow.png",
        6: "red.png",
        7: "substitution.png"
    }.get(x)

    for narration in narrations:
        narration["type"] = img_lookup(int(narration.get("type"))) if narration.get("type") is not None else ""

    return {"narrations": narrations}

@register.inclusion_tag('_vs_center_team_data.html')
def sl_center_team_data(match_id):
    # currently stubbed, will handle thru view
    pass

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True