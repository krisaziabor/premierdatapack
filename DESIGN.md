# app.py functions

The three sets of 20 variables being defined help build data on both the front and back pages.
- The first set uses a helper function called obtainTeamData. This allows the front page table to accumulate with accurate data based on a team's current rankings in the standings
- The second set allows us to view the accurate club badges on all pages
- The final set produces the accurate club badges of each team's next opponent – please look to the caution statement on README.md for a statement of warning on this feature.

## next1-20() functions

The next twenty functions that are called correspond to each team and their page dedicated to their next matchup. Within each function these data points are called upon:
- The names of both teams
- The time and stadia of both matchups
- The result and goals of the first matchup (if it has occurred)
- A brief synopsis of recent matchups between the sides
- A series of points regarding the form of each side and the performances of their players.
When a badge is clicked, its corresponding HTML page is triggered and the datapack template is rendered with the specific data points.

## welcomehome()

welcomehome delivers data for both the home page and the data pack page (when the form is used). Its methodology is identical to the aforemention next() functions.

# helpers.py functions

## Here is a short overview of every function and its purpose:

- reverseClubSearch retrieves an image, id number, or name of a club when given one of these properties as an input

- compareClubs looks at a maximum of 10 recent Premier League matches between two opponents and determined how many a team has won, lost, and drawn.

- topGoalscorer returns the amount of goals the top goalscorer of a team has scored, as well as their name.

- topAssisters operates in the same manner as topGoalscorer; only assists (the pass before a goal) are now being considered.

- playersUnavailable returns an array of injured players from a certain side.

- datapack is likely the most important one – it finds the two matchups between sides and stores many smaller data points concerning the two matchups

## Tertiary functions

Let us establish that tertiary functions are ones that do not appear on their own in the main code, but help helper functions achieve their greater goal.

Here is a list of the tertiary functions used in the helpers.py code:

- obtainFixtureList returns the full list of fixtures for the current Premier League season

- findCommonYears returns a list of all the seasons that two specific Premier Leagues teams played in at the same time. It also returns every corresponding ID #.

- getPlayerName returns a player's full name when their ID# has been provided.