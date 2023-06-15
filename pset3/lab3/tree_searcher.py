#
# This tree searcher uses the lab3 games framework
# to run alpha-beta searches on static game trees
# of the form seen in quiz/recitation/tutorial examples.
#
# (See TEST_1 for an example tree.)
#
# In the directory where lab3.py lives, run:
#
#    ~> python tree_search.py
#
# But as prereq, your lab3.py should have def alpha_beta_search
# implemented, and your function signature conforms to the interface
# defined below:
#
# def alpha_beta_search(board, depth,
#                       eval_fn,
#		        get_next_moves_fn,
#		        is_terminal_fn):
#
# In context of tree searches:
#
# board is the current tree node.
#
# depth is the search depth.  If you specify depth as a very large
#   number then your search will end at the leaves of trees.
# 
# def eval_fn(board):
#   a function that returns a score for a given board from the
#   perspective of the state's current player.
#
# def get_next_moves(board):
#   a function that takes a current node (board) and generates
#   all next (move, newboard) tuples.
#
# def is_terminal_fn(depth, board):
#   is a function that checks whether to statically evaluate
#   a board/node (hence terminating a search branch).
#
# You can modify the existing alpha_beta_search interface in lab3
# to work with this interface by definining your own is_terminal_fn
# using optional arguments, like so:
#
# def alpha_beta_search(board, depth,
#                       eval_fn,
#                       get_next_moves_fn=get_all_next_moves,
#                       is_terminal_fn=<your_terminal_function>):
class Node:
	"""
	Representation of a generic game tree node.
	Each node holds
	1. a label
	2. a static value (internal nodes
	generally have a None static value)
	3. node type  {MIN, MAX}
	4. list of child nodes.
		"""
	def __init__(self, label, value, node_type, children=[]):
		self.label = label
		self.value = value
		self.node_type = node_type
		self.children = children
		# custom addition
		self.alpha = None
		self.beta = None
		self.parent = None
		# the name of child thats used to update this node's alpha or beta
		self.action = None 
		# end of custom addition

	# custom added methods
	def getNodeType(self):
		return self.node_type
	def getAction(self):
		return self.action
	def setAction(self, val):
		self.action = val 
	def getParent(self):
		return self.parent
	def setParent(self, val):
		self.parent = val 
	def setAlpha(self, val):
		self.alpha = val
	def getAlpha(self):
		return self.alpha
	def setBeta(self, val):
		self.beta = val
	def getBeta(self):
		return self.beta  
	# end of methods
	
	
	def set_children(self, child_nodes):
		"""Set the children of this tree node"""
		if not self.children:
			self.children = []
		for child in child_nodes:
			self.children.append(child)

	def get_children(self):
		return self.children

	def __str__(self):
		"""Print the value of this node."""
		if self.value is None:
			return self.label
		else:
			return "%s[%s]" %(self.label, self.value)

	def add(self, child):
		"""Add children to this node."""
		if not self.children:
			self.children = []	    
		self.children.append(child)

	def num_children(self):
		"""Find how many children this node has."""
		if self.children:
			return len(self.children)
		else:
			return 0

def tree_as_string(node, depth=0):
	"""
	Generates a string representation of the tree
	in a space indented format
	"""
	static_value = tree_eval(node)
	# buf = "%s%s:%s\n" %(" "*depth, node.label, static_value)
	buf = f"{' '*depth}{node.label}:{static_value}\n"
	for elt in node.children:
		buf += tree_as_string(elt, depth+1)
	return buf

def make_tree(tup):
    """
    Generates a Node tree from a tuple formatted tree
    """
    return make_tree_helper(tup, "MAX")
    
def make_tree_helper(tup, node_type):
	"""Generate a Tree from tuple format"""
	n = Node(tup[0], tup[1], node_type)
	# print(f"tup in make_tree_helper : {tup}")
	children = []
	if len(tup) > 2:
		if node_type == "MAX":
			node_type = "MIN"
		else:
			node_type = "MAX"
		
	for c in range(2,len(tup)):
		# print(f"adding {tup[c]} as child")
		children.append(make_tree_helper(tup[c], node_type))
	n.set_children(children)
	
	return n

def is_at_depth(depth, node):
    """
    is_terminal_fn for fixed depth trees
    True if depth == 0 has been reached.
    """
    return depth <= 0

