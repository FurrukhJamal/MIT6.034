from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):              #"(?x) is an (?y)"
    # print(f"hypothesis : {hypothesis}")
    binding = None
    for rule in rules:
        if match(rule.consequent()[0], hypothesis) !=None:
            binding = match(rule.consequent()[0], hypothesis)
    if binding == None :
        return hypothesis
    # print(f"binding : {binding}")
    matches = []
    for rule in rules:
        # print(f"rule.consequent() : {rule.consequent()}")
        try:

            consequent = populate(rule.consequent()[0], binding)
        except KeyError:
            continue
        if consequent == hypothesis:
            matches.append(rule.antecedent())
    
    # print(f"matches : {matches}")
    if len(matches) == 0:
        return hypothesis
    goalTree = OR(hypothesis)
    for antecedent in matches:
        # print(f"typeS : {antecedent[0]}")
        if type(antecedent) == AND or type(antecedent) == OR:
            if type(antecedent) == AND and len(antecedent) == 1:
                antecedentWVariable = populate(antecedent[0], binding)
                node = backchain_to_goal_tree(rules, antecedentWVariable)
                goalTree.append(AND(simplify(node))) # would have to experiment with simplified
            
            elif type(antecedent) == AND and len(antecedent) > 1:
                subTree = []
                for leaf in antecedent:
                    antecedentWVariable = populate(leaf, binding)
                    node = backchain_to_goal_tree(rules, antecedentWVariable)
                    subTree.append(simplify(node))
                goalTree.append(AND(subTree))
            elif type(antecedent) == OR and len(antecedent) == 1:
                antecedentWVariable = populate(antecedent[0], binding)
                node = backchain_to_goal_tree(rules, antecedentWVariable)
                goalTree.append(simplify(OR(node)))
            
            elif type(antecedent) == OR and len(antecedent) > 1:
                subTree = []
                for leaf in antecedent:
                    antecedentWVariable = populate(leaf, binding)
                    node = backchain_to_goal_tree(rules, antecedentWVariable)
                    subTree.append(simplify(node))
                goalTree.append(simplify(OR(subTree)))
        else:
            # print(f"type of antecedent in else : {type(antecedent)}")
            antecedentWVariable = populate(antecedent, binding)
            node = backchain_to_goal_tree(rules,antecedentWVariable)
            # print(f"node : {node}")
            
            goalTree.append(node)
            goalTree = simplify(goalTree)
    
    return goalTree
         
        

# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print(backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin'))

# # Debugging test13
# rules = (
#     IF( AND( '(?x) has (?y)',
#                         '(?x) has (?z)' ),
#                    THEN( '(?x) has (?y) and (?z)' ) ),
#     IF( '(?x) has rhythm and music',
#         THEN( '(?x) could not ask for anything more' ) ) 
             
# )
# print(backchain_to_goal_tree(rules, 'gershwin could not ask for anything more'))
