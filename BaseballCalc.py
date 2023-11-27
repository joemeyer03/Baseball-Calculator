#!/usr/bin/env python3

import os
import math
from statistics import NormalDist

avg_wins_of_playoff_team = 94.82
stdev_of_wins_of_playoff_team = 6.76

def pythag_wins(runs_scored, runs_allowed) -> float:
    return 1 / (1 + (runs_allowed / runs_scored)**2)

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
            percent = pythag_wins(runs_scored, runs_allowed)
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

def runs_playoffs() -> None:
    pass

def lucky() -> None:
    pass

def playoff_predictor() -> None:
    pass

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
    runs_playoffs : ["How many runs does my team need to make the playoffs?","2"],
    lucky : ["Is my team lucky?","3"],
    playoff_predictor : ["Playoff Predictor","4"],
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