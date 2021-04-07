# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the warehouse domain.

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools


def set_up(initial_tenner_board):
    '''Helper for setting up the board for tenner_csp_model_1
       and tenner_csp_model_2
    '''
    board = [[] for k in range(len(initial_tenner_board[0]))]
    for i in range(len(initial_tenner_board[0])):
        row = []
        for j in range(0, 10):
            num = initial_tenner_board[0][i][j]
            if num == -1:  # spaces not filled
                row.append(Variable("V[{}][{}]".format(i, j), [k for k in range(0, 10)]))
            else:  # spaces already filled in
                row.append(Variable("V[{}][{}]".format(i, j), [num]))
        board[i] = row
    return board


def column_sum_constraint(board, initial_tenner_board, cons):
    '''Set sum constraints for columns in Model 1 and 2
    '''
    num_rows = len(initial_tenner_board[0])
    for col in range(0, 10):
        col_var = []
        for row in range(0, num_rows):
            col_var.append(board[row][col])
        col_con = Constraint("Column{}".format(col), col_var)
        # Add all tuples that sum towards the required value
        sat_tups = []
        domains = [variable.domain() for variable in col_var]
        for dom_tup in itertools.product(*domains):
            if sum(dom_tup) == initial_tenner_board[1][col]:
                sat_tups.append(dom_tup)
        col_con.add_satisfying_tuples(sat_tups)
        cons.append(col_con)


# def row_sum_constraint(board, initial_tenner_board, cons):
#     '''Set Sum constraints for rows in Model 2
#     '''
#     num_rows = len(initial_tenner_board[0])
#     for row in range(0, num_rows):
#         row_var = []
#         for col in range(0, 10):
#             row_var.append(board[row][col])
#         row_con = Constraint("Row{}".format(row), row_var)
#         sat_tups = []
#         domains = [var.domain() for var in row_var]
#         for dom_tup in itertools.product(*domains):
#             # must consist of unique ordering of 10 numbers {0, ..., 9}
#             # so the sum must be 45
#             if sum(dom_tup) == 45:
#                 counts = dict()
#                 for i in dom_tup:
#                     if counts.get(i, 0) > 0:
#                         break
#                     counts[i] = counts.get(i, 0) + 1
#             else:
#                 sat_tups.append(dom_tup)
#         row_con.add_satisfying_tuples(sat_tups)
#         cons.append(row_con)


def adjacent_constraints(process, board, initial_tenner_board, a, b, cons):
    '''Set constraints to make sure all variables on the board (except
       numbers on the last row or column) are different from the element
       at the right/bottom/bottom right
    '''
    num_rows = len(initial_tenner_board[0])
    if process:
        for (x, y) in process:
            row = a + x
            col = b + y
            if (row >= 0 and row <= num_rows - 1) and (col >= 0 and col <= 9):
                var1 = board[a][b]  # the variable itself
                var2 = board[row][col]  # adjacent variable of the variable
                cur_con = Constraint("C(A[{}][{}])(A[{}][{}]".format(row, col, a, b), [var1, var2])
                # Add all tuples of which the two variables are different
                sat_tups = []
                for dom_tup in itertools.product(var1.domain(), var2.domain()):
                    if dom_tup[0] != dom_tup[1]:
                        sat_tups.append(dom_tup)
                cur_con.add_satisfying_tuples(sat_tups)
                cons.append(cur_con)


def row_constraints_1(board, initial_tenner_board, cons):
    '''Set constraint for row such that no two variable are the same (binary)
    '''
    num_rows = len(initial_tenner_board[0])
    for i in range(0, num_rows):
        for j in range(0, 10):
            for k in range(j + 1, 10):
                cur_con = Constraint("C(Q{},Q{})".format(i, j), [board[i][j], board[i][k]])
                sat_tups = []
                for dom_tup in itertools.product(board[i][j].cur_domain(), board[i][k].cur_domain()):
                    if dom_tup[0] != dom_tup[1]:
                        sat_tups.append(dom_tup)
                cur_con.add_satisfying_tuples(sat_tups)
                cons.append(cur_con)


