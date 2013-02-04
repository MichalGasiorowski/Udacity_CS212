"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

from functools import update_wrapper
import cProfile

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f


NOT_MOVABLE = ['@','|']

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

@memo
def get_border(N=N,with_goal=True):
    ret = []
    for i in range(N):
        ret += [i,i*N,N*(N-1)+i,N-1 + N*i]
    if with_goal:
        ret.remove(getGoalCoordinate(N))
    return tuple(set(ret))

@memo
def getGoalCoordinate(N):  
   if N%2 == 0:  
      return int(N-1 + (N/2 -1)*N)  
   else:  
      return int(N-1 + (N-1)/2 *N)


def is_goal(state,N=N):
    star_t = [st for st in state if st[0] == '*']
    return getGoalCoordinate(N) in st[1]  

@memo
def is_car_vertical(t,N=N):
    """
    Return True if car is oriented <--- --->
    otherwise returns False
    """
    if len(t) <2:
        return None
    return abs(t[0] - t[1]) ==1


def successors(state):
    """Return a dict of {state:action} pairs describing what can be reached from
    the state and how."""
    ret = {}
    occupied = set()
    move_adder = (1,-1)
    if DEBUG : print (state)
    for car in state :
        if car[0]!='@':
            occupied |= set(car[1])
    if DEBUG : print ('occupied:',occupied)
    for car in state:
        #if DEBUG : print ('  ',car,car[0],not car[0] in NOT_MOVABLE)
        loc_occupied = occupied.copy()
        if not car[0] in NOT_MOVABLE:
            if DEBUG : print ('-----------------\n','    ',car)
            c_loc = car[1]
            loc_occupied -= set(c_loc)
            if DEBUG: print ('occupied:',occupied,'c_loc:',c_loc,'loc_occupied:',loc_occupied)
            if is_car_vertical(c_loc):
                move_adder = (1,-1)
            else:
                move_adder = (N,-N)
            if DEBUG : print ('    ','move_adder:',move_adder)
            for m in move_adder:
                for i in range(1,N):
                    move = (car[0],i*m)
                    if DEBUG : print ('      ','move:',i*m,'c_loc:',c_loc )
                    new_loc = tuple([move[1] + loc for loc in c_loc])
                    if DEBUG: print ('      ','new_loc:',new_loc,'loc_occupied:',loc_occupied,'set(new_loc ):',set(new_loc ))
                    if loc_occupied & set(new_loc ):
                        if DEBUG: print ('        ','cant move more!', 'car:',car,'move:',move)
                        break
                    new_state = tuple([st if st[0] != car[0] else (car[0],new_loc) for st in state])
                    ret[new_state] = move
                    if DEBUG: print ('      ','--ADDED NEW MOVE--:',move)
    if DEBUG: print (list(ret.values()))
    return ret


def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""

    def is_goal(state):
        star_t = [st for st in state if st[0] == '*']
        #print (star_t[0])
        return getGoalCoordinate(N) in star_t[0][1]
                
    return shortest_path_search(start, successors, is_goal)
    
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple([start + i*incr for i in range(n)])

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    only_cars = [ (cars[i][0],cars[i][1]) for i in range(len(cars)) ]
    border = [('|',get_border())]
    goal_st = [('@',(getGoalCoordinate(N),))]
    return tuple(goal_st + only_cars + border)


def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    #print (state)
    board = ['.'] * N**2
    for (c, squares) in state:
        #print (c,squares)
        for s in squares:
            board[s] = c
    #print (board)
    # Now print it out
    for i,s in enumerate(board):
        print (s,end=" ")
        if i % N == N - 1: print()

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))


DEBUG = False

#show(puzzle1)
#print (successors(puzzle1))
#show(puzzle2)
#sshow(puzzle3)

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

