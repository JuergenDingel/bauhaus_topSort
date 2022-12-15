
from bauhaus import Encoding, proposition, constraint, print_theory
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

COIN = [1, 2, 3, 4]
POS = [1, 2, 3, 4]

class Unique(object):
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __repr__(self):
        return str(self)
    def __str__(self):
        assert False, "You need to define the __str__ function on a proposition class"

####################################
# ## CLASSES FOR ATOMIC PROPOSITIONS
####################################
@proposition(E)
class Lt(Unique):
    def __init__(self, coin1, coin2):
        self.coin1 = coin1
        self.coin2 = coin2
    def __str__(self):
        return f"c{self.coin1}<c{self.coin2}"

@proposition(E)
class At(Unique):
    def __init__(self, coin, pos):
        self.coin = coin
        self.pos = pos
    def __str__(self):
        return f"c{self.coin}@p{self.pos}"

####################################
# GENERAL CONSTRAINTS: 'LESS THAN'
####################################

# no coin is less than itself
for coin in COIN:
    E.add_constraint(~Lt(coin,coin))

# 'less than' on coins is a total order (i.e., for each pair of different coins, exactly one of them is less than the other)
for coin1 in COIN:
    for coin2 in COIN:
        if coin1!=coin2:
            constraint.add_exactly_one(E, Lt(coin1,coin2), Lt(coin2,coin1))

# 'less than' is transitive
for c1 in COIN:
    for c2 in COIN:
       for c3 in COIN:
            E.add_constraint((Lt(c1,c2) & Lt(c2,c3)) >> Lt(c1,c3))

###############################
# GENERAL CONSTRAINTS: ORDERING
###############################

# ordering must respect coin values
for p in POS:
    if p+1 in POS:
        for c1 in COIN:
            for c2 in COIN:
                E.add_constraint((At(c1,p) & At(c2,p+1)) >> Lt(c1,c2))

# every coin is in exactly one position
for c in COIN:
    constraint.add_exactly_one(E, [At(c,p) for p in POS])   

# every position has exactly one coin
for p in POS:
    constraint.add_exactly_one(E, [At(c,p) for c in COIN])   

########################
# ADDITIONAL CONSTRAINTS
########################

# additional constraints; change as appropriate to capture how coin values compare
E.add_constraint(Lt(3,2))    # c3 < c2
E.add_constraint(Lt(2,1))    # c2 < c1
# E.add_constraint(c3ltc1)    # c3 < c1

##########################
# CONSTRAINTS FOR CHECKING 
##########################
# E.add_constraint(At(3,1))
# E.add_constraint(At(2,1))
# E.add_constraint(~At(3,1))

#########
# SOLVING
#########

# Don't compile until you're finished adding all your constraints!
T = E.compile()
# E.introspect()
# After compilation (and only after), you can check some of the properties
# of your model:
print("\nsatisfiable? %s" % T.satisfiable())
print("#solutions: %d" % count_solutions(T))
soln = T.solve()
# E.introspect(soln)
# print("Pretty print of theory:")
# E.pprint(T, soln)

# print solution
print_theory(soln)
# print("solution: %s" % soln)

order = {}
for k in soln:
    if str(k)[2]=='@' and soln[k]:
        print(k)
        order[str(k)[4]] = str(k)[1]

for p in POS:
    print(f'pos {p}: coin {order[str(p)][0]}')

print("\nlikelihood that specific atomic proposition is true:")
# for v,vn in zip([At(c,p) for c in COIN for p in POS], ["c1@p1","c1@p2","c1@p3","c2@p1","c2@p2","c2@p3","c3@p1","c3@p2","c3@p3"]):
for v,vn in zip([At(c,p) for c in COIN for p in POS], [str(At(c,p)) for c in COIN for p in POS]):
    # Ensure that you only send these functions NNF formulas
    # Literals are compiled to NNF here
    print(" %s: %.2f" % (vn, likelihood(T, v)))
#        print(" %s: %s" % (vn, v))

print("\nnegating theory...")
T = T.negate()
print("negation satisfiable: %s" % T.satisfiable())
