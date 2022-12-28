# Background

(https://youtu.be/xLNT8eR78qw)

The Premier League is an English football competition that starts every August and ends every May. 20 of the best teams in the country play 38 games each, and the one with the most points at the end of the season is crowned the champion.

Commentators of the Premier League are tasked with not only creating a vibrant atmosphere but also providing deep insights into all aspects of the game. To do this, television networks hire data scientists and analysists who create 50-page-long (sometimes more) data packs, filled to the brim with scenarios and their corressponding stakes in the game. This is how commentators can deliver seemingly random facts at ease; but in truth, the proccess is a tedious one for all parties.

"premier data pack" presents a modern alternative to this issue, and allows any type of users to be in control on the data they consume.

# Configuration and Installation

In order to use the website at all, you must register for an API key, as we will not be able to find our data without it. Follow these directions and you should be good to go!

- Visit (https://www.sportmonks.com/).
- Click on "Try for Free".
- Agree to the Terms of Service and create an account.
- Activate your free trial (credit card unfortunately required) :(
- Go over to "API"
- Press on "Tokens"
- Create a new API token with a name of your choosing.
- !!!! Save onto the key! Sportmonks will not provide it to you once you press the x button.


To access the Sportmonks data, enter this command into your terminal
```bash
cd final-project
export API_KEY=insert_your_key_here
```

Once that is done, run
```bash
flask run
```
to get the website running.

It will take many moments for the website to load, as there are several queries being made in the background.
Once a link appears, press on it, and there you go!

# Usage

There are two ways to produce a data pack:

- Fill out the form on the top
- Press on a club's next opponent by their badge on the far right.

Option one allows you to have more agency over the two teams you choose, while option two is a convenient way to view data for a team's upcoming match. From there, it is all about what you do with it! Have fun!

# Caution

As you will see when using the next club feature, the API updates less frequently than the Premier League and their new schedules. If you need confirmation on accurate upcoming matchups, please visit (https://www.premierleague.com/).
