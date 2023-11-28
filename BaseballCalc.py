#!/usr/bin/env python3

import os
import math
import time
from statistics import NormalDist

## These stats are based off the last 5 years of playoffs
## MLB changed the playoff format in 2022, but I chose to include 2018 to now
## to create a larger sample size and I retroactively added teams to the playoffs.
## Also ignored the 2020 season which was shortened due to covid
avg_wins_of_playoff_team = 94.82
stdev_of_wins_of_playoff_team = 6.76

### Takes a teams runs scored and their runs allowed and calculates what their
### win percentage should be based off Bill James pythagorean win percentage
def __pythag_wins(runs_scored, runs_allowed) -> float:
    return 1 / (1 + (runs_allowed / runs_scored)**2)

### Takes two percentages and returns the probability that A beats B
def __head_to_head_percent(A_percent, percent_B):
    numerator = A_percent - A_percent * percent_B
    denominator = A_percent + percent_B - 2 * A_percent * percent_B
    return  numerator / denominator

### Takes two teams win totals and returns the probability that A beats B
def __head_to_head_wins_losses(A_wins, B_wins):
    A_losses = 162 - A_wins
    B_losses = 162 - B_wins

    return (A_wins * B_losses) / (A_wins * B_losses + B_wins * A_losses)

### Takes two teams win totals and a series length and figures out the odds that team A wins the series
### Calculates prob that team A beats team B 
### Then determines if a team would win the majority of a 7 game series
def __prob_to_win_series(A_wins, B_wins, series_length):
    wins_needed = series_length // 2 + 1
    A_wins_game = __head_to_head_wins_losses(A_wins, B_wins)
    A_wins_series = 0

    for i in range(wins_needed, series_length + 1):
        A_wins_series += (A_wins_game ** i) * (1-A_wins_game) ** (series_length - i) * math.comb(series_length, i)
    return A_wins_series

### Takes two teams and returns which team wins the series
def __run_series(runs, teams, A, B, series_length) -> int:
    A_wins = __pythag_wins(runs[A][0], runs[A][1])
    B_wins = __pythag_wins(runs[B][0], runs[B][1])
    A_beats_B = round(__prob_to_win_series(A_wins, B_wins, series_length)*100, 1)
    time.sleep(1)
    if (A_beats_B >= 50): 
        print("The " + teams[A] + " have a " + str(A_beats_B) + "% chance of beating the " + teams[B] + ".")
        return A
    else:
        print("The " + teams[B] + " have a " + str(100 - A_beats_B) + "% chance of beating the " + teams[A] + ".")
        return B

### Asks a player for either wins/losses or runs scored/allowed and determines if the team should make the playoffs
def make_playoffs() -> None:
    print("Would you rather: \
            \n\t1. Determine if your team will make it based off its current \
            \twin percentage \
            \n\t2. Determine if your team will make it based off its current \
            \truns for and runs allowed (removes luck from the equation)")
    inp = input("Enter input: ")
    inp_loop = False
    while(not(inp_loop)):
        if inp == "1":
            inp_loop = True
            wins = int(input("Enter current wins: "))
            losses = int(input("Enter current losses: "))
            percent = wins / (wins+losses)
        elif inp == "2":
            inp_loop = True
            runs_scored = int(input("Enter current runs scored: "))
            runs_allowed = int(input("Enter current runs allowed: "))
            percent = __pythag_wins(runs_scored, runs_allowed)
        else:
            print("Try again.")
            inp = input("Enter input: ")
        
    fullSeasonWins = math.floor(percent * 162)
    Z = NormalDist(mu=avg_wins_of_playoff_team, sigma=stdev_of_wins_of_playoff_team).zscore(fullSeasonWins)
    percent_more = math.floor(100 * (1 - NormalDist().cdf(Z)))
    print(str(percent_more) + "% of playoff teams would have a better record than this.")
    if (fullSeasonWins > avg_wins_of_playoff_team):
        print("So, your team definitely makes the playoffs")
    elif (fullSeasonWins > avg_wins_of_playoff_team - stdev_of_wins_of_playoff_team):
        print("So, your team probably makes the playoffs")
    elif (fullSeasonWins > avg_wins_of_playoff_team - stdev_of_wins_of_playoff_team * 2):
        print("So, your team has a slight chance to make the playoffs")
    else:
        print("So, your team will not make the playoffs")

## Asks for how many runs team has scored and allowed and asks for actual win percent
## Outputs projected number of games team is going to win more than they should
def lucky() -> None:
    pass

## Asks user for teams current win percentage and competitors current win percentage
#  Determines who will win 
def who_wins() -> None:
    pass

## Asks user for batter's batting average and pitcher's batting average against and determines who would win
def pitch_v_hitter() -> None:
    pass