def row_constraints_2(board, initial_tenner_board, cons):
    '''Set constraint for row such that no two variable are the same (n-anry)
    '''
    num_rows = len(initial_tenner_board[0])
    for i in range(0, num_rows):
        dom = [k for k in range(10)]
        var_scope = []
        sat_tups = []
        for j in range(10):
            if initial_tenner_board[0][i][j] != -1:
                dom.remove(initial_tenner_board[0][i][j])  # make the domain smaller
            else:
                var_scope.append(board[i][j])
        cur_con = Constraint("C{}".format(i), var_scope)
        for perm in itertools.permutations(dom):
            sat_tups.append(perm)
        cur_con.add_satisfying_tuples(sat_tups)
        cons.append(cur_con)


def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 7.


       The input board is specified as a pair (n_grid, last_row).
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid.
       If a -1 is in the list it represents an empty cell.
       Otherwise if a number between 0--9 is in the list then this represents a
       pre-set board position. E.g., the board

       ---------------------
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists

       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]


       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.

       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each
       column.
    '''
    # IMPLEMENT
    # set up the board
    board = set_up(initial_tenner_board)
    num_rows = len(initial_tenner_board[0])
    cons = []

    column_sum_constraint(board, initial_tenner_board, cons)

    for row in range(0, num_rows):
        for col in range(0, 10):
            if row == num_rows - 1 and col == 9:
                process = []
            elif row != num_rows - 1 and col == 9:
                process = [(1, 0)]
            elif row == num_rows - 1 and col != 9:
                process = [(0, 1)]
            else:
                process = [(0, 1), (1, 0), (1, 1)]
            adjacent_constraints(process, board, initial_tenner_board, row, col, cons)

    row_constraints_1(board, initial_tenner_board, cons)

    # build CSP Model
    vars = []
    for row in board:
        for var in row:
            vars.append(var)
    tenner_csp_model_1 = CSP("tenner_csp_model_1", vars)

    # add all constraint we made
    for con in cons:
        tenner_csp_model_1.add_constraint(con)

    return tenner_csp_model_1, board


##############################


def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.

       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary
       contstraints to encode contiguous cells (including diagonally contiguous
       cells), however. Each -ary constraint is over more
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''
    # IMPLEMENT
    # set up the board
    board = set_up(initial_tenner_board)
    num_rows = len(initial_tenner_board[0])
    cons = []

    column_sum_constraint(board, initial_tenner_board, cons)

    for row in range(0, num_rows):
        for col in range(0, 10):
            if row == num_rows - 1 and col == 9:
                process = []
            elif row != num_rows - 1 and col == 9:
                process = [(1, 0)]
            elif row == num_rows - 1 and col != 9:
                process = [(0, 1)]
            else:
                process = [(0, 1), (1, 0), (1, 1)]
            adjacent_constraints(process, board, initial_tenner_board, row, col, cons)

    row_constraints_2(board, initial_tenner_board, cons)

    for row in range(0, num_rows):
        for col in range(0, 10):
            if row == num_rows - 1 and col == 9:
                process = []
            elif row != num_rows - 1 and col == 9:
                process = [(1, 0)]
            elif row == num_rows - 1 and col != 9:
                process = [(0, 1)]
            else:
                process = [(0, 1), (1, 0), (1, 1)]
            adjacent_constraints(process, board, initial_tenner_board, row, col, cons)

    # build CSP Model
    vars = []
    for row in board:
        for var in row:
            vars.append(var)
    tenner_csp_model_2 = CSP("tenner_csp_model_2", vars)

    # add all constraint we made
    for con in cons:
        tenner_csp_model_2.add_constraint(con)

    return tenner_csp_model_2, board
