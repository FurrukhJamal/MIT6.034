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
    def __init__(self, board, label, node_type, children=[], value = None):
        self.label = label
        self.value = value
        self.node_type = node_type
        self.children = children
        self.board = board
        # custom addition
        self.alpha = None
        self.beta = None
        self.parent = None
        # the name of child thats used to update this node's alpha or beta
        self.action = None 
        # end of custom addition

    # custom added methods
    def getLabel(self):
        return self.label
    def getBoard(self):
        return self.board
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