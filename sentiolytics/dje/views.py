# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

def home(request):
    a = []
    for x in range(1, 35):
        a.append(x)


    return render_to_response('statshome.html', {'weeklist': a, 'player_name': "Caner Turkmen"})

def team(request):
    return render_to_response('statsteam.html')

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