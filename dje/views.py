# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

def home(request):
    a = []
    for x in range(1, 35):
        a.append(x)


    return render_to_response('statshome.html', {'weeklist': a})

def team(request,num):
    from random import randint
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
    team =""
    if int(num)==1:
        team = "Beşiktaş"
    elif int(num)==2:
        team = "Bursaspor"
    elif int(num)==3:
        team = "Eskişehirspor"
    elif int(num)==4:
        team = "Fenerbahçe"
    elif int(num)==5:
        team = "Galatasaray"
    elif int(num)==6:
        team = "Gençlerbirliği"
    elif int(num)==7:
        team = "Gaziantepspor"
    elif int(num)==8:
        team = "İstanbul BB"
    elif int(num)==9:
        team = "KDÇ Karabükspor"
    elif int(num)==13:
        team = "Mersin İY"
    elif int(num)==15:
        team = "Orduspor"
    elif int(num)==17:
        team = "Sivasspor"
    elif int(num)==18:
        team = "Trabzonspor"
    else:
        team = "Sentiospor"


    return render_to_response('statsteam.html', {'team_list': a, 'team':team, 'team_selected': int(num), 'player_list':b})


def league(request):
    from random import randint
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