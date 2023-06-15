# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
# run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
# run_game(basic_player, human_player)

## Or watch the computer play against itself:
# run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    currentP = board.get_current_player_id()
    otherP = board.get_other_player_id()
    if board.is_game_over():
        score =  -1000
    else : 
        score = board.longest_chain(currentP) * 10
        numOfChains = len(set(filter(lambda x : len(x) > 1, board.chain_cells(currentP))))
        score += numOfChains * 5
        for row in range(board.board_height):
            for col in range(board.board_width):
                if board.get_cell(row, col) == otherP:
                    score -= 1
        # for row in range(6):
        #     for col in range(7):
        #         if board.get_cell(row, col) == board.get_current_player_id():
        #             score -= abs(3-col)
        #         elif board.get_cell(row, col) == board.get_other_player_id():
        #             score += abs(3-col)
    
    return score 



## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

# def alphaBetaScore(node, depth, get_next_moves_fn, is_terminal_fn):
#     print(f"node in function alphaScore : {node.getNode()}")
#     from practice import MyNode
#     if is_terminal_fn(depth, node.getNode()):
#         print(f"terminal node : {node.getLabel()}")
#         return 

    
#     for label, n in get_next_moves_fn(node.getNode()):
#         print(f"L : {label}")
#         N = MyNode(n, node, node.getAlpha(), node.getBeta())
#         alphaBetaScore(N, depth - 1, get_next_moves_fn, is_terminal_fn)

def alphaBeta_find_board_value(board, depth, eval_fn, 
                                                get_next_moves_fn,
                                                is_terminal_fn, labelNum,):
    # print(f"the explored node : {board}")
    if is_terminal_fn(depth, board.getBoard()):
        return eval_fn(board.getBoard())
    
    from node import Node
    children = get_next_moves_fn(board.getBoard())
    
    # child is (move, new_board)
    for child in children:
        child = Node(child[1], (labelNum, child), "MIN")
        board.add(child)
        child.setParent(board)
        child.setAlpha(board.getAlpha())
        child.setBeta(board.getBeta())
        labelNum += 1

    if board.getNodeType() == "MIN":
        flagForPrunningNextBranch = False 
        # for move, new_board in board.get_children():
        for node in board.get_children():
            move = node.getLabel()[1][0]
            new_board = node
            if flagForPrunningNextBranch == True:
                # prune this child is flag is set
                flagForPrunningNextBranch = False
                continue 
            
            # print(f"exploring child of {board} : {move}")
            # print(f"new_board.getAlpha() : {new_board.getAlpha()} board.getBeta() for {board} : {board.getBeta()}")
            if new_board.getAlpha() < board.getBeta():
                val = -1 * alphaBeta_find_board_value(new_board, depth-1, eval_fn,
                                                    get_next_moves_fn,
                                                    is_terminal_fn, labelNum)
                # print(f"score fo {move} for parent : {board} is {val} in MIN condition")    
                if val < board.getBeta():
                    # print(f"adding sscore for {move} to its alpha")
                    board.setBeta(val)
                    board.setAction(move)
                    # print(f"DEBUG : board.getBeta() : {board.getBeta()} , board.getParent().getAlpha() : {board.getParent().getAlpha()}")

            # prunning after every iteration of child node check if parents beta is <= alpha of parents parent. if yes prune the next child that is to come 
            if board.getBeta() <= board.getParent().getAlpha():
                flagForPrunningNextBranch = True        
            
        return board.getBeta()    
    
    elif board.getNodeType() == "MAX":
        flagForPrunningNextBranch = False
        
        # for move, new_board in board.get_children():
        for node in board.get_children():
            move = node.getLabel()[1][0]
            new_board = node    
            if flagForPrunningNextBranch == True:
                flagForPrunningNextBranch = False
                continue   
            # print(f"exploring child of {board} : {move}")
            if new_board.getBeta() > board.getAlpha():
                val = -1 * alphaBeta_find_board_value(new_board, depth-1, eval_fn,
                                                    get_next_moves_fn,
                                                    is_terminal_fn, labelNum)
                # print(f"score fo {move} for parent : {board} is {val} in MAX condition")
                if val > board.getAlpha():
                    board.setAlpha(val)
                    board.setAction(move)
            # prunning after every iteration of child node check if parents alpha is >= beta of parents parent. if yes prune the next child that is to come 
            if board.getAlpha() >= board.getParent().getBeta():
                flagForPrunningNextBranch = True 

        return board.getAlpha()



## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    # raise NotImplementedError
    
    from node import Node
    children = get_next_moves_fn(board)
    
    board = Node(board, "root", "MAX")
    best_val = None
    
    board.setAlpha(-INFINITY)
    board.setBeta(INFINITY)
    labelNum = 0
    # child is (move, new_board)
    for child in children:
        child = Node(child[1], (labelNum, child), "MIN")
        board.add(child)
        child.setParent(board)
        child.setAlpha(board.getAlpha())
        child.setBeta(board.getBeta())
        labelNum += 1
    
    
    # for move, new_board in board.get_children():
    for node in board.get_children():
        move = node.getLabel()[1][0]
        new_board = node    
        if new_board.getBeta() > new_board.getParent().getAlpha():
            val = -1 * alphaBeta_find_board_value(new_board, depth-1, eval_fn,
                                                get_next_moves_fn,
                                                is_terminal_fn, labelNum)
            
            if val > board.getAlpha():
                # print(f"adding sscore for {move} to its beta")
                board.setAlpha(val)
                board.setAction(move)
                
    return board.getAction()


    
    
      


## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
# run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
    # raise NotImplementedError
    currentP = board.get_current_player_id()
    otherP = board.get_other_player_id()
    if board.is_game_over():
        score =  -1000
    else : 
        score = board.longest_chain(currentP) * 10
        # score = 0
     
        # horizontal line check reversed order
        for row in range((board.board_height - 1), -1, -1):
            for col in range(board.board_width):
                if board.get_cell(row, col) == currentP:
                    try:
                        counter = 0
                        for i in range(1, 4):
                            if board.get_cell(row, col + i) == currentP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row, col + i) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"Found a horizontal line")
                            score += 10
                        if counter == 1:
                            score += 5 
                    except(KeyError, IndexError):
                        pass
                # detect opponents line
                if board.get_cell(row, col) == otherP:
                    try:
                        counter = 0
                        for i in range(1, 4):
                            if board.get_cell(row, col + i) == otherP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row, col + i) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"Found a horizontal line")
                            score -= 100
                         
                    except(KeyError, IndexError):
                        pass

        
        # # vertical line
        for col in range(board.board_width):
            for row in range(board.board_height -1, -1, -1):
                try:
                    counter = 0
                    # print(f"player at row : {row} col : {col} : {board.get_cell(row , col)}")
                    if board.get_cell(row , col) == currentP:
                        for i in range(-1, -4, -1):
                            # print(f"i: {i}")
                            if board.get_cell(row + i, col) == currentP and i > -3:
                                counter += 1
                            elif i == -3 and board.get_cell(row + i, col) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"found a vertical line")
                            score += 10
                        if counter == 2:
                            score += 3
                         
                except (KeyError, IndexError):
                    pass

                # detect if opponent has a three coin line
                if board.get_cell(row , col) == otherP:
                    try:    
                        for i in range(-1, -4, -1):
                            # print(f"i: {i}")
                            if board.get_cell(row + i, col) == otherP and i > -3:
                                counter += 1
                            elif i == -3 and board.get_cell(row + i, col) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"found a vertical line")
                            score -= 500 
                    except (KeyError, IndexError):
                        pass
                 
        # Diagnol reversed 
        for row in range(board.board_height - 1, -1, -1):
            for col in range(board.board_width):
                #daignol in direction down right from (row, col)
                if board.get_cell(row, col) == currentP:
                    try:
                        counter = 0 
                        for i in range(1, 4):
                            if board.get_cell(row + i, col + i) == currentP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row + i, col + i) == 0:
                                counter += 1    
                            else:
                                break
                          
                        if counter == 3:
                            # print(f"found a daignol line")
                            score += 20
                        if counter == 1 and board.get_cell(row - 1, col - 1 ) == 0 and board.get_cell(row, col - 1) != 0:
                            score += 15
                        
                    except (KeyError, IndexError):
                        pass
                ### Stop opponent in the same direction
                if board.get_cell(row, col) == otherP:
                    try:
                        counter = 0 
                        for i in range(1, 4):
                            if board.get_cell(row + i, col + i) == otherP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row + i, col + i) == 0:
                                counter += 1    
                            else:
                                break
                          
                        if counter == 3:
                            # print(f"found a daignol line")
                            score -= 20
                        
                                               
                    except (KeyError, IndexError):
                        pass
                 
                
                # daignol in direction up right from (row, col)
                if board.get_cell(row, col) == currentP:    
                    try:
                        counter = 0 
                        # print(f"player : {board.get_cell(row, col)}")
                        for i in range(1, 4):
                            if board.get_cell(row - i, col + i) == currentP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row - i, col + i) == 0:
                                counter +=10
                            else:
                                break
                        if counter == 3:
                            # print(f"found a daignol line")
                            score += 20
                        if counter == 1 and board.get_cell(row - 2, col + 2) == 0 and board.get_cell(row - 1, col + 2) != 0:
                            score += 15 
                    except (KeyError, IndexError):
                        pass 
                ### Stop opponent in the same direction 
                if board.get_cell(row, col) == otherP:    
                    try:
                        counter = 0 
                        # print(f"player : {board.get_cell(row, col)}")
                        for i in range(1, 4):
                            if board.get_cell(row - i, col + i) == otherP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row - i, col + i) == 0:
                                counter +=1
                            else:
                                break
                        if counter == 3:
                            # print(f"found a daignol line")
                            score -= 20

                        
                    except (KeyError, IndexError):
                        pass
                
                
                
                # daignol in direction down left from (row, col)        
                if board.get_cell(row, col) == currentP:
                    
                    try:        
                        counter = 0 
                        for i in range(1, 4):
                            if board.get_cell(row + i, col - i) == currentP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row + i, col - i) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"found a daigonal line")
                            score += 20
                        if counter == 1 and board.get_cell(row + 1, col + 1) == 0 and board.get_cell(row, col + 1) != 0:
                            score += 15
                    except (KeyError, IndexError):
                        pass
                ###Stop opponent in the same direction
                if board.get_cell(row, col) == otherP:
                    
                    try:        
                        counter = 0 
                        for i in range(1, 4):
                            if board.get_cell(row + i, col - i) == otherP and i < 3:
                                counter += 1
                            elif i == 3 and board.get_cell(row + i, col - i) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"found a daigonal line")
                            score -= 100
                        
                    except (KeyError, IndexError):
                        pass 
                
                
                
                
                # daignol in direction up left from (row, col)
                if board.get_cell(row, col) == currentP:
                    try:                         
                        counter = 0 
                        # print(f"currentP : {currentP}")
                        for i in range(1, 4):
                            # print(f"(row - i : {row - i}, col - i : {col - i}) = {board.get_cell(row - i, col - i)}")
                            
                            if board.get_cell(row - i, col - i) == currentP and i < 3:
                                counter += 1
                            elif i == 3 and  board.get_cell(row - i, col - i) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"found a daignol line at row :{row}")
                            score += 20
                        if counter == 1 and board.get_cell(row - 2, col - 2) == 0 and board.get_cell(row - 1, col - 2) != 0:
                            score += 15

                    except (KeyError, IndexError):
                        pass
                ### Stop opponent in the same direction
                if board.get_cell(row, col) == otherP:
                    try:                         
                        counter = 0 
                        # print(f"currentP : {currentP}")
                        for i in range(1, 4):
                            if board.get_cell(row - i, col - i) == otherP and i < 3:
                                counter += 1
                            elif i == 3 and  board.get_cell(row - i, col - i) == 0:
                                counter += 1
                            else:
                                break
                        if counter == 3:
                            # print(f"found a daignol line at row :{row}")
                            score -= 20
                        
                    except (KeyError, IndexError):
                        pass
                # Stopping opponent for daignols with one missing in bw
                if board.get_cell(row, col) == otherP:
                    try:
                        counter = 1
                        for i in range(1,4):
                            if board.get_cell(row - i, col + i) == otherP:
                                counter += 1
                        if counter == 3:
                            score -= 12
                        counter = 1
                        for i in range(1,4 ):
                            if board.get_cell(row - i, col - i) == otherP:
                                counter += 1
                        if counter == 3:
                            score -= 12
                    except(IndexError, KeyError):
                        pass
                # stopping opponent having three consecutive horizontally after empty cell
                if board.get_cell(row, col) == 0:
                    try:
                        counter = 0
                        for i in range(1,4):
                            if board.get_cell(row, col + i) == otherP:
                                counter += 1
                        if counter == 3:
                            score -=500
                        if counter == 2:
                            score -= 200
                    except(IndexError, KeyError):
                        pass 
                
        
        
        # diagnol line
        # for row in range(board.board_height):
        #     for col in range(board.board_width):
        #         # daignol in direction down right from (row, col)
        #         if board.get_cell(row, col) == currentP:
        #             try:
        #                 counter = 0
        #                 for i in range(1, 4):
        #                     if board.get_cell(row + i, col + i) == currentP and i < 3:
        #                         counter += 1
        #                     elif i == 3 and board.get_cell(row + i, col + i) == 0:
        #                         counter += 1    
        #                     else:
        #                         break
                          
        #                 if counter == 3:
        #                     # print(f"found a daignol line")
        #                     score += 10
        #             except (KeyError, IndexError):
        #                 pass    
                   
        #         # daignol in direction up right from (row, col)
        #         if board.get_cell(row, col) == currentP:    
        #             try:
        #                 counter = 0 
        #                 # print(f"player : {board.get_cell(row, col)}")
        #                 for i in range(1, 4):
        #                     if board.get_cell(row - i, col + i) == currentP and i < 3:
        #                         counter += 1
        #                     elif i == 3 and board.get_cell(row - i, col + i) == 0:
        #                         counter +=10
        #                     else:
        #                         break
        #                 if counter == 3:
        #                     # print(f"found a daignol line")
        #                     score += 10
        #             except (KeyError, IndexError):
        #                 pass 
        #         # daignol in direction down left from (row, col)        
        #         if board.get_cell(row, col) == currentP:
                    
        #             try:        
        #                 counter = 0 
        #                 for i in range(1, 4):
        #                     if board.get_cell(row + i, col - i) == currentP and i < 3:
        #                         counter += 1
        #                     elif i == 3 and board.get_cell(row + i, col - i) == 0:
        #                         counter += 1
        #                     else:
        #                         break
        #                 if counter == 3:
        #                     # print(f"found a daigonal line")
        #                     score += 10
        #             except (KeyError, IndexError):
        #                 pass
        #         # daignol in direction up left from (row, col)
        #         if board.get_cell(row, col) == currentP:
        #             try:                         
        #                 counter = 0 
        #                 # print(f"currentP : {currentP}")
        #                 for i in range(1, 4):
        #                     # print(f"(row - i : {row - i}, col - i : {col - i}) = {board.get_cell(row - i, col - i)}")
                            
        #                     if board.get_cell(row - i, col - i) == currentP and i < 3:
        #                         counter += 1
        #                     elif i == 3 and  board.get_cell(row - i, col - i) == 0:
        #                         counter += 1
        #                     else:
        #                         break
        #                 if counter == 3:
        #                     # print(f"found a daignol line at row :{row}")
        #                     score += 10
        #             except (KeyError, IndexError):
        #                 pass    
                    
        


        numOfPlaces = board.board_width * board.board_height
        remaining = numOfPlaces - board.num_tokens_on_board()
        # print(f"spots remaining: {remaining}")
        score -= remaining              
    return score

# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if True:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # # # better evaluate from player 1
    # print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    print (f"{test_board_1} => {better_evaluate(test_board_1)}")
    # better evaluate from player 2
    # print "%s => %s" %(test_board_2, better_evaluate(test_board_2))
    # print (f"{test_board_2} => {better_evaluate(test_board_2)}")

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
# run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
# run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "more than a week"
WHAT_I_FOUND_INTERESTING = "learning the alpha beta on paper"
WHAT_I_FOUND_BORING = "evaluation functions"
NAME = "Furrukh"
EMAIL = "furrukh@example.com"

