import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import obtainTeamData, obtainPremTeams, datapack, reverseClubSearch, compareClubs, getNextTeamIMG, accurateIMG, topGoalscorer, topAssister, playersUnavailable


# I created a forgot password page

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# my code begins

# for league standings
team1 = obtainTeamData(1)
team2 = obtainTeamData(2)
team3 = obtainTeamData(3)
team4 = obtainTeamData(4)
team5 = obtainTeamData(5)
team6 = obtainTeamData(6)
team7 = obtainTeamData(7)
team8 = obtainTeamData(8)
team9 = obtainTeamData(9)
team10 = obtainTeamData(10)
team11 = obtainTeamData(11)
team12 = obtainTeamData(12)
team13 = obtainTeamData(13)
team14 = obtainTeamData(14)
team15 = obtainTeamData(15)
team16 = obtainTeamData(16)
team17 = obtainTeamData(17)
team18 = obtainTeamData(18)
team19 = obtainTeamData(19)
team20 = obtainTeamData(20)

# this gets a club's accurate image based on their current league position
club1 = accurateIMG(1)
club2 = accurateIMG(2)
club3 = accurateIMG(3)
club4 = accurateIMG(4)
club5 = accurateIMG(5)
club6 = accurateIMG(6)
club7 = accurateIMG(7)
club8 = accurateIMG(8)
club9 = accurateIMG(9)
club10 = accurateIMG(10)
club11 = accurateIMG(11)
club12 = accurateIMG(12)
club13 = accurateIMG(13)
club14 = accurateIMG(14)
club15 = accurateIMG(15)
club16 = accurateIMG(16)
club17 = accurateIMG(17)
club18 = accurateIMG(18)
club19 = accurateIMG(19)
club20 = accurateIMG(20)

# this gets a the badge of a team's upcoming opponent – based on the original team's league position
nextclub1 = getNextTeamIMG(1)
nextclub2 = getNextTeamIMG(2)
nextclub3 = getNextTeamIMG(3)
nextclub4 = getNextTeamIMG(4)
nextclub5 = getNextTeamIMG(5)
nextclub6 = getNextTeamIMG(6)
nextclub7 = getNextTeamIMG(7)
nextclub8 = getNextTeamIMG(8)
nextclub9 = getNextTeamIMG(9)
nextclub10 = getNextTeamIMG(10)
nextclub11 = getNextTeamIMG(11)
nextclub12 = getNextTeamIMG(12)
nextclub13 = getNextTeamIMG(13)
nextclub14 = getNextTeamIMG(14)
nextclub15 = getNextTeamIMG(15)
nextclub16 = getNextTeamIMG(16)
nextclub17 = getNextTeamIMG(17)
nextclub18 = getNextTeamIMG(18)
nextclub19 = getNextTeamIMG(19)
nextclub20 = getNextTeamIMG(20)

