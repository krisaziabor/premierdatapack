import os
import requests
import urllib.parse
import json
from flask import redirect, render_template, request, session
from functools import wraps



def datapack(teamOne, teamTwo):
    # find match IDs where teamOne is against teamTwo

    # logic: find ID of
    #array = []
    #rray.append(teamOne)
    #array.append(teamTwo)
    #return array

    desiredFixtures = []
    fixtures = obtainFixtureList()
    for match in range(len(fixtures)):
        if ((fixtures[match]['localteam_id'] == teamOne or fixtures[match]['localteam_id'] == teamTwo) and (fixtures[match]['visitorteam_id'] == teamOne or fixtures[match]['visitorteam_id'] == teamTwo)):
            desiredFixtures.append(fixtures[match])
            continue
        else:
            continue
    return desiredFixtures

def obtainFixtureList():
    try:
        api_key = os.environ.get("API_KEY")
        payload={}
        headers = {}
        url =f"https://soccer.sportmonks.com/api/v2.0/seasons/19734?api_token={api_key}&include=fixtures.events,fixtures.venue"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        quote = json.loads(textresponse)

        return (quote['data']['fixtures']['data'])

    except (KeyError, TypeError, ValueError):
        return None

def compareClubs(one, two, amt):
    results = {}
    try:
        api_key = os.environ.get("API_KEY")
        payload={}
        headers={}
        url=f"https://soccer.sportmonks.com/api/v2.0/head2head/{one}/{two}?api_token={api_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        quote = json.loads(textresponse)
        wins1 = 0
        wins2 = 0
        draws = 0
        historyCount = len(quote['data'])
        while amt > historyCount:
            amt -= 1
            if amt <= historyCount:
                break

        for match in range(amt):
            homeFC = int(quote['data'][match]['scores']['localteam_score'])
            awayFC = int(quote['data'][match]['scores']['visitorteam_score'])
            if (homeFC == awayFC):
                draws += 1
                continue
            else:
                homeID = int(quote['data'][match]['localteam_id'])
                awayID = int(quote['data'][match]['visitorteam_id'])

                if homeID == one and awayID == two:
                    if (homeFC > awayFC):
                        wins1 += 1
                    elif (awayFC > homeFC):
                        wins2 += 1
                elif (homeID == two) and (awayID == one):
                    if (homeFC > awayFC):
                        wins2 += 1
                    elif (awayFC > homeFC):
                        wins1 += 1
                else:
                    print(homeID)
                    print(awayID)
                    return None


        results.update({'wins1': wins1})
        results.update({'wins2': wins2})
        results.update({'draws': draws})
        return results

    except (KeyError, TypeError, ValueError):
        return None

#print(obtainFixtureList())

def reverseClubSearch(inputs, ivalue, output):
    if inputs != "name" and inputs != "img" and inputs != "id":
        return None
    elif output != "name" and output != "img" and output != "id":
        return None
    else:
        try:
            api_key = os.environ.get("API_KEY")
            payload = {}
            headers = {}
            url = f"https://soccer.sportmonks.com/api/v2.0/teams/season/19734?api_token={api_key}&include=venue"
            response = requests.request("GET", url, headers=headers, data=payload)
            textresponse = response.text
            response.raise_for_status()
        except requests.RequestException:
            return None

        try:
            quote = json.loads(textresponse)

            for position in range(20):
                if inputs == "img":
                    if ivalue == quote['data'][position]['logo_path']:
                        if output == "img":
                            return quote['data'][position]['logo_path']
                        elif output == "stadeImg":
                            return quote['data'][position]['venue']['data']['image_path']
                        else:
                            return quote['data'][position][output]
                    else:
                        continue
                else:
                    if ivalue == quote['data'][position][inputs]:
                        if output == "img":
                            return quote['data'][position]['logo_path']
                        elif output == "stadeImg":
                            return quote['data'][position]['venue']['data']['image_path']
                        else:
                            return quote['data'][position][output]
                    else:
                        continue
            return None

        except (KeyError, TypeError, ValueError):
            return None

#test = reverseClubSearch("id", 19, "name")
#print(test)

def obtainPremTeams(position):
    try:
        position -= 1
        api_key = os.environ.get("API_KEY")
        payload = {}
        headers = {}
        url = f"https://soccer.sportmonks.com/api/v2.0/teams/season/19734?api_token={api_key}&include=venue"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        quote = json.loads(textresponse)

        return {
            "name": quote['data'][position]['name'],
            "img": quote['data'][position]['logo_path'],
            "id": int(quote['data'][position]['id']),
            "stadeImg": quote['data'][position]['venue']['data']['image_path']
        }

    except (KeyError, TypeError, ValueError):
        return None

