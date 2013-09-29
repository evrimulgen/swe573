"""
URL routes config for the stats center application
"""

from django.conf.urls import patterns, url
# from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', 'statcenter.views.statscenter', name='home'),
    url(r'^week/(\d*)/$', 'statcenter.views.home'),
    url(r'^team/(\d*)/$', 'statcenter.views.team'),
    url(r'^team/$', 'statcenter.views.teamselect'),
    url(r'^player/(\d*)/$', 'statcenter.views.playerselect'),
    url(r'^player/(?P<num>\d*)/(?P<player_id>\d*)/$', 'statcenter.views.player'),
    url(r'^compare/$', 'statcenter.views.compare'),
    url(r'^compare/player/$', 'statcenter.views.compareplayer'),
    url(r'^player/$', 'statcenter.views.player_teamselect'),
    url(r'^partial_teamstats/$', 'statcenter.views.partial_teamsidestats')
)

