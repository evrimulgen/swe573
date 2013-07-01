# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from random import randint
from django.http import HttpRequest
import urllib2, urllib

def home(request):
    a = []
    for x in range(1, 35):
        a.append(x)


    return render_to_response('statshome.html', {'weeklist': a})

def team(request, num):
    from random import randint
    a =[]
    for x in range(1, 19):
        a.append(x)

#    post_data = [('name','Gladys'),]     # a sequence of two element tuples
#    result = urllib2.urlopen('http://example.com', urllib.urlencode(post_data))
#    content = result.read()

    post_data = '{"team_ids":["1"]}'
    result = urllib2.urlopen('http://sentio.cloudapp.net:8080/api/GetTeamsInformation', post_data)
    content = result.read()

    b = []
#    for x in range(1, 35):
#        match = randint(0,34)
#        min = randint(0,12432)
#        goal = randint(0,25)
#        assist = randint(0,16)
#        yellow = randint(0,8)
#        red = randint(0,4)
#        run = randint(0,11300)
#    b.append({'jersey': "%s"%x, 'name': 'Serhat Kurtulus', 'match': int(match), 'min': int(min), 'goal': int(goal), 'assist': int(assist), 'yellow': int(yellow), 'red': int(red), 'run': int(run)})


    return render_to_response('statsteam.html', {'team_list': a, 'team':team, 'team_selected': int(num), 'player_list':b})


def league(request):
    a =[]
    for x in range(1, 19):
        a.append(x)
    b = []

    for x in range(1, 35):
        match = randint(0,34)
        min = randint(0,12432)
        goal = randint(0,25)
        assist = randint(0,16)
        yellow = randint(0,8)
        red = randint(0,4)
        run = randint(0,11300)
        b.append({'jersey': "%s"%x, 'name': 'Serhat Kurtulus', 'match': int(match), 'min': int(min), 'goal': int(goal), 'assist': int(assist), 'yellow': int(yellow), 'red': int(red), 'run': int(run)})

    c = []
    for x in range(1, 35):
        c.append(x)

    return render_to_response('statsleague.html', {'weeklist': c , 'player_list':b, 'team_list': a})


def before(request):
    return render_to_response('beforematch.html')
def center(request):
    return render_to_response('matchcenter.html', {'homeTeam': u"Fenerbahçe", 'awayTeam': u"Galatasaray", 'stadiumName': u"ŞÜKRÜ SARAÇOĞLU STADI", 'homeLogo': "images/logo4.png", 'awayLogo':"images/logo5.png"})
def summary(request):
    return render_to_response('matchsummary.html')
def player(request):
    return render_to_response('playerstats.html')
def table(request):
    return render_to_response('matchtable.html')