def obtainTeamData(position):
    try:
        position -= 1
        api_key = os.environ.get("API_KEY")
        payload={}
        headers = {}
        url = f"https://soccer.sportmonks.com/api/v2.0/standings/season/19734?api_token={api_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = json.loads(textresponse)
        # print (((quote['data'][0]['standings']['data'][0]['team_name'])))


        return {
            "teamID": quote['data'][0]['standings']['data'][position]['team_id'],
            "teamName": quote['data'][0]['standings']['data'][position]['team_name'],
            "points": int(quote["data"][0]["standings"]["data"][position]["points"]),
            "form": quote["data"][0]["standings"]["data"][position]["recent_form"],
            "playedGames": int(quote["data"][0]["standings"]["data"][position]["overall"]["games_played"]),
            "wins": int(quote["data"][0]["standings"]["data"][position]["overall"]["won"]),
            "draws": int(quote["data"][0]["standings"]["data"][position]["overall"]["draw"]),
            "losses": int(quote["data"][0]["standings"]["data"][position]["overall"]["lost"]),
            "goalsFor": int(quote["data"][0]["standings"]["data"][position]["overall"]["goals_scored"]),
            "goalsAgainst": int(quote["data"][0]["standings"]["data"][position]["overall"]["goals_against"]),
            "goalDifference": int(quote["data"][0]["standings"]["data"][position]["total"]["goal_difference"])
        }
    except (KeyError, TypeError, ValueError):
        return None

def accurateIMG(position):
    accurateID = int(obtainTeamData(position)['teamID'])
    desiredIMG = reverseClubSearch("id", accurateID, "img")
    return desiredIMG

#start is 2005/06
premYearID = [{'year':1586}, {'year':8}, {'year':14}, {'year':6}, {'year':11}, {'year':2}, {'year':9}, {'year':7}, {'year':3}, {'year':12}, {'year': 10}, {'year': 13}, {'year':6397}, {'year':12962}, {'year':16036}, {'year':17420}, {'year':18378}]
premIDYear = {1586: 2005, 8: 2006, 14: 2007, 6: 2008, 11: 2009, 2: 2010, 9: 2011, 7: 2012, 3: 2013, 12: 2014, 10: 2015, 13: 2016, 6397: 2017, 12962: 2018, 16036: 2019, 17420: 2020, 18378: 2021}

def findCommonYears(one, two):
    seasonIDArr = []
    for season in range(len(premYearID)):
        oneStatus = 0
        twoStatus = 0
        try:
            api_key = os.environ.get("API_KEY")
            payload={}
            headers={}
            url = f"https://soccer.sportmonks.com/api/v2.0/standings/season/{premYearID[season]['year']}?api_token={api_key}"
            response = requests.request("GET", url, headers=headers, data=payload)
            textresponse = response.text
            response.raise_for_status()

        except request.RequestException:
            return "None1"

        try:
            quote = json.loads(textresponse)

            for team in range(len(quote['data'][0]['standings']['data'])):
                if int(quote['data'][0]['standings']['data'][team]['team_id']) == one:
                    oneStatus += 1
                else:
                    continue

            for team in range(len(quote['data'][0]['standings']['data'])):
                if int(quote['data'][0]['standings']['data'][team]['team_id']) == two:
                    twoStatus += 1
                else:
                    continue

            if oneStatus == 1 and twoStatus == 1:
                seasonIDArr.append(premYearID[season]['year'])

        except (KeyError, TypeError, ValueError):
            return "None2"

    return seasonIDArr

def teamLeagueHistory(one, two):

    commonSznArr = findCommonYears(one, two)
    fullDict = []
    oneHss = []
    twoHss = []
    for season in range(len(commonSznArr)):
        try:
            api_key = os.environ.get("API_KEY")
            payload={}
            headers={}
            url = f"https://soccer.sportmonks.com/api/v2.0/standings/season/{premYearID[season]['year']}?api_token={api_key}"
            response = requests.request("GET", url, headers=headers, data=payload)
            textresponse = response.text
            response.raise_for_status()

        except request.RequestException:
            return "None1"

        try:
            quote = json.loads(textresponse)
            for team in range(len(quote['data'][0]['standings']['data'])):
                if int(quote['data'][0]['standings']['data'][team]['team_id']) == one:
                    tmp = commonSznArr[season]
                    yearSzn = premIDYear[tmp]
                    oneHss.append({yearSzn:quote['data'][0]['standings']['data'][team]['position']})
                else:
                    continue
            for team2 in range(len(quote['data'][0]['standings']['data'])):
                if int(quote['data'][0]['standings']['data'][team2]['team_id']) == two:
                    tmp2 = commonSznArr[season]
                    yearSzn2 = premIDYear[tmp2]
                    twoHss.append({yearSzn2:quote['data'][0]['standings']['data'][team2]['position']})
                else:
                    continue
        except (KeyError, TypeError, ValueError):
            return None

    fullDict.append({"one": oneHss})
    fullDict.append({"two": twoHss})
    return fullDict

def getListKeys(dict):
    list = ""
    for key in dict.keys():
        list = key

    return list

def getListValues(dict):
    list = ""
    for value in dict.values():
        list = value

    return list

def getsingleValue(dict):
    for key, value in dict.items():
        return value

