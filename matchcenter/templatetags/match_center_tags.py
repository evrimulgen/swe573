from django import template
from matchcenter.helpers import get_fixture

register = template.Library()

LEAGUE_ID = 1
SEASON_ID = 9064

@register.inclusion_tag('_vs_fixture.html')
def sl_fixture(match_id):
    weeks, currentWeek = get_fixture(LEAGUE_ID, SEASON_ID, int(match_id))
    return {"weeks": weeks, "currentWeek": currentWeek}

@register.inclusion_tag('_vs_before_playerlistitem.html')
def sl_before_playerlistitem(player, team):
    return {
        "class": ('starting' if player.get('eleven')==1 else 'sub'),
        "player": player,
        "team" : team
    }

@register.inclusion_tag('_vs_center_eventitem.html', takes_context=True)
def sl_center_eventitem(context, event, homeid, awayid):
    img_lookup = lambda x: {
        0: "images/goal.png",
        1: "images/own-goal.png",
        2: "images/penalty.png",
        3: "images/missed-pen.png",
        4: "images/yellow.png",
        5: "images/second-yellow.png",
        6: "images/red.png",
        7: "images/substitution.png"
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
        0: "images/goal.png",
        1: "images/own-goal.png",
        2: "images/penalty.png",
        3: "images/missed-pen.png",
        4: "images/yellow.png",
        5: "images/second-yellow.png",
        6: "images/red.png",
        7: "images/substitution.png"
    }.get(x)

    for narration in narrations:
        narration["type"] = img_lookup(int(narration.get("type"))) if narration.get("type") is not None else ""

    return {"narrations": narrations}

@register.inclusion_tag('_vs_center_team_data.html')
def sl_center_team_data(match_id):
    # currently stubbed, will handle thru view
    pass