def is_leaf(depth, node):
    """
    is_terminal_fn for variable-depth trees.
    Check if a node is a leaf node.
    """
    return node.num_children() == 0


def tree_get_next_move(node):
    """
    get_next_move_fn for trees
    Returns the list of next moves for traversing the tree
    """
    return [(n.label, n) for n in node.children]

def tree_eval(node):
	"""
	Returns the static value of a node
	"""
	# if node.value is not None:
	# if node.node_type == "MIN":
	#     return -node.value
	# elif node.node_type == "MAX":
	#     return node.value
	#     else:
	#         raise Exception("Unrecognized node type: %s" %(node.node_type))
	# else:
	#     return None
	if node.value is not None:
		if node.node_type == "MIN":
			return -node.value
		elif node.node_type == "MAX":
			return node.value
		else:
			# raise Exception("Unrecognized node type: %s" %(node.node_type))
			raise Exception("Unrecognized node type: %s" % (node.node_type,))

	else:
		return None

def TEST_1(expected):
	# from lab3 import alpha_beta_search
	from practice import minimax
	tup_tree = ("A", None,
		("B", None,
			("C", None,
			("D", 2),
			("E", 2)),
			("F", None,
			("G", 0),
			("H", 4))
			),
		("I", None,
			("J", None,
			("K", 6),
			("L", 8)),
			("M", None,
			("N", 4),
			("O", 6))
			)
		)
	print(f"tup_tree in TEST_1 : {tup_tree}")
	print(f"its length : {len(tup_tree)}\n")
	tree = make_tree(tup_tree)
	# print "%s:\n%s" %("TREE_1", tree_as_string(tree))
	print(f"TREE_1:\n{tree_as_string(tree)}")
	# v = alpha_beta_search(tree, 10,
	# 			tree_eval,
	# 			tree_get_next_move,
	# 			is_leaf)
	v = minimax(tree, 10,
				tree_eval,
				tree_get_next_move,
				is_leaf)
	# print "BEST MOVE: %s" %(v)
	print(f"BEST MOVE: {v}")
	print(f"EXPECTED: {expected}")

def TEST_2(expected):
    # from lab3 import alpha_beta_search
	from practice import minimax
	tup_tree = ("A", None,
		("B", None,
			("C", None,
			("D", 6),
			("E", 4)),
			("F", None,
			("G", 8),
			("H", 6))
			),
		("I", None,
			("J", None,
			("K", 4),
			("L", 0)),
			("M", None,
			("N", 2),
			("O", 2))
			)
		)
	tree = make_tree(tup_tree)
	print (f"TREE_2:\n{tree_as_string(tree)}")
	# v = alpha_beta_search(tree, 10,
	# 			tree_eval,
	# 			tree_get_next_move,
	# 			is_leaf)

	v = minimax(tree, 10,
				tree_eval,
				tree_get_next_move,
				is_leaf)
	print (f"BEST MOVE: {v}") 
	print (f"EXPECTED: {expected}" )

def TEST_3(expected):
    # from lab3 import alpha_beta_search
	from practice import minimax, test_minimax
	tup_tree = ("A", None,
		("B", None,
			("E", None,
			("K", 8),
			("L", 2)),
			("F", 6)
			),
		("C", None,
			("G", None,
			("M", None,
			("S", 4),
			("T", 5)),
			("N", 3)),
			("H", None,
			("O", 9),
			("P", None,
			("U", 10),
			("V", 8))
			),
			),
		("D", None,
			("I", 1),
			("J", None,
			("Q", None,
			("W", 7),
			("X", 12)),
			("K", None,
			("Y", 11),
			("Z", 15)
			),
			)
			)
		)
	tree = make_tree(tup_tree)
	print (f"TREE_3:\n{tree_as_string(tree)}")
	# v = alpha_beta_search(tree, 10,
	# 			tree_eval,
	# 			tree_get_next_move,
	# 			is_leaf)
	v = minimax(tree, 10,
				tree_eval,
				tree_get_next_move,
				is_leaf)
	# v = test_minimax(tree, 10,
	# 			tree_eval,
	# 			tree_get_next_move,
	# 			is_leaf)
	
	print (f"BEST-MOVE: {v}") 
	print (f"EXPECTED: {expected}")

if __name__ == "__main__":
    # Run basic tests using trees.
    TEST_1("I")
    TEST_2("B")
    TEST_3("B")
