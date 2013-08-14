
"""
Utilities for Sentiolytics Frontend
"""

import urllib2
import django.utils.simplejson as json

def service_request(id, data):
    url = "http://sentio.cloudapp.net:8080/api/%s" % id
    if data:
        d = json.dumps(data)
        result = urllib2.urlopen(url,d)
    return result.read()


def try_service():
    data = {"leagueId":1,"seasonId":8918,"matchId":11730060}
    teams = service_request("GetMatchData", data)
    j_obj = json.loads(teams)
    datalist = j_obj["data"]
    matchDataDict = []
    homeDataDict = []
    awayDataDict = []

    homeDistance = 0
    awayDistance = 0
    homeSpeed = 0
    awaySpeed = 0
    homeHIR = 0
    awayHIR = 0
    homeTotalPass = 0
    awayTotalPass = 0
    homeSuccessfulPass = 0
    awaySuccessfulPass = 0

    homeTotalShot = 0
    awayTotalShot = 0
    homeSuccessfulShot = 0
    awaySuccessfulShot = 0

    homeTotalCross = 0
    awayTotalCross = 0
    homeSuccessfulCross = 0
    awaySuccessfulCross = 0

    homeFoul = 0
    awayFoul = 0

    for dat in datalist:
        matchDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
        if dat[0] == 2:
            homeDistance += int(dat[4] or 0)
            homeSpeed += int(dat[5] or 0)
            homeHIR += int(dat[6] or 0)
            homeTotalPass += int(dat[7] or 0)
            homeSuccessfulPass += int(dat[8] or 0)
            homeTotalShot += int(dat[9] or 0)
            homeSuccessfulShot += int(dat[10] or 0)
            homeTotalCross += int(dat[11] or 0)
            homeSuccessfulCross += int(dat[12] or 0)
            homeFoul += int(dat[13] or 0)

            homeDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})
        elif dat[0] == 1:

            awayDistance += int(dat[4] or 0)
            awaySpeed += int(dat[5] or 0)
            awayHIR += int(dat[6] or 0)
            awayTotalPass += int(dat[7] or 0)
            awaySuccessfulPass += int(dat[8] or 0)
            awayTotalShot += int(dat[9] or 0)
            awaySuccessfulShot += int(dat[10] or 0)
            awayTotalCross += int(dat[11] or 0)
            awaySuccessfulCross += int(dat[12] or 0)
            awayFoul += int(dat[13] or 0)

            awayDataDict.append({'teamId':dat[0],'playerName':dat[1],'playerId':dat[2],'jerseyNumber':dat[3],'totalDistance':int(dat[4] or 0),'averageSpeed':int(dat[5] or 0),'HIRDistance':int(dat[6] or 0),'totalPass':int(dat[7] or 0),'successfulPass':int(dat[8] or 0),'passRatio':int(int(dat[7] or 0)-int(dat[8] or 1)*100),'totalShot':int(dat[9] or 0),'successfulShot':int(dat[10] or 0),'shotRatio':int(int(dat[9] or 0)/int(dat[10] or 1)*100),'totalCross':int(dat[11] or 0),'successfulCross':int(dat[12] or 0),'crossRatio':int(int(dat[11] or 0)/int(dat[12] or 1)*100),'foulCommitted':int(dat[13] or 0),'foulAgainst':int(dat[14] or 0)})

    homeSpeed /= int(len(homeDataDict) or 1)
    awaySpeed /= int(len(awayDataDict) or 1)

    homePassRatio = int(homeSuccessfulPass/int(homeTotalPass or 1) * 100)
    awayPassRatio = int(awaySuccessfulPass/int(awayTotalPass or 1) * 100)

    homeShotRatio = int(homeSuccessfulShot/int(homeTotalShot or 1) * 100)
    awayShotRatio = int(awaySuccessfulShot/int(awayTotalShot or 1) * 100)

    homeCrossRatio = int(homeSuccessfulCross/int(homeTotalCross or 1) * 100)
    awayCrossRatio = int(awaySuccessfulCross/int(awayTotalCross or 1) * 100)

    homeDistancePercent = 0
    awayDistancePercent = 0
    if homeDistance+awayDistance < 1:
        homeDistancePercent = 50
    else:
        homeDistancePercent = int(homeDistance/(homeDistance+awayDistance)*100)
    awayDistancePercent = 100 - homeDistancePercent

    homeSpeedPercent = 0
    awaySpeedPercent = 0
    if homeSpeed+awaySpeed < 1:
        homeSpeedPercent = 50
    else:
        homeSpeedPercent = int(homeSpeed/(homeSpeed+awaySpeed)*100)
    awaySpeedPercent = 100 - homeSpeedPercent

    homeHIRPercent = 0
    awayHIRPercent = 0
    if homeHIR+awayHIR < 1:
        homeHIRPercent = 50
    else:
        homeHIRPercent = int(homeHIR/(homeHIR+awayHIR)*100)
        print (homeHIR/float(homeHIR+awayHIR))
    awayHIRPercent = 100 - homeHIRPercent

    homeTotalPassPercent = 0
    awayTotalPassPercent = 0
    if homeTotalPass+awayTotalPass < 1:
        homeTotalPassPercent = 50
    else:
        homeTotalPassPercent = int(homeTotalPass/(homeTotalPass+awayTotalPass)*100)
    awayTotalPassPercent = 100 - homeTotalPassPercent

    homeSuccessfulPassPercent = 0
    awaySuccessfulPassPercent = 0
    if homeSuccessfulPass+awaySuccessfulPass < 1:
        homeSuccessfulPassPercent = 50
    else:
        homeSuccessfulPassPercent = int(homeSuccessfulPass/(homeSuccessfulPass+awaySuccessfulPass)*100)
    awaySuccessfulPassPercent = 100 - homeSuccessfulPassPercent

    homePassRatioPercent = 0
    awayPassRatioPercent = 0
    if homePassRatio+awayPassRatio < 1:
        homePassRatioPercent = 50
    else:
        homePassRatioPercent = int(homePassRatio/(homePassRatio+awayPassRatio)*100)
    awayPassRatioPercent = 100 - homePassRatioPercent

    homeTotalShotPercent = 0
    awayTotalShotPercent = 0
    if homeTotalShot+awayTotalShot < 1:
        homeTotalShotPercent = 50
    else:
        homeTotalShotPercent = homeTotalShot/(homeTotalShot+awayTotalShot)*100
    awayTotalShotPercent = 100 - homeTotalShotPercent

    homeSuccessfulShotPercent = 0
    awaySuccessfulShotPercent = 0
    if homeSuccessfulShot+awaySuccessfulShot < 1:
        homeSuccessfulShotPercent = 50
    else:
        homeSuccessfulShotPercent = int((homeSuccessfulShot/(homeSuccessfulShot+awaySuccessfulShot))*100)
    awaySuccessfulShotPercent = 100 - homeSuccessfulShotPercent

    homeShotRatioPercent = 0
    awayShotRatioPercent = 0
    if homeShotRatio+awayShotRatio < 1:
        homeShotRatioPercent = 50
    else:
        homeShotRatioPercent = int(homeShotRatio/(homeShotRatio+awayShotRatio)*100)
    awayShotRatioPercent = 100 - homeShotRatioPercent

    homeTotalCrossPercent = 0
    awayTotalCrossPercent = 0
    if homeTotalCross+awayTotalCross < 1:
        homeTotalCrossPercent = 50
    else:
        homeTotalCrossPercent = int(homeTotalCross/(homeTotalCross+awayTotalCross)*100)
    awayTotalCrossPercent = 100 - homeTotalCrossPercent

    homeSuccessfulCrossPercent = 0
    awaySuccessfulCrossPercent = 0
    if homeSuccessfulCross+awaySuccessfulCross < 1:
        homeSuccessfulCrossPercent = 50
    else:
        homeSuccessfulCrossPercent = int(homeSuccessfulCross/(homeSuccessfulCross+awaySuccessfulCross)*100)
    awaySuccessfulCrossPercent = 100 - homeSuccessfulCrossPercent

    homeCrossRatioPercent = 0
    awayCrossRatioPercent = 0
    if homeCrossRatio+awayCrossRatio < 1:
        homeCrossRatioPercent = 50
    else:
        homeCrossRatioPercent = int(homeCrossRatio/(homeCrossRatio+awayCrossRatio)*100)
    awayCrossRatioPercent = 100 - homeCrossRatioPercent

    homeFoulPercent = 0
    awayFoulPercent = 0
    if homeFoul+awayFoul < 1:
        homeFoulPercent = 50
    else:
        homeFoulPercent = int(homeFoul/(homeFoul+awayFoul)*100)
    awayFoulPercent = 100 - homeFoulPercent

    teamStatsDict = []
    teamStatsDict.append({'homeDistance':homeDistance,'homeDistancePercent':homeDistancePercent,'awayDistance':awayDistance,'awayDistancePercent':awayDistancePercent,'homeSpeed':homeSpeed,'homeSpeedPercent':homeSpeedPercent,'awaySpeed':awaySpeed,'awaySpeedPercent':awaySpeedPercent,'homeHIR':homeHIR,'homeHIRPercent':homeHIRPercent,'awayHIR':awayHIR,'awayHIRPercent':awayHIRPercent,'homeTotalPass':homeTotalPass,'homeTotalPassPercent':homeTotalPassPercent,'awayTotalPass':awayTotalPass,'awayTotalPassPercent':awayTotalPassPercent,'homeSuccessfulPass':homeSuccessfulPass,'homeSuccessfulPassPercent':homeSuccessfulPassPercent,'awaySuccessfulPass':awaySuccessfulPass,'awaySuccessfulPassPercent':awaySuccessfulPassPercent,'homePassRatio':homePassRatio,'homePassRatioPercent':homePassRatioPercent,'awayPassRatio':awayPassRatio,'awayPassRatioPercent':awayPassRatioPercent,'homeTotalShot':homeTotalShot,'homeTotalShotPercent':homeTotalShotPercent,'awayTotalShot':awayTotalShot,'awayTotalShotPercent':awayTotalShotPercent,'homeSuccessfulShot':homeSuccessfulShot,'homeSuccessfulShotPercent':homeSuccessfulShotPercent,'awaySuccessfulShot':awaySuccessfulShot,'awaySuccessfulShotPercent':awaySuccessfulShotPercent,'homeShotRatio':homeShotRatio,'homeShotRatioPercent':homeShotRatioPercent,'awayShotRatio':awayShotRatio,'awayShotRatioPercent':awayShotRatioPercent,'homeTotalCross':homeTotalCross,'homeTotalCrossPercent':homeTotalCrossPercent,'awayTotalCross':awayTotalCross,'awayTotalCrossPercent':awayTotalCrossPercent,'homeSuccessfulCross':homeSuccessfulCross,'homeSuccessfulCrossPercent':homeSuccessfulCrossPercent,'awaySuccessfulCross':awaySuccessfulCross,'awaySuccessfulCrossPercent':awaySuccessfulCrossPercent,'homeCrossRatio':homeCrossRatio,'homeCrossRatioPercent':homeCrossRatioPercent,'awayCrossRatio':awayCrossRatio,'awayCrossRatioPercent':awayCrossRatioPercent,'homeFoul':homeFoul,'homeFoulPercent':homeFoulPercent,'awayFoul':awayFoul,'awayFoulPercent':awayFoulPercent})






try_service()