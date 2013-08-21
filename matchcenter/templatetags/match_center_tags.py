from django import template
from matchcenter.helpers import get_fixture

register = template.Library()

LEAGUE_ID = 1
SEASON_ID = 9064

@register.inclusion_tag('_vs_fixture.html')
def sl_fixture(match_id):
    weeks, currentWeek = get_fixture(LEAGUE_ID, SEASON_ID, int(match_id))
    return {"weeks": weeks, "currentWeek": currentWeek}