# the next 20 functions are carbon copies. thus, i will only comment for the first function and its details.
@app.route("/next1", methods=["GET", "POST"])
def next1():

    # it is not neccessary to differentiate between GET and POST methods here
    # the two club ID numbers are retrieved from the user's selection of the "next badge"
    oneFC = int(team1["teamID"])
    # reversesearch from image path to finding club's id
    twoFC = int(reverseClubSearch("img", nextclub1, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    # retrieving two possible matchups between sides
    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])

    # retrieving club names and badges of two sides
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    # print(fixlist)

    # will later be filled with details of goals
    goals = []
    # will later be filled with details of final score, and goals for either side
    ft = " "
    homeTeam = " "
    awayTeam = " "

    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            # if any type of goal has occurred, add to goals array
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    # if the homeTeam string is empty, the first match has not been played yet. This means some data should not be returned to the site.
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        # warning message for potential inaccuracies
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("datapack.html", dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2, goalScorer1 = goalScorer1, goalScorer2 = goalScorer2)

    # this means the first game has been played. we can proceed to fill in data over the occurrance of the first match
    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            #adding to arrays for goalscorers and the corresponding minute
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    #these data points do not rely on the first game's occurrence.
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next2", methods=["GET", "POST"])
def next2():
    oneFC = int(team2["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub2, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next3", methods=["GET", "POST"])
def next3():
    oneFC = int(team3["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub3, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next4", methods=["GET", "POST"])
def next4():
    oneFC = int(team4["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub4, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)


@app.route("/next5", methods=["GET", "POST"])
def next5():
    oneFC = int(team5["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub5, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next6", methods=["GET", "POST"])
def next6():
    oneFC = int(team6["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub6, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next7", methods=["GET", "POST"])
def next7():
    oneFC = int(team7["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub7, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next8", methods=["GET", "POST"])
def next8():
    oneFC = int(team8["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub8, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next9", methods=["GET", "POST"])
def next9():
    oneFC = int(team9["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub9, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next10", methods=["GET", "POST"])
def next10():
    oneFC = int(team10["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub10, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next11", methods=["GET", "POST"])
def next11():
    oneFC = int(team11["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub11, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next12", methods=["GET", "POST"])
def next12():
    oneFC = int(team12["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub12, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next13", methods=["GET", "POST"])
def next13():
    oneFC = int(team13["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub13, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next14", methods=["GET", "POST"])
def next14():
    oneFC = int(team14["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub14, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next15", methods=["GET", "POST"])
def next15():
    oneFC = int(team15["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub15, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next16", methods=["GET", "POST"])
def next16():
    oneFC = int(team16["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub16, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next17", methods=["GET", "POST"])
def next17():
    oneFC = int(team17["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub17, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next18", methods=["GET", "POST"])
def next18():
    oneFC = int(team18["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub18, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)

    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

@app.route("/next19", methods=["GET", "POST"])
def next19():
    oneFC = int(team19["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub19, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)


@app.route("/next20", methods=["GET", "POST"])
def next20():
    oneFC = int(team20["teamID"])
    twoFC = int(reverseClubSearch("img", nextclub20, "id"))

    if (oneFC == twoFC):
        flash("please pick two different teams this time! :) ")
        return redirect("/")

    results = datapack(oneFC, twoFC)
    fixlist = []
    for match in range(len(results)):
        fixlist.append(results[match])
    nameOneFC = reverseClubSearch("id", oneFC, "name")
    nameTwoFC = reverseClubSearch("id", twoFC, "name")
    imgOneFC = reverseClubSearch("id", oneFC, "img")
    imgTwoFC = reverseClubSearch("id", twoFC, "img")
    print(fixlist)
    goals = []
    ft = " "
    homeTeam = " "
    awayTeam = " "
    for matchday in range(len(fixlist)):
        for moment in range(len(fixlist[matchday]['events']['data'])):
            if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                goals.append(fixlist[matchday]['events']['data'][moment])
                ft = fixlist[matchday]['scores']['ft_score']
                homeTeam = fixlist[matchday]['localteam_id']
                awayTeam = fixlist[matchday]['visitorteam_id']
            else:
                continue
    if (homeTeam == " "):
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
        return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

    goalscorers1 = []
    goalscorers2 = []
    minutes1 = []
    minutes2 = []
    homeFC = reverseClubSearch("id", int(homeTeam), "name")
    awayFC = reverseClubSearch("id", int(awayTeam), "name")
    for goal in range(len(goals)):
        if int(goals[goal]['team_id']) == oneFC:
            goalscorers1.append(goals[goal]['player_name'])
            minutes1.append(goals[goal]['minute'])
        else:
            goalscorers2.append(goals[goal]['player_name'])
            minutes2.append(goals[goal]['minute'])
    clubComparison = compareClubs(oneFC, twoFC, 10)
    wins1 = clubComparison['wins1']
    wins2 = clubComparison['wins2']
    draws = clubComparison['draws']
    goalScorer1 = topGoalscorer(oneFC)
    goalScorer2 = topGoalscorer(twoFC)
    topAssister1 = topAssister(oneFC)
    topAssister2 = topAssister(twoFC)
    injuredPlayers1 = playersUnavailable(oneFC)
    injuredPlayers2 = playersUnavailable(twoFC)
    # print(clubComparison)
    flash("Due to frequent re-arranging of the Premier League schedule, some of the next matches are not fully accurate, as the API does not update frequently. Please reference premierleague.com for the most recent updates.")
    return render_template("nextteam.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)


@app.route("/", methods=["GET", "POST"])
def welcomehome():
    """Show home page"""

    # this mean someone is visiting the site, not publishing details for use to manipulate (as of yet)
    if request.method == "GET":
        return render_template("home.html",
        name1 = team1["teamName"], img1 = club1, img2 = club2, img3 = club3, img4 = club4, img5 = club5, img6 = club6, img7 = club7, img8 = club8, img9 = club9, img10 = club10, img11 = club11, img12 = club12, img13 = club13, img14 = club14, img15 = club15, img16 = club16, img17 = club17, img18 = club18, img19 = club19, img20 = club20, name2 = team2["teamName"], name3 = team3["teamName"], name4 = team4["teamName"], name5 = team5["teamName"], name6 = team6["teamName"], name7 = team7["teamName"], name8 = team8["teamName"], name9 = team9["teamName"], name10 = team10["teamName"], name11 = team11["teamName"], name12 = team12["teamName"], name13 = team13["teamName"], name14 = team14["teamName"], name15 = team15["teamName"], name16 = team16["teamName"], name17 = team17["teamName"], name18 = team18["teamName"], name19 = team19["teamName"], name20 = team20["teamName"], points1 = team1["points"], points2 = team2["points"], points3 = team3["points"], points4 = team4["points"], points5 = team5["points"], points6 = team6["points"], points7 = team7["points"], points8 = team8["points"], points9 = team9["points"], points10 = team10["points"], points11 = team11["points"], points12 = team12["points"], points13 = team13["points"], points14 = team14["points"], points15 = team15["points"], points16 = team16["points"], points17 = team17["points"], points18 = team18["points"], points19 = team19["points"], points20 = team20["points"], form1 = team1["form"], form2 = team2["form"], form3 = team3["form"], form4 = team4["form"], form5 = team5["form"], form6 = team6["form"], form7 = team7["form"], form8 = team8["form"], form9 = team9["form"], form10 = team10["form"], form11 = team11["form"], form12 = team12["form"], form13 = team13["form"], form14 = team14["form"], form15 = team15["form"], form16 = team16["form"], form17 = team17["form"], form18 = team18["form"], form19 = team19["form"], form20 = team20["form"], pg1 = team1["playedGames"], pg2 = team2["playedGames"], pg3 = team3["playedGames"], pg4 = team4["playedGames"], pg5 = team5["playedGames"], pg6 = team6["playedGames"], pg7 = team7["playedGames"], pg8 = team8["playedGames"], pg9 = team9["playedGames"], pg10 = team10["playedGames"], pg11 = team11["playedGames"], pg12 = team12["playedGames"], pg13 = team13["playedGames"], pg14 = team14["playedGames"], pg15 = team15["playedGames"], pg16 = team16["playedGames"], pg17 = team17["playedGames"], pg18 = team18["playedGames"], pg19 = team19["playedGames"], pg20 = team20["playedGames"], wins1 = team1["wins"], wins2 = team2["wins"], wins3 = team3["wins"], wins4 = team4["wins"], wins5 = team5["wins"], wins6 = team6["wins"], wins7 = team7["wins"], wins8 = team8["wins"], wins9 = team9["wins"], wins10 = team10["wins"], wins11 = team11["wins"], wins12 = team12["wins"], wins13 = team13["wins"], wins14 = team14["wins"], wins15 = team15["wins"], wins16 = team16["wins"], wins17 = team17["wins"], wins18 = team18["wins"], wins19 = team19["wins"], wins20 = team20["wins"], draws1 = team1["draws"], draws2 = team2["draws"], draws3 = team3["draws"], draws4 = team4["draws"], draws5 = team5["draws"], draws6 = team6["draws"], draws7 = team7["draws"], draws8 = team8["draws"], draws9 = team9["draws"], draws10 = team10["draws"], draws11 = team11["draws"], draws12 = team12["draws"], draws13 = team13["draws"], draws14 = team14["draws"], draws15 = team15["draws"], draws16 = team16["draws"], draws17 = team17["draws"], draws18 = team18["draws"], draws19 = team19["draws"], draws20 = team20["draws"], losses1 = team1["losses"], losses2 = team2["losses"], losses3 = team3["losses"], losses4 = team4["losses"], losses5 = team5["losses"], losses6 = team6["losses"], losses7 = team7["losses"], losses8 = team8["losses"], losses9 = team9["losses"], losses10 = team10["losses"], losses11 = team11["losses"], losses12 = team12["losses"], losses13 = team13["losses"], losses14 = team14["losses"], losses15 = team15["losses"], losses16 = team16["losses"], losses17 = team17["losses"], losses18 = team18["losses"], losses19 = team19["losses"], losses20 = team20["losses"], gf1 = team1["goalsFor"], gf2 = team2["goalsFor"], gf3 = team3["goalsFor"], gf4 = team4["goalsFor"], gf5 = team5["goalsFor"], gf6 = team6["goalsFor"], gf7 = team7["goalsFor"], gf8 = team8["goalsFor"], gf9 = team9["goalsFor"], gf10 = team10["goalsFor"], gf11 = team11["goalsFor"], gf12 = team12["goalsFor"], gf13 = team13["goalsFor"], gf14 = team14["goalsFor"], gf15 = team15["goalsFor"], gf16 = team16["goalsFor"], gf17 = team17["goalsFor"], gf18 = team18["goalsFor"], gf19 = team19["goalsFor"], gf20 = team20["goalsFor"], ga1 = team1["goalsAgainst"], ga2 = team2["goalsAgainst"], ga3 = team3["goalsAgainst"], ga4 = team4["goalsAgainst"], ga5 = team5["goalsAgainst"], ga6 = team6["goalsAgainst"], ga7 = team7["goalsAgainst"], ga8 = team8["goalsAgainst"], ga9 = team9["goalsAgainst"], ga10 = team10["goalsAgainst"], ga11 = team11["goalsAgainst"], ga12 = team12["goalsAgainst"], ga13 = team13["goalsAgainst"], ga14 = team14["goalsAgainst"], ga15 = team15["goalsAgainst"], ga16 = team16["goalsAgainst"], ga17 = team17["goalsAgainst"], ga18 = team18["goalsAgainst"], ga19 = team19["goalsAgainst"], ga20 = team20["goalsAgainst"], gd1 = team1["goalDifference"], gd2 = team2["goalDifference"], gd3 = team3["goalDifference"], gd4 = team4["goalDifference"], gd5 = team5["goalDifference"], gd6 = team6["goalDifference"], gd7 = team7["goalDifference"], gd8 = team8["goalDifference"], gd9 = team9["goalDifference"], gd10 = team10["goalDifference"], gd11 = team11["goalDifference"], gd12 = team12["goalDifference"], gd13 = team13["goalDifference"], gd14 = team14["goalDifference"], gd15 = team15["goalDifference"], gd16 = team16["goalDifference"], gd17 = team17["goalDifference"], gd18 = team18["goalDifference"], gd19 = team19["goalDifference"], gd20 = team20["goalDifference"], id1 = team1["teamID"], id2 = team2["teamID"], id3 = team3["teamID"], id4 = team4["teamID"], id5 = team5["teamID"], id6 = team6["teamID"], id7 = team7["teamID"], id8 = team8["teamID"], id9 = team9["teamID"], id10 = team10["teamID"], id11 = team11["teamID"], id12 = team12["teamID"], id13 = team13["teamID"], id14 = team14["teamID"], id15 = team15["teamID"], id16 = team16["teamID"], id17 = team17["teamID"], id18 = team18["teamID"], id19 = team19["teamID"], id20 = team20["teamID"], nextclub1 = nextclub1, nextclub2 = nextclub2, nextclub3 = nextclub3, nextclub4 = nextclub4, nextclub5 = nextclub5, nextclub6 = nextclub6, nextclub7 = nextclub7, nextclub8 = nextclub8, nextclub9 = nextclub9, nextclub10 = nextclub10, nextclub11 = nextclub11, nextclub12 = nextclub12, nextclub13 = nextclub13, nextclub14 = nextclub14, nextclub15 = nextclub15, nextclub16 = nextclub16, nextclub17 = nextclub17, nextclub18 = nextclub18, nextclub19 = nextclub19, nextclub20 = nextclub20)

    else:
        oneFC = int(request.form.get("clubOne"))
        twoFC = int(request.form.get("clubTwo"))

        # you cannot pick the same team!
        if (oneFC == twoFC):
            flash("please pick two different teams this time! :) ")
            return redirect("/")

        # rest of code is in identical nature to next1(). refer to it's comments if questions arise.
        results = datapack(oneFC, twoFC)
        fixlist = []
        for match in range(len(results)):
            fixlist.append(results[match])
        nameOneFC = reverseClubSearch("id", oneFC, "name")
        nameTwoFC = reverseClubSearch("id", twoFC, "name")
        imgOneFC = reverseClubSearch("id", oneFC, "img")
        imgTwoFC = reverseClubSearch("id", twoFC, "img")
        goals = []
        ft = " "
        homeTeam = " "
        awayTeam = " "
        for matchday in range(len(fixlist)):
            for moment in range(len(fixlist[matchday]['events']['data'])):
                if fixlist[matchday]['events']['data'][moment]['type'] == "goal" or fixlist[matchday]['events']['data'][moment]['type'] == "own-goal" or fixlist[matchday]['events']['data'][moment]['type'] == "penalty":
                    goals.append(fixlist[matchday]['events']['data'][moment])
                    ft = fixlist[matchday]['scores']['ft_score']
                    homeTeam = fixlist[matchday]['localteam_id']
                    awayTeam = fixlist[matchday]['visitorteam_id']
                else:
                    continue

        if (homeTeam == " "):
            clubComparison = compareClubs(oneFC, twoFC, 10)
            wins1 = clubComparison['wins1']
            wins2 = clubComparison['wins2']
            draws = clubComparison['draws']
            goalScorer1 = topGoalscorer(oneFC)
            goalScorer2 = topGoalscorer(twoFC)
            topAssister1 = topAssister(oneFC)
            topAssister2 = topAssister(twoFC)
            injuredPlayers1 = playersUnavailable(oneFC)
            injuredPlayers2 = playersUnavailable(twoFC)
            return render_template("datapack.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)

        goalscorers1 = []
        goalscorers2 = []
        minutes1 = []
        minutes2 = []
        homeFC = reverseClubSearch("id", int(homeTeam), "name")
        awayFC = reverseClubSearch("id", int(awayTeam), "name")
        for goal in range(len(goals)):
            if int(goals[goal]['team_id']) == oneFC:
                goalscorers1.append(goals[goal]['player_name'])
                minutes1.append(goals[goal]['minute'])
            else:
                goalscorers2.append(goals[goal]['player_name'])
                minutes2.append(goals[goal]['minute'])
        clubComparison = compareClubs(oneFC, twoFC, 10)
        wins1 = clubComparison['wins1']
        wins2 = clubComparison['wins2']
        draws = clubComparison['draws']
        goalScorer1 = topGoalscorer(oneFC)
        goalScorer2 = topGoalscorer(twoFC)
        topAssister1 = topAssister(oneFC)
        topAssister2 = topAssister(twoFC)
        injuredPlayers1 = playersUnavailable(oneFC)
        injuredPlayers2 = playersUnavailable(twoFC)
        # print(clubComparison)
        return render_template("datapack.html", goalScorer1 = goalScorer1, goalScorer2 = goalScorer2, dateOne = fixlist[0]['time']['starting_at']['date_time'], dateTwo = fixlist[1]['time']['starting_at']['date_time'], nameOneFC = nameOneFC, nameTwoFC = nameTwoFC, imgOneFC = imgOneFC, imgTwoFC = imgTwoFC, stadeOne = fixlist[0]['venue']['data']['name'], stadeTwo = fixlist[1]['venue']['data']['name'], goalscorers1 = goalscorers1, goalscorers2 = goalscorers2, minutes1 = minutes1, minutes2 = minutes2, ft = ft, homeFC = homeFC, awayFC = awayFC, wins1 = wins1, draws = draws, wins2 = wins2, topAssister1 = topAssister1, topAssister2 = topAssister2, injuredPlayers1 = injuredPlayers1, injuredPlayers2 = injuredPlayers2)
