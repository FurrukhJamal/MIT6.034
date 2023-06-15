from production import IF, AND, NOT, OR, THEN, DELETE, forward_chain
from zookeeper import ZOOKEEPER_RULES, ZOO_DATA

theft_rule = IF( 'you have (?x)',
                THEN( 'i have (?x)' ),
                DELETE( 'you have (?x)' ))

data = ( 'you have apple',
        'you have orange',
        'you have pear' )

print(f"type(theft_rule) : {type(theft_rule)}")

print (forward_chain([theft_rule], data, verbose=True))
# print("/n/n TESTING Zookeeper.py")
# print (forward_chain(list(ZOOKEEPER_RULES), [ZOO_DATA], verbose=True))


transitive_rule = IF(AND("(?x) beats (?y)",
                         "(?y) beats (?z)"),
                    THEN("(?x) beats (?z)"))

data = ("three-of-a-kind beats two-pair",
        "two-pair beats pair")

print (forward_chain([transitive_rule], data, verbose=True))
