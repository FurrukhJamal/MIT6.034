# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5 or Python v2.6
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = 'fill-me-in'


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
    return x*x*x

def factorial(x):
    if x < 0:
        raise Exception("x must not be negative")
    if x == 0:
        return 1
    return x * factorial(x -1)

def count_pattern(pattern, lst):
    lenPattern = len(pattern)
    numPatterns = 0
    for i in range(0,len(lst) - (len(pattern)) + 1):
        # print(f"lst[i] : {lst[i]}")
        if lst[i] == pattern[0]:
            # print(f"matched lst[i] : {lst[i]}")
            counter = 0 
            for j in range(1,len(pattern)):
                # print(f"pattern[j] : {pattern[j]}")
                if lst[i + j] == pattern[j]:
                    counter += 1

            if counter == len(pattern) - 1:
                numPatterns += 1
    
    # print(f"patterns : {numPatterns}")
    return numPatterns

                




# Problem 2.2: Expression depth

def depth(expr):
    # base case expression is a variable
    # if not isinstance(expr, (tuple, list)):
    #     return 0 
    # elif isinstance(expr, list) and len(expr) == 1:
    #     print("return 1 condition")
    #     return 1
    # else : 
    #     op, *args = expr
    #     print(f"type(args) : {type(args)}")
    #     dept =  depth(args)
    #     # for arg in args:
    #     #     dept += depth(args)
    #     return dept 

    # print(f"type(expr) at start of function : {type(expr)}")
    # print(f"expr : {expr}")
    if not isinstance(expr, (tuple, list)):  # Base case: expression is a variable
        # print(f"base case hitting,expr: {expr}")
        return 0
    
    else:
        # print(f"type(expr) in else condition: {type(expr)}")
        op, *args = expr  # Split tuple into operator and arguments
        # print(f"args : {args} type(args) : {type(args)}")
        # return 1 + max(depth(arg) for arg in args)
        dept = 1
        result = [] 
        for arg in args:
            result.append(depth(arg))
        # print(f"result : {result}")
        dept += max(result)
        # print(f"dept : {dept}\n")
        return dept
    


# Problem 2.3: Tree indexing

def tree_ref(tree, index):
    temp = None
    for i in range(len(index)):
        if temp == None:
            temp = tree[index[i]]
        else:
            temp = temp[index[i]]
    return temp  
    



# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = "2023"

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = "8"

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = "fair"

# How many hours did this lab take?
HOURS = "10"


if __name__ == "__main__":
    # count_pattern(["a", "b", "a"], ['g', 'a', 'b', 'a', 'b', 'a', 'b', 'a'])
    # count_pattern(["a", "b"], ['a', 'b', 'c', 'e', 'b', 'a', 'b', 'f'])
    # print(depth('x'))
    print(depth(('expt', 'x', 2))) # 1
    # print(depth(('+', ('expt', 'x', 2), ('expt', 'y', 2)))) # 2
    # print(depth(('/', ('expt', 'x', 5), ('expt', ('-', ('expt', 'x', 2), 1), ('/', 5, 2))))) # 4
    print(depth(['+', ['expt', 'x', 2], ['expt', 'y', 2]]))

    # print(tree_ref((((1, 2), 3), (4, (5, 6)), 7, (8, 9, 10)), (3, 1))) # 9
    # print(tree_ref((((1, 2), 3), (4, (5, 6)), 7, (8, 9, 10)), (1, 1, 1))) # 6
    # print(tree_ref((((1, 2), 3), (4, (5, 6)), 7, (8, 9, 10)), (0,))) #((1,2), 3)