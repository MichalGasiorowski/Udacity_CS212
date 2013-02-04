# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 pOoints
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

MAX_NUM =20
MULT_DART = {'OFF':0,'S':1,'D':2,'T':3}
DARTS_POSS = []
for i in range(1,MAX_NUM+1):
    DARTS_POSS += ['S' + str(i),'D' + str(i),'T' + str(i)]
DARTS_POSS += ['SB','DB','OFF']

DARTS_POINTS = {}
for dart in DARTS_POSS:
    if dart =='OFF':
        DARTS_POINTS[dart] = 0
    elif dart =='SB':
        DARTS_POINTS[dart] = 25
    elif dart == 'DB':
        DARTS_POINTS[dart] = 50
    else:
        DARTS_POINTS[dart] = MULT_DART[dart[0]]*int(dart[1:])

def get_points_to_darts(dart_points=DARTS_POINTS):
    ret ={}
    for dart,val in dart_points.items():
        if val in ret:
            ret[val] += [dart]
        else:
            ret[val] = [dart]
    return ret

def choose(points,points_darts,double=False):
    if points not in points_darts:
        return None
    if points==0:
        sorted_choices = points_darts[points]
    else:
        sorted_choices = sorted(points_darts[points],key = lambda x: MULT_DART[x[0]])
    if double:
        if points ==0:
            return False
        #print ([i[0] for i in sorted_choices])
        double_dart = [dart for dart in sorted_choices if dart[0] =='D']
        if not double_dart:
            return None
        else:
            return double_dart[0]            
    else:
        return sorted_choices[0]

#print ('DARTS_POINTS:',DARTS_POINTS)
#print ('get_points_to_darts():',get_points_to_darts())
#print ('choose:',choose(12,get_points_to_darts(),False))

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""


def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    # your code here
    ret=[]
    points_darts = get_points_to_darts()
    possible_scores = sorted(points_darts.keys(),reverse=True)
    all_possible_scores = [0] + sorted(points_darts.keys(),reverse=True)
    for dart1 in all_possible_scores:
        if dart1 > total:
            continue
        chosen_dart1 = choose(dart1,points_darts,False)
        for dart2 in all_possible_scores:
            if dart1 + dart2 > total:
                continue
            chosen_dart2 = choose(dart2,points_darts,False)
            for dart3 in possible_scores:
                if dart1 + dart2 + dart3 < total :
                    break
                chosen_dart3 = choose(dart3,points_darts,True)
                if not chosen_dart3:
                    continue
                if dart1 + dart2 + dart3 == total:
                    ret += [ [k for k in [chosen_dart1,chosen_dart2,chosen_dart3] if k !='OFF']]
    if not ret: return None
    #print (sorted(ret,key = lambda x:len(x)))
    return sorted(ret,key = lambda x:len(x))[0]


#print ('double_out(total):',double_out(170))
#print ('double_out(total):',double_out(100))   
"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""

SECTIONS = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
SECTION_NUM = len(SECTIONS)
RING_RATIO_MUL= {'T':(1,( ('S',1 ), ) ),'D':(1, ( ('S',0.5),('OFF',0.5) ) ),
                 'S':(0.2, ( ('D',0.5),('T',0.5) ) ),'SB':(1, ( ('DB', 0.25 ),('S',0.75) ) ),
                 'DB':(3, ( ('SB', 1./3 ),('S',2./3) ) )}

MISS_CLOCKWISE = 0.5


def get_nearby_section(val,sections=SECTIONS):
    i = sections.index(val)
    return [SECTIONS[(i-1)%20],SECTIONS[(i+1) % 20]]

def is_bull(target):
    return target[-1] == 'B'

def get_ex_points(outcomes,darts_points =DARTS_POINTS):
    ret =0
    for out,p in outcomes.items():
        ret+=darts_points[out]*p
    return ret

def ring_outcome(target,miss):
    ret = {}
    #print (target,is_bull(target))
    ring = None
    if is_bull(target):
        ring = target
    else:
        ring = target[0]
        
    ring_muls = RING_RATIO_MUL[ring]
    ret[ring] = 1-miss*ring_muls[0] 
    for r in ring_muls[1]:
        #print (r)
        ret[r[0]] = ring_muls[0] *r[1] *miss
    return ret

def section_outcome(target,miss):
    ret = {}
    
    if is_bull(target):
        section = target[-1]
        ret[section] = 1-miss
        for i in range(1,SECTION_NUM+1):
            ret[str(i)] = miss*1./SECTION_NUM
    else:
        section = target[1:]
        ret[section] = 1-miss
        for nearby in get_nearby_section(int(section)):
            ret[str(nearby)] = miss*MISS_CLOCKWISE
    return ret
    

def outcome(target, miss):
    """Return a probability distribution of [(target, probability)] pairs."""
    #your code here
    ret={}
    if target == 'OFF':
        return {'OFF':1}
    r_outcome = ring_outcome(target,miss)
    s_outcome = section_outcome(target,miss)
    bull = is_bull(target)
    if bull:
        ret['SB'] = r1 = r_outcome['SB'] * s_outcome['B']
        ret['DB'] = r2 = r_outcome['DB'] * s_outcome['B']
        for i in range(1,SECTION_NUM+1):
            ret['S'+str(i)] = (1.-r1-r2)/SECTION_NUM
        return ret
    
    for r_out,r_val in r_outcome.items():
        if r_out =='OFF':
            ret[r_out] = r_val
            continue
        for s_out,s_val in s_outcome.items():
            ret[r_out + s_out] = r_val * s_val


    return ret

def best_target(miss):
    """Return the target that maximizes the expected score."""
    #your code here
    dart_candidates =[(dart,get_ex_points(outcome(dart,miss))) for dart in DARTS_POSS]
    return sorted(dart_candidates,key=lambda x:x[1],reverse=True)[0][0]
        
def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))
#print (best_target(0.0))
test_darts()
test_darts2()
#print (get_nearby_section(5))
#print (ring_outcome('SB',0.2))
#print (ring_outcome('DB',0.2))
#print ('ring_outcome(\'S20\',0.2):',ring_outcome('S20',0.2))
#print ('ring_outcome(\'T20\',0.2):',ring_outcome('T20',0.2))
#print ('ring_outcome(\'D20\',0.2):',ring_outcome('D20',0.2))
#print (section_outcome('SB', .2))
#print (section_outcome('S20', .2))
#print (outcome('S20', .2))
#print ('outcome(\'SB\', .2):',outcome('SB', .2))
