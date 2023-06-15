from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False
    X = state.get_current_variable()
    if X == None:
        return True

    x = X.get_assigned_value() 
     
    Xconstraints = state.get_constraints_by_name(X.get_name())
    for constraint in Xconstraints:
        Y_name = constraint.get_variable_j_name()
        Y = state.get_variable_by_name(Y_name)
        if Y.is_assigned():
            if constraint.check(state, X.get_assigned_value(), Y.get_assigned_value()) == True:
                continue
        for y in Y.get_domain():
            if constraint.check(state, X.get_assigned_value(), y) == False:
                Y.reduce_domain(y)
            
        if Y.domain_size() == 0:
            return False
    return True  
    
    # raise NotImplementedError

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    from collections import deque
    # raise NotImplementedError
    q = deque()
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False
        
    variables = state.get_all_variables()
    
    for variable in variables:
        if len(variable.get_domain()) == 1:
            q.append(variable.get_name())
    
    visited = []
    while len(q) != 0:
        X_name = q.popleft()
        visited.append(X_name)
        X = state.get_variable_by_name(X_name)
        Xconstraints = state.get_constraints_by_name(X.get_name())
        
        for constraint in Xconstraints:
            Y_name = constraint.get_variable_j_name()
            Y = state.get_variable_by_name(Y_name)
            for y in Y.get_domain():
                
                if constraint.check(state, X.get_domain()[0], y) == False:
                    Y.reduce_domain(y)
                if len(Y.get_domain()) == 0:
                    return False
        
        for variable in state.get_all_variables():
            if len(variable.get_domain()) == 1 and variable.get_name() not in q and variable.get_name() not in visited:
                q.append(variable.get_name())  
    
    return True

    
    
    
    

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
# print(f"senate_people : {senate_people[0]}")
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
# evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    if len(list1) !=  len(list2):
        return 0
    
    distance = 0 
    for i in range(len(list1)):
        distance += (list1[i] - list2[i])**2
    
    import math
    distance = math.sqrt(distance)
    return distance  

    return hamming_distance(list1, list2)

#Once you have implemented euclidean_distance, you can check the results:
# evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(hamming_distance, 1)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
# print(CongressIDTree(senate_people, senate_votes, homogeneous_disorder))

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    # assuming the first element from yes to be a +ve and and other element in no to be a -ve
    positive = yes[0]
    negative = ""
    for nos in no:
        if nos != positive:
            negative = nos
    # if arrays have same the same type that means yes and no lists are homogenious
    if negative == "":
        return 0
    
    # calculating the average disorder for yes and nos seperately and suming themby the formula
    # number of samples in yes or no branch/total samples * disorder of yes branch based on predetermined positives
    # and negatives
    
    Yes = []
    No = []
    for element in yes:
        if element == positive:
            Yes.append(element)
        else:
            No.append(element)
    
    sum = 0
    sum += len(yes)/(len(yes) + len(no)) * getDisorder(Yes, No)

    Yes = []
    No = []
    for element in no:
        if element == positive:
            Yes.append(element)
        else:
            No.append(element)

    sum += len(no)/(len(yes) + len(no)) * getDisorder(Yes, No)
    return sum

    return homogeneous_disorder(yes, no)

# considering yes to be positive and no to be negative getting the disorder based on 
# formula -P/T log2(P/T) - N/T log2(N/T)
def getDisorder(yes, no):
    import math
    yes_count = len(yes)
    no_count = len(no)
    total_count = yes_count + no_count

    if yes_count == 0 or no_count == 0:
        return 0

    yes_ratio = yes_count / total_count
    no_ratio = no_count / total_count

    disorder = -(yes_ratio * math.log2(yes_ratio) + no_ratio * math.log2(no_ratio))
    return disorder

# print (CongressIDTree(senate_people, senate_votes, information_disorder))
# print (CongressIDTree(house_people, house_votes, information_disorder))
# evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print ("ID tree for first group:")
        print (CongressIDTree(house_limited_group1, house_limited_votes,information_disorder))
        print(" ")
        print (f"ID tree for second group:")
        print (CongressIDTree(house_limited_group2, house_limited_votes, information_disorder))
        print()
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 826
# i = 1
# while True:
#     rep_classified = limited_house_classifier(house_people, house_votes, i)
#     print(f"i : {i} rep_classified : {rep_classified}")
#     if  rep_classified >= 430:
#         N_1 = i
#         print(f"N_1 should be : {N_1}")
#         break
#     i += 1

rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
# N_2 = 120
N_2 = 106
i = 1
# while True:
#     senator_classified = limited_house_classifier(senate_people, senate_votes, i)
#     # print(f"i : {i} limited_house_classifier(house_people, house_votes, i) : {senator_classified}")

#     if  senator_classified >= 90:
#         N_2 = i
#         print(f"N_2 should be {i}")
#         break
#     i += 1

senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
print(f"senator_classified : {senator_classified}")
## Now, find a value of n that classifies at least 95 of last year's senators correctly.
# N_3 = 130
N_3 = 111
# i = 1
# while True:
#     old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, i)
#     if  old_senator_classified >= 95:
#         N_3 = i
#         print(f"N_3 should be {i}")
#         break
#     i += 1

old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "3 days"
WHAT_I_FOUND_INTERESTING = "Nothing in this one, I just couldnt even understand what I was doing I just implemented the specs in the pset specs and tried to pass the tests, i think a mega recitation and tutorials for this pset are missing on ocw"
WHAT_I_FOUND_BORING = "Everything"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception("Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn)

        # raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
