**Tenner Grid Formal Description**

The game of Tenner Grid (also known as “From 1 to 10”, “Zehnergitter”, or “Grid Ten”) consists of a rectangular grid with dimensions nrows by 10 columns, and a special (n+1)-th row. The task is to fill in the first nrows so that every row contains the digits 0 through 9. In columns, the numbers may be repeated.
The (n+1)-th row contains numbers which give the sum of the numbers in their respective columns. The numbers in the (n+1)-th row are always given in the start state.
The digits in adjacent cells (even cells that are diagonally adjacent) must be different. For example, cell(0,0) is adjacent to cell(0,1), cell(1,0) and cell(1,1).
The start state of the puzzle has some spaces already filled in.
A puzzle is solved if all empty cells are filled in with an integer from 0 to 9 and all above constraints are satisfied.

**propagators.py**
This contains implementation of two propagators: propFC and propGAC, to realize Forward Checking and GAC, respectively. 
An MRV heuristic also added for selecting variables to be assigned.

**tenner_csp.py**
This contains two Tenner Grid CSP models.

**cspbase.py**
This contains class definitions for the python objects Constraint, Variable, and BT.
