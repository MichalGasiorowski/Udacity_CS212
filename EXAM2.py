"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
"""
Features:
person_name, day_of_week,occupation, bought 
"""

import itertools

days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
gadgets = ["laptop","droid","tablet","iphone","YYY"]
jobs = ["programmer","writer","manager","designer","XXX"]
guys = ["Hamming","Knuth","Minsky","Simon","Wilkes"]


def get_text_order(order,only_guys):
    ret = []
    guys_ret =[]
    for i_day in range(len(days)):
        guy = guys[order[0].index(i_day)]
        gadget = gadgets[order[1].index(i_day)]
        job = jobs[order[2].index(i_day)]
        ret.append(days[i_day] + ":%s;%s;%s" % (guy,gadget,job))
        guys_ret.append(guy)
    if only_guys:
        return guys_ret
    return ret

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    days = Monday, Tuesday,Wednesday,Thursday,Friday = list(range(5))
    orderings = list(itertools.permutations(days))
    
    ll= list(((Hamming,Knuth,Minsky,Simon,Wilkes),(laptop,droid,tablet,iphone,YYY),(programmer,writer,manager,designer,XXX))
                     for (laptop,droid,tablet,iphone,YYY) in orderings
                     if (not tablet is Friday) 
                     and (laptop is Wednesday) 
                     and (Tuesday in (iphone,tablet))
                     for (programmer,writer,manager,designer,XXX) in orderings
                     if (not designer is Thursday) 
                     and (not designer is droid )
                     for (Hamming,Knuth,Minsky,Simon,Wilkes) in orderings
                     if (Knuth is Simon + 1)  
                     and (not programmer is Wilkes) 
                     and (not writer is Minsky) 
                     and (Knuth is manager +1) 
                     and (((programmer,droid) == (Wilkes,Hamming)) or ((programmer,droid) == (Hamming,Wilkes)) )
                     and (not manager in (Knuth,tablet)) 
                     and ((laptop,Wilkes) == (Monday,writer) or (laptop,Wilkes) == (writer,Monday)) 
                     )
    
    return get_text_order(ll[0],True)

print logic_puzzle()
