from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dje.views.home', name='home'),
    url(r'^team/(\d*)/$', 'dje.views.team'),
    url(r'^team/$', 'dje.views.team'),
    url(r'^league/$', 'dje.views.league'),
    url(r'^before/$', 'dje.views.before'),
    url(r'^center/$', 'dje.views.center'),
    url(r'^summary/$', 'dje.views.summary'),
    url(r'^player/$', 'dje.views.player'),
    url(r'^table/$', 'dje.views.table'),
    url(r'^board/$', 'dje.views.chalkboard'),
    url(r'^api/(?P<path>\w+)$', 'dje.views.router'),

    # url(r'^dje2/', include('dje2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
