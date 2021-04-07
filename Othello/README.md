**Othello AI Description**

Othello is a 2-player board game that is played with distinct pieces that are typically black on one side and white on the other side, each side belonging to one player. Our version of the game is played on a chess board of any size, but the typical game is played on an 8x8 board. Players (black and white) take turns placing their pieces on the board.

Placement is dictated by the rules of the game, and can result in the flipping of coloured pieces from white to black or black to white. The rules of the game are explained in detail at https://en.wikipedia.org/wiki/Reversi (Links to an external site.).



**Acknowledgements:**
This project is based on one used in Columbia University’s Artificial Intelligence Course (COMS W4701). Special thanks to Dr. Daniel Bauer, who developed the starter code that we've extended.



**Objective:**
The player’s goal is to have a majority of their coloured pieces showing at the end of the game.

**Game Ending:**
Our version of the game differs from the standard rules described on Wikipedia in one minor point: The game ends as soon as one of the players has no legal moves left.

**Rules:**
The game begins with four pieces placed in a square in the middle of the grid, two white pieces and two black pieces (Figure 1, at left). Black makes the first move.

At each player’s turn, the player may place a piece of their own colour on an unoccupied square, if it “brackets” one or more opponent pieces in a straight line along at least one axis (vertical, horizontal, or diagonal). 



**agent.py**
This contains the game agent.

**othello_gui.py**
This contains a simple graphical user interface (GUI) for Othello.

**othello_game.py**
This contains the game ”manager”. This stores the current game state and communicates with different player AIs.

**othello_shared.py**
This contains functions for computing legal moves, captured disks, and successor game states. These are shared between the game manager, the GUI and the AI players.

**randy_ai.py**
This specifies an ”AI” player (named Randy) that randomly selects a legal move.



**Game State Representation:**
Each game state contains two pieces of information: The current player and the current disks on the board. Throughout our implementation, Player 1 (dark) is represented using the integer 1, and Player 2 (light) is represented using the integer 2.
