# Baseball-Calculator
Attempts to calculate certain baseball questions using statistics. Answers these questions so far:

## Should my team make the playoffs?
- Asks the user to choose between entering wins/losses or runs scored/allowed and determines if the team should make the playoffs.
- If the user opts to use runs, the program will calculate the expected wins using the [pythagorean expectation formula](https://en.wikipedia.org/wiki/Pythagorean_expectation).
- I determine if a team makes the playoffs by determining how far away the win total is from the mean wins a playoff team usually has.
- I determined that the average wins of a playoff team is 94.82 and the standard deviation is 6.76 
    - MLB changed the playoff format in 2022 to include more teams, but I chose to include back to 2018, I retroactively added teams to the playoffs, to create a larger sample size.
    - I also ignored the 2020 season which was shortened due to covid

## Is my team lucky?
- Not currently implemented
- Will ask for how many runs team has scored and allowed and ask for actual win percent
- Outputs projected number of games team is going to win more than they should
- Also uses pythagorean expectation

## Is my team going to win this game?
- Not currently implemented
- Will ask user for teams current win percentage and competitors current win percentage
- Determines who will win using Bill James's [Log5](https://en.wikipedia.org/wiki/Log5) formula

## Who wins between a pitcher and batter?
- Not currently implemented
- Will ask user for batter's batting average and pitcher's batting average against and determines who would win
- Also uses Log5

## Who would win the World Series?
- Asks user for teams in playoffs and their run totals and determines who would win the whole thing
- Uses pythagorean expectation to determine how many teams a team should have actually got based off their run totals
- Using those wins, program determines who would win a series of 3, 5, or 7 games
    - First, program determines the probability that a team wins one game using the Log5 formula, will call that P(A)
    - Then, uses this equation to determine probability that a team wins majority of the games in a series (this equation is for a seven game series, where one team needs to win 4 games):
```math
\sum_{n=4}^7 P(A) ^ n \cdot (1-P(A))^{7-n} \cdot {7 \choose n}
```
- There is a file called "2023playoffs.txt", which has the proper inputs for the 2023 MLB playoffs, if you'd like to see the prediction and probabilities