## Asks user for teams in playoffs and their run totals and determines who would win the whole thing
def playoff_predictor() -> None:
    inp_help = ["first", "second", "third", "fourth", "fifth", "sixth"]
    
    american = list()
    american_runs = list(list())
    national = list()
    national_runs = list(list())

    for i in inp_help:
        name = input("Enter name of " + i + " place American League team: ")
        runs_for = int(input("Enter runs scored by the " + name + ": "))
        runs_against = int(input("Enter runs scored against the " + name + ": "))
        american.append(name)
        american_runs.append([runs_for, runs_against])
    for i in inp_help:
        name = input("Enter name of " + i + " place National League team: ")
        runs_for = int(input("Enter runs scored by the " + name + ": "))
        runs_against = int(input("Enter runs scored against the " + name + ": "))
        national.append(name)
        national_runs.append([runs_for, runs_against])
    print("\n\n------------------------Playoff Simulation Based off Wins------------------------\n")
    print("\n---------------------------------Wild Card Games---------------------------------\n")
    # who wins American Leauge wild card games
    face_two_seed_a = __run_series(american_runs, american, 2, 5, 3)
    face_one_seed_a = __run_series(american_runs, american, 3, 4, 3)
    # who wins National League wild card games
    face_two_seed_n = __run_series(national_runs, national, 2, 5, 3)
    face_one_seed_n = __run_series(national_runs, national, 3, 4, 3)

    time.sleep(2)
    print("\n--------------------------------------ALDS---------------------------------------\n")
    # who wins ALDSs
    alcs_team_one = __run_series(american_runs, american, 1, face_two_seed_a, 5)
    alcs_team_two = __run_series(american_runs, american, 0, face_one_seed_a, 5)
    time.sleep(2)
    print("\n--------------------------------------NLDS---------------------------------------\n")
    # who wins NLDSs
    nlcs_team_one = __run_series(national_runs, national, 1, face_two_seed_n, 5)
    nlcs_team_two = __run_series(national_runs, national, 0, face_one_seed_n, 5)

    time.sleep(2)
    print("\n--------------------------------------ALCS---------------------------------------\n")
    # who wins ALCS
    american_ws_team = __run_series(american_runs, american, alcs_team_one, alcs_team_two, 7)
    time.sleep(2)
    print("\n--------------------------------------NLCS---------------------------------------\n")
    # who wins NLCS
    national_ws_team = __run_series(national_runs, national, nlcs_team_one, nlcs_team_two, 7)
    
    time.sleep(2)
    print("\n----------------------------------World Series-----------------------------------\n")
    # who wins World Series
    nl_wins = __pythag_wins(national_runs[national_ws_team][0], national_runs[national_ws_team][1])
    al_wins = __pythag_wins(american_runs[american_ws_team][0], american_runs[american_ws_team][1])
    A_beats_B = round(__prob_to_win_series(nl_wins, al_wins, 7)*100, 1)
    time.sleep(3)
    if (A_beats_B > .5):
        print("The " + national[national_ws_team] + " have a " + str(A_beats_B) + "% chance of beating the " + american[american_ws_team] + ", so they win the World Series!")
    else:
        print("The " + american[american_ws_team] + " have a " + str(100 - A_beats_B) + "% chance of beating the " + national[national_ws_team] + ", so they win the World Series!")
    

def help():
    print("\nCommands:")
    for comVals in command_blueprints:
        cb_val = command_blueprints[comVals]
        ### format function name to spaced title format
        print(f" {cb_val[-1]:>2}) ", end="")
        for counted, comOpt in enumerate(cb_val[:-1]):
            if counted != 0: print(end=' '*(6+len(comVals.__name__)))
            print(f"{comOpt}")
        if len(cb_val)==0: print()
    print(" Quit: - \"quit\" (or leave empty)")

command_blueprints = {
    help : ["Help", "0"],
    make_playoffs : ["Should my team make the playoffs?","1"],
    lucky : ["Is my team lucky?","2"],
    who_wins : ["Is my team going to win this game?","3"],
    pitch_v_hitter : ["Who wins between a pitcher and batter?","4"],
    playoff_predictor : ["Playoff Predictor","6"],
}
commands = {}

def setup_commands():
    for func in command_blueprints:
        for text_option in command_blueprints[func]:
            commands[text_option] = func
    return True

def main(clear_screen=setup_commands()) -> None:
    if clear_screen: os.system("clear")
    print("Baseball Calculator will answer a few of your baseball questions.\
    \nTake a look at the commands and choose some.")
    help()
    quit = False
    while (not quit):
        command = input("Enter a command: ")
        if command.lower() in ["quit",""]: quit = True
        elif command not in commands: print("Try again.")
        else: commands[command]()
    return print("Goodbye!")

if __name__ == '__main__':
    main()