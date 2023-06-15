from tree_searcher import Node
from util import INFINITY 

class MyNode(Node):
    def __init__(self, node, parent =None, alpha = None, beta = None):
        self.node = node
        self.alpha = alpha
        self.beta = beta
        self.action = None
        self.parent = parent
    def getValue(self):
        return self.getNode().value
    
    def getNode(self):
        return self.node
    
    def setAlpha(self, val):
        self.alpha = val
    
    def getAlpha(self):
        return self.alpha
    
    def setBeta(self, val):
        self.beta = val
    
    def getBeta(self):
        return self.beta
    
    def getLabel(self):
        return self.node.label
    
    def setLabel(self, val):
        self.node.label = val 
    
    def setAction(self, val):
        self.action = val
    
    def getAction(self):
        return self.action
    
    def getChildren(self):
        return self.node.get_children()
    
    def getParent(self):
        return self.parent
    
    def __str__(self):
        return super().__str__() + f" alpha : {self.alpha} , beta : {self.beta}, parent : {self.parent}, action : {self.action}"          


from tree_searcher import is_leaf

def minimax_find_board_value(board, depth, eval_fn,
                             get_next_moves_fn,
                             is_terminal_fn):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    # print(f"the explored node : {board}")
    if is_terminal_fn(depth, board):
        return eval_fn(board)
    
    for child in board.get_children():
        child.setParent(board)
        child.setAlpha(board.getAlpha())
        child.setBeta(board.getBeta())

    if board.getNodeType() == "MIN":
        flagForPrunningNextBranch = False 
        for move, new_board in get_next_moves_fn(board):
            if flagForPrunningNextBranch == True:
                # prune this child is flag is set
                flagForPrunningNextBranch = False
                continue 
            
            # print(f"exploring child of {board} : {move}")
            # print(f"new_board.getAlpha() : {new_board.getAlpha()} board.getBeta() for {board} : {board.getBeta()}")
            if new_board.getAlpha() < board.getBeta():
                val = -1 * minimax_find_board_value(new_board, depth-1, eval_fn,
                                                    get_next_moves_fn,
                                                    is_terminal_fn)
                # print(f"score fo {move} for parent : {board} is {val} in MIN condition")    
                if val < board.getBeta():
                    # print(f"adding sscore for {move} to its alpha")
                    board.setBeta(val)
                    board.setAction(val)
                    # print(f"DEBUG : board.getBeta() : {board.getBeta()} , board.getParent().getAlpha() : {board.getParent().getAlpha()}")

            # prunning after every iteration of child node check if parents beta is <= alpha of parents parent. if yes prune the next child that is to come 
            if board.getBeta() <= board.getParent().getAlpha():
                flagForPrunningNextBranch = True        
            
        return board.getBeta()    
    
    elif board.getNodeType() == "MAX":
        flagForPrunningNextBranch = False
        for move, new_board in get_next_moves_fn(board):
            if flagForPrunningNextBranch == True:
                flagForPrunningNextBranch = False
                continue   
            # print(f"exploring child of {board} : {move}")
            if new_board.getBeta() > board.getAlpha():
                val = -1 * minimax_find_board_value(new_board, depth-1, eval_fn,
                                                    get_next_moves_fn,
                                                    is_terminal_fn)
                # print(f"score fo {move} for parent : {board} is {val} in MAX condition")
                if val > board.getAlpha():
                    board.setAlpha(val)
                    board.setAction(move)
            # prunning after every iteration of child node check if parents alpha is >= beta of parents parent. if yes prune the next child that is to come 
            if board.getAlpha() >= board.getParent().getBeta():
                flagForPrunningNextBranch = True 

        return board.getAlpha()                

def minimax(board, depth, eval_fn,
            get_next_moves_fn,
            is_terminal_fn,
            verbose = True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    
    best_val = None
    board.setAlpha(-INFINITY)
    board.setBeta(INFINITY)

    for child in board.get_children():
        child.setParent(board)
        child.setAlpha(board.getAlpha())
        child.setBeta(board.getBeta())
    
    for move, new_board in get_next_moves_fn(board):
        
        if new_board.getBeta() > new_board.getParent().getAlpha():
            val = -1 * minimax_find_board_value(new_board, depth-1, eval_fn,
                                                get_next_moves_fn,
                                                is_terminal_fn)
            
            if val > board.getAlpha():
                # print(f"adding sscore for {move} to its beta")
                board.setAlpha(val)
                board.setAction(move)
                
    return board.getAction()






def test_minimax_find_board_value(board, depth, eval_fn,
                             get_next_moves_fn,
                             is_terminal_fn):
    
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * test_minimax_find_board_value(new_board, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
        if best_val == None or val > best_val:
            best_val = val

    return best_val

def test_minimax(board, depth, eval_fn,
            get_next_moves_fn,
            is_terminal_fn,
            verbose = True):
        
    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * test_minimax_find_board_value(new_board, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        print(f"score gotten for {move} : {val}")
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)
            
    if verbose:
        print (f"MINIMAX: Decided on column {best_val[1]} with rating {best_val[0]}")

    return best_val[1]

