from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
       # Examples:
       url(r'^$', 'dje.views.statscenter', name='home'),
       url(r'^week/(\d*)/$', 'dje.views.home'),
       url(r'^team/(\d*)/$', 'dje.views.team'),
       url(r'^team/$', 'dje.views.team2'),
       url(r'^player/(\d*)/$', 'dje.views.player3'),
       url(r'^player/(?P<num>\d*)/(?P<player_id>\d*)/$', 'dje.views.playerx'),
       url(r'^league/$', 'dje.views.league'),
       url(r'^(\d*)/before/$', 'dje.views.before'),
       url(r'^(\d*)/$', 'dje.views.matchcenter'),
       url(r'^(\d*)/center/$', 'dje.views.center'),
       url(r'^compare/$', 'dje.views.compare'),
       url(r'^summary/$', 'dje.views.summary'),
       url(r'^player/$', 'dje.views.player'),
       url(r'^(\d*)/table/$', 'dje.views.table'),
       url(r'^board/$', 'dje.views.chalkboard'),
       url(r'^(\d*)/radar_vebview/$', 'dje.views.radar_vebview'),
       url(r'^api/(?P<path>\w+)$', 'dje.views.router'),
       (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '../static/images/favicon.ico'}),

    url(r'^radar/$', 'dje.views.radar'),

                       # url(r'^dje2/', include('dje2.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
)
