#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    total_dis = 0
    for snowball in state.snowballs:
        distance = abs(snowball[0] - state.destination[0]) + abs(snowball[1] - state.destination[1])
        size = state.snowballs[snowball]
        if (size == 0 or size == 1 or size == 2):
            total_dis += distance
        elif (size == 3 or size == 4 or size == 5):
            total_dis += 2 * distance
        else:
            total_dis += 3 * distance
    return total_dis


#HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible snowball heuristic'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    return len(state.snowballs)

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    total_dis = 0
    for snowball in state.snowballs:
        # snowball at destination.
        if snowball == state.destination:
            total_dis += 0
        # snowball not at destination, check if it is in deadlock.
        else:
            if edge_check(snowball, state.destination, state.width, state.height):
                return float('inf')
            if obstacle_check(snowball, state.obstacles):
                return float('inf')
        distance = abs(snowball[0] - state.destination[0]) + abs(snowball[1] - state.destination[1])
        size = state.snowballs[snowball]
        if (size == 0 or size == 1 or size == 2):
            total_dis += distance
        elif (size == 3 or size == 4 or size == 5):
            total_dis += 2 * distance
        else:
            total_dis += 3 * distance
    total_dis += robot_to_target(state)
    return total_dis


def edge_check(snowball, destination, width, height):
    '''Checks if a snowball is on an edge of the board.'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: true if a snowball is on an edge of the board where the goal is not, false otherwise'''

    # Checking if destination is on the edge of the board
    left_edge = destination[0] == 0
    right_edge = destination[0] == width - 1
    top_edge = destination[1] == 0
    bottom_edge = destination[1] == height - 1

    # Checking if snowball is on an edge, while destination is not on the same edge.
    if not left_edge and snowball[0] == 0:
        return True
    elif not right_edge and snowball[0] == width-1:
        return True
    elif not top_edge and snowball[1] == 0:
        return True
    elif not bottom_edge and snowball[1] == height-1:
        return True
    else:
        return False


def obstacle_check(snowball, obstacles):
    ''' Checks if a snowball not on edge is stuck by obstacles.'''
    '''A snowball is stuck by obstacles if it's there are more than 2 obstacles on its top/left/right/bottom'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: true if a snowball is stuck, false otherwise'''
    # Get the coordinates of the adjacent coordinates and check if the snowball is stuck
    left = (snowball[0] - 1, snowball[1])
    right = (snowball[0] + 1, snowball[1])
    top = (snowball[0], snowball[1] - 1)
    bottom = (snowball[0], snowball[1] + 1)
    if top in obstacles and left in obstacles:
        return True
    elif top in obstacles and right in obstacles:
        return True
    elif bottom in obstacles and left in obstacles:
        return True
    elif bottom in obstacles and right in obstacles:
        return True
    else:
        return False

def robot_to_target(state):
    ''' Calculates the manhattan distance of the robot to the nearest target not on goal '''
    ''' The target priority is this: b, A, B, G, m, C, s'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a number representing the manhattan distance of the robot to the nearest target not on goal'''
    # self.snowball_sizes = {0: 'b', 1: 'm', 2: 's', 3: 'A', 4: 'B', 5: 'C', 6: 'G'}
    # snowball sizes: 'b' is 'big', 'm' is 'medium' and 's' is small.
    # A type 'G' snowman is a complete snowman.
    # A type 'A' snowman is formed by placing a medium snowball atop big one.
    # A type 'B' snowman is formed by placing a small snowball atop medium one.
    # A type 'C' snowman is formed by placing a small snowball atop big one.

    # this is a list of possible combos of the snowball size
    possibilities = {0: [0, 1, 2], 1: [0, 4], 2: [1, 5], 3: [2, 3], 4: [6]}
    # use a flag to indicate which combo this state belongs to
    flag = [True, True, True, True, True]
    # we store the combo of this state in dictionary combo
    # key: snowball size, value: snowball position
    combo = {}
    # indicate whether all snowballs are not in the destination
    none_at_destination = True
    for snowball in state.snowballs:
        combo[state.snowballs[snowball]] = snowball
        if state.destination == snowball:
            none_at_destination = False
        for i in range(0, 5):
            if state.snowballs[snowball] not in possibilities[i]:
                flag[i] = False
    if none_at_destination:
        if flag[0] or flag[1]:
            return abs(state.robot[0] - combo[0][0]) + abs(state.robot[1] - combo[0][1])
        elif flag[2]:
            return abs(state.robot[0] - combo[5][0]) + abs(state.robot[1] - combo[5][1])
        elif flag[3]:
            return abs(state.robot[0] - combo[3][0]) + abs(state.robot[1] - combo[3][1])
        else:
            return abs(state.robot[0] - combo[6][0]) + abs(state.robot[1] - combo[6][1])
    else:
        priority = [0, 3, 4, 5, 1, 2, 6]
        i = 0
        while i < 6:
            for snowball in state.snowballs:
                if state.snowballs[snowball] == priority[i] and snowball != state.destination:
                    return abs(state.robot[0] - snowball[0]) + abs(state.robot[1] - snowball[1])
            i += 1
        return 0


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 5):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    result = False

    se = SearchEngine('custom', 'full')

    # introduce costbound for node pruning.
    costbound = (float("inf"), float("inf"), float("inf"))

    # keep searching within the timebound, save 0.01 second for safety.
    while timebound > 0:
        start_time = os.times()[4]

        fval_fn = (lambda sN: fval_function(sN, weight))
        se.init_search(initial_state, snowman_goal_state, heur_fn, fval_fn)
        curr = se.search(timebound, costbound)

        # decrease weight and keep it below 1 to get optimal solution.
        weight = max(1, weight * 0.8)

        # result not found
        if not curr:
            return result

        # node pruning based on (g value + h value).
        if curr.gval + heur_fn(curr) <= costbound[2]:
            costbound = (float("inf"), float("inf"), curr.gval + heur_fn(curr))
            result = curr

        # timebound for next iteration.
        timebound -= os.times()[4] - start_time
    return result


def anytime_gbfs(initial_state, heur_fn, timebound = 5):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    result = False

    # introduce costbound for node pruning.
    costbound = (float("inf"), float("inf"), float("inf"))

    # initialize search engine.
    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, snowman_goal_state, heur_fn)

    # keep searching within the timebound, save 0.01 second for safety.
    while timebound > 0.01:
        start_time = os.times()[4]

        curr = se.search(timebound, costbound)

        # result not found
        if not curr:
            return result

        # node pruning based on g value.
        if curr.gval <= costbound[0]:
            costbound = (curr.gval, float("inf"), float("inf"))
            result = curr

        # timebound for next iteration.
        timebound -= os.times()[4] - start_time

    return result