puzzle_muzzle = [(('*', (26, 27)), ('G', (9, 10)), ('Y', (14, 22, 30)), ('P', (17, 25, 33)), ('O', (41, 49)), ('B', (20, 28, 36)), ('A', (45, 46)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63))), ('A', -3), (('*', (26, 27)), ('G', (9, 10)), ('Y', (14, 22, 30)), ('P', (17, 25, 33)), ('O', (41, 49)), ('B', (20, 28, 36)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('A', (42, 43))), ('B', 16), (('*', (26, 27)), ('G', (9, 10)), ('Y', (14, 22, 30)), ('P', (17, 25, 33)), ('O', (41, 49)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('A', (42, 43)), ('B', (36, 44, 52))), ('Y', 24), (('*', (26, 27)), ('G', (9, 10)), ('P', (17, 25, 33)), ('O', (41, 49)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('A', (42, 43)), ('B', (36, 44, 52)), ('Y', (38, 46, 54))), ('*', 4), (('G', (9, 10)), ('P', (17, 25, 33)), ('O', (41, 49)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('A', (42, 43)), ('B', (36, 44, 52)), ('Y', (38, 46, 54)), ('*', (30, 31)))]

## puzzle2
puzzle2_set = [(('*', (26, 27)), ('B', (20, 28, 36)), ('P', (33, 34, 35)), ('O', (41, 49)), ('Y', (51, 52, 53)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63))), ('B', -8), (('*', (26, 27)), ('P', (33, 34, 35)), ('O', (41, 49)), ('Y', (51, 52, 53)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (12, 20, 28))), ('P', 1), (('*', (26, 27)), ('O', (41, 49)), ('Y', (51, 52, 53)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (12, 20, 28)), ('P', (34, 35, 36))), ('O', -24), (('*', (26, 27)), ('Y', (51, 52, 53)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (12, 20, 28)), ('P', (34, 35, 36)), ('O', (17, 25))), ('P', -1), (('*', (26, 27)), ('Y', (51, 52, 53)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (12, 20, 28)), ('O', (17, 25)), ('P', (33, 34, 35))), ('Y', -2), (('*', (26, 27)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (12, 20, 28)), ('O', (17, 25)), ('P', (33, 34, 35)), ('Y', (49, 50, 51))), ('B', 24), (('*', (26, 27)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('O', (17, 25)), ('P', (33, 34, 35)), ('Y', (49, 50, 51)), ('B', (36, 44, 52))), ('*', 4), (('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('O', (17, 25)), ('P', (33, 34, 35)), ('Y', (49, 50, 51)), ('B', (36, 44, 52)), ('*', (30, 31)))]
## puzzle3
puzzle3_set = [(('*', (25, 26)), ('B', (19, 27, 35)), ('P', (36, 37, 38)), ('O', (45, 53)), ('Y', (49, 50, 51)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63))), ('B', -8), (('*', (25, 26)), ('P', (36, 37, 38)), ('O', (45, 53)), ('Y', (49, 50, 51)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (11, 19, 27))), ('P', -2), (('*', (25, 26)), ('O', (45, 53)), ('Y', (49, 50, 51)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (11, 19, 27)), ('P', (34, 35, 36))), ('O', -32), (('*', (25, 26)), ('Y', (49, 50, 51)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (11, 19, 27)), ('P', (34, 35, 36)), ('O', (13, 21))), ('P', 2), (('*', (25, 26)), ('Y', (49, 50, 51)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (11, 19, 27)), ('O', (13, 21)), ('P', (36, 37, 38))), ('Y', 3), (('*', (25, 26)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('B', (11, 19, 27)), ('O', (13, 21)), ('P', (36, 37, 38)), ('Y', (52, 53, 54))), ('B', 24), (('*', (25, 26)), ('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('O', (13, 21)), ('P', (36, 37, 38)), ('Y', (52, 53, 54)), ('B', (35, 43, 51))), ('*', 5), (('@', (31,)), ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)), ('O', (13, 21)), ('P', (36, 37, 38)), ('Y', (52, 53, 54)), ('B', (35, 43, 51)), ('*', (30, 31)))]

def test_puzz_set(puzz_set):
    for puzz in puzz_set[0::2]:
        solve_parking_puzzle(puzz)
    return

def test_basic_puzz():
    solve_parking_puzzle(puzzle1)
    solve_parking_puzzle(puzzle2)
    solve_parking_puzzle(puzzle3)

##for puzz in puzzle_muzzle[0::2]:
##    show(puzz)
##    #print (sorted(list(successors(puzz).values())))
##    print (path_actions(solve_parking_puzzle(puzz)))
##
##for puzz in puzzle2_set[0::2]:
##    show(puzz)
##    print (path_actions(solve_parking_puzzle(puzz)))
##
##for puzz in puzzle3_set[0::2]:
##    show(puzz)
##    print (path_actions(solve_parking_puzzle(puzz)))

cProfile.run('test_basic_puzz()')
#cProfile.run('test_puzz_set(puzzle3_set)')

