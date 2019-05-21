# 2048 Solver

### As an extension to this project I am going to develop some JS to add a visual level to the solution.

## First solution to tackling the 2048 tile game. 

The solution is implementing an expectimax algorithm with a few general heuristics. 
The expectimax algorihtm is a variation of the adversarial minimax algorithm, where the adversarial (opponent) nodes are changed with "random" nodes as there is no real opponent.

### Random Details.
+ There arer a couple heursitcs that I have tried with similar levels of success. 
  + One is simply just taking the highest valued piece on the board. -> *Worked well*
  + Another is taking the denisity of the board (the summed value of the occupied pieces divided by the number of occupied pieces.) -> *Worked Well*
  + Another tactic I tried with very limited success was trying to leverage the certain positions and scenarios on the board. -> *Did not work very well, hit and miss*
    -   The reason I believe it did not work is that the scenarios and positions I was trying to achieve were to specific and therefore the AI put precedence on achieving these board states I wanted instead of just getting the highest valued tile and then missing other opportunities that would have lead to better states.
    -   On an interesting note, by watching the AI play with different heuristics it developed its own style of playing and would have particular game states that came up often for each heuristic.

### 2048 Tile Solver Game:
+ The game is a 4x4 matrix.
+ In unoccupied tiles each at the beginning of each turn a 2 or 4 values tile will generate randomly.
+ The aim is to generate te highsest score sliding the board up/down or left/right to combine tiles (tiles values must match to be combined, the combination value is the sum of the two tiles.)
+ The game ends when their are no more available tiles to place a new 2 or 4 valued tile.