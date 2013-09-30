import os
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

urlpatterns = patterns('',

        # special paths
        url(r'^api/(?P<path>\w+)$', 'dje.views.router'),
        url(r'^(\d*)/radar_vebview/$', 'dje.views.radar_vebview'),

        # old match center
        url(r'^(\d*)/before/$', 'dje.views.before'),
        url(r'^(\d*)/$', 'dje.views.matchcenter'),
        url(r'^(\d*)/center/$', 'dje.views.center'),
        url(r'^(\d*)/table/$', 'dje.views.table'),
        url(r'^board/$', 'dje.views.chalkboard'),
        url(r'^radar/$', 'dje.views.radar'),

        # favicon, suspended for now
        # url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '../static/images/favicon.ico'}),

        # new match center
        url(r'^new/', include('matchcenter.urls')),

        # static path (MUST NOT BE USED IN PRODUCTION)
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static_path, 'show_indexes': True}),

        # stats center
        url(r'^$', 'dje.views.statscenter', name='home'),
        url(r'^week/(\d*)/$', 'dje.views.home'),
        url(r'^team/(\d*)/$', 'dje.views.team'),
        url(r'^team/$', 'dje.views.team2'),
        url(r'^player/(\d*)/$', 'dje.views.player3'),
        url(r'^player/(?P<num>\d*)/(?P<player_id>\d*)/$', 'dje.views.playerx'),
        url(r'^league/$', 'dje.views.league'),
        url(r'^compare/$', 'dje.views.compare'),
        url(r'^summary/$', 'dje.views.summary'),
        url(r'^player/$', 'dje.views.player'),
        url(r'^matchinfo/(\d*)/$', 'matchcenter.views.matchinfo'),
        # new stats center
        url(r'^ns/', include('statcenter.urls')),
)
