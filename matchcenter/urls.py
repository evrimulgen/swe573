from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dje.views.statscenter', name='home'),
    url(r'^(\d*)/before/$', 'matchcenter.views.before'),
    url(r'^(\d*)/$', 'matchcenter.views.before'),
    url(r'^(\d*)/center/$', 'matchcenter.views.center'),
    url(r'^(\d*)/table/$', 'matchcenter.views.table'),
    url(r'^(\d*)/radar_webview/$', 'matchcenter.views.radar_webview'),

    # url(r'^partial/(?P<partial>.+)/(?P<match_id>\d*)/$', 'matchcenter.views.partial_renderer', name="partial" )

    url(r'^partial/fixture/(\d*)/$', 'matchcenter.views.partial_fixture'),
    url(r'^partial/events/(\d*)/$', 'matchcenter.views.partial_events'),
    # url(r'^api/(?P<path>\w+)$', 'matchcenter.views.router'),

    # url(r'^radar/$', 'dje.views.radar'),

    # url(r'^dje2/', include('dje2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