#def datapresent(one, two):
    #data = teamLeagueHistory(one, two)
    #x_axis = []
    #for years in range(len(data[0]['one'])):
    #    x_axis.append(getListKeys(data[0]['one'][years]))
    #y_axis1 = []
    #for years1 in range(len(data[0]['one'])):
    #    y_axis1.append(getListValues(data[0]['one'][years1]))
    #y_axis2 = []
    #for years2 in range(len(data[1]['two'])):
      #  y_axis2.append(getListValues(data[1]['two'][years2]))
    #return[x_axis, y_axis1, y_axis2]

def getNextTeamIMG(position):
    position = int(obtainTeamData(position)['teamID'])
    try:
        api_key = os.environ.get("API_KEY")
        payload={}
        headers={}
        url = f"https://soccer.sportmonks.com/api/v2.0/teams/{position}?api_token={api_key}&include=upcoming"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except request.RequestException:
            return "None1"

    try:
        quote = json.loads(textresponse)
        nextMatch = quote['data']['upcoming']['data'][0]
        nextMatchPoss = []
        nextMatchPoss.append(nextMatch['localteam_id'])
        nextMatchPoss.append(nextMatch['visitorteam_id'])
        desiredID = 0
        for possibility in range(2):
            if int(nextMatchPoss[possibility]) != position:
                desiredID = nextMatchPoss[possibility]
            else:
                continue
        desiredIMG = reverseClubSearch("id", desiredID, "img")
        return desiredIMG

    except (KeyError, TypeError, ValueError):
        return None

def getPlayerName(id):
    try:
        api_key = os.environ.get("API_KEY")
        payload={}
        headers={}
        url = f"https://soccer.sportmonks.com/api/v2.0/players/{id}?api_token={api_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except request.RequestException:
            return "None1"

    try:
        quote = json.loads(textresponse)
        return quote['data']['fullname']

    except (ValueError):
        return "None2"

def dictValuesStringtoInt(dict):
   #Given a list of dictionaries, return a list of dictionaries with all values converted to integers
    newdict = {}
    for key, value in dict.items():
        newdict[key] = round(float(value))
    return newdict

def playersUnavailable(team):
    injurylist = []
    answer = []
    try:
        api_key = os.environ.get("API_KEY")
        payload={}
        headers={}
        url = f"https://soccer.sportmonks.com/api/v2.0/teams/{team}?api_token={api_key}&include=squad"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except request.RequestException:
            return "None1"

    try:
        quote = json.loads(textresponse)
        potentialInjuries = []
        for player in range(len(quote['data']['squad']['data'])):
                status = (quote['data']['squad']['data'][player]['injured'])
                potentialInjuries.append({int(quote['data']['squad']['data'][player]['player_id']): status})
        for entry in potentialInjuries:
            for key, value in entry.items():
                if value is None:
                    entry[key] = 0
        for entry in potentialInjuries:
            '''if status is true, add player to injurylist'''
            for key, value in entry.items():
                if value == True:
                    injurylist.append(key)

        for entry in injurylist:
            answer.append(getPlayerName(entry))
            return answer
    except (ValueError):
        return "None2"

def topAssister(team):
    highestAssister = []
    try:
        api_key = os.environ.get("API_KEY")
        payload={}
        headers={}
        url = f"https://soccer.sportmonks.com/api/v2.0/teams/{team}?api_token={api_key}&include=squad"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except request.RequestException:
            return "None1"

    try:
        quote = json.loads(textresponse)
        potentialAssisters = []
        for player in range(len(quote['data']['squad']['data'])):
                assists = (quote['data']['squad']['data'][player]['assists'])
                potentialAssisters.append({int(quote['data']['squad']['data'][player]['player_id']): assists})
        for entry in potentialAssisters:
            for key, value in entry.items():
                if value is None:
                    entry[key] = 0
        highestAssister = max(potentialAssisters, key=lambda x: list(x.values())[0])
        playername = getPlayerName(getListKeys(highestAssister))
        return [playername, int(getListValues(highestAssister))]
    except (ValueError):
        return "None2"

def topGoalscorer(team):
    highestGoalscorer = []
    try:
        api_key = os.environ.get("API_KEY")
        payload={}
        headers={}
        url = f"https://soccer.sportmonks.com/api/v2.0/teams/{team}?api_token={api_key}&include=squad"
        response = requests.request("GET", url, headers=headers, data=payload)
        textresponse = response.text
        response.raise_for_status()

    except request.RequestException:
            return "None1"

    try:
        quote = json.loads(textresponse)
        potentialGoalscorers = []
        for player in range(len(quote['data']['squad']['data'])):
                goals = (quote['data']['squad']['data'][player]['goals'])
                potentialGoalscorers.append({int(quote['data']['squad']['data'][player]['player_id']): goals})
        for entry in potentialGoalscorers:
            for key, value in entry.items():
                if value is None:
                    entry[key] = 0
        highestGoalscorer = max(potentialGoalscorers, key=lambda x: list(x.values())[0])
        playername = getPlayerName(getListKeys(highestGoalscorer))
        return [playername, int(getListValues(highestGoalscorer))]
    except (ValueError):
        return "None2"


print(playersUnavailable(6))

