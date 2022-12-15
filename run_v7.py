
from bauhaus import Encoding, proposition, constraint, print_theory
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

TASK = [1, 2, 3]
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
# instances of this class represent atomic propositions 'DepOn(t1,t2)' capturing that task t1 depends on task t2
@proposition(E)
class DepOn(Unique):
    def __init__(self,task1,task2):
        self.task1 = task1
        self.task2 = task2
    def __str__(self):
        return f"t{self.task1}>t{self.task2}"

# instances of this class represent atomic propositions 'At(t,p)' capturing that task t is assigned position p
@proposition(E)
class At(Unique):
    def __init__(self, task, pos):
        self.task = task
        self.pos = pos
    def __str__(self):
        return f"t{self.task}@p{self.pos}"

####################################
# GENERAL CONSTRAINTS: 'DEPENDS ON'
####################################

# no task depends on itself
for task in TASK:
   E.add_constraint(~DepOn(task,task))


# DepOn is transitive 
for t1 in TASK:
    for t2 in TASK:
       for t3 in TASK:
            E.add_constraint((DepOn(t1,t2) & DepOn(t2,t3)) >> DepOn(t1,t3))

###############################
# GENERAL CONSTRAINTS: ORDERING
###############################

# ordering must respect task dependencies
for p1 in POS:
    for p2 in [p for p in POS if p>p1]:
        for t1 in TASK :
            for t2 in TASK :
                E.add_constraint((At(t1,p1) & At(t2,p2)) >> ~DepOn(t1,t2))

# every task is in exactly one position
for t in TASK:
    constraint.add_exactly_one(E, [At(t,p) for p in POS])   

# every position has exactly one task
# for p in POS:
#    constraint.add_exactly_one(E, [At(t,p) for t in TASK])   

# every position has as most one task
for p in POS:
    constraint.add_at_most_one(E, [At(t,p) for t in TASK])   

########################
# ADDITIONAL CONSTRAINTS
########################
# additional constraints; change as appropriate to capture how task values compare
E.add_constraint(DepOn(3,2))    # t3 > t2
# E.add_constraint(DepOn(2,1))    # t2 > t1
# E.add_constraint(DepOn(3,1))    # t3 > t1
# E.add_constraint(~DepOn(3,1))    # t3 > t2
# E.add_constraint(~DepOn(2,1))    # t3 > t2
# E.add_constraint(~DepOn(2,3))    # t3 > t2
# E.add_constraint(~DepOn(1,2))    # t3 > t2
# E.add_constraint(~DepOn(1,3))    # t3 > t2

##########################
# CONSTRAINTS FOR CHECKING 
##########################
# E.add_constraint(~At(3,3))
# E.add_constraint(At(2,3))
# E.add_constraint(~At(3,3))
# E.add_constraint(At(3,1))
# E.add_constraint(~(At(3,2) >> At(2,1)))
# E.add_constraint(~((DepOn(1,2) >> ~DepOn(2,1)) & (DepOn(1,3) >> ~DepOn(3,1)) & \
#                    (DepOn(2,1) >> ~DepOn(1,2)) & (DepOn(2,3) >> ~DepOn(3,2)) & \
#                    (DepOn(3,1) >> ~DepOn(1,3)) & DepOn(3,2) >> ~DepOn(2,3)))
# E.add_constraint(DepOn(1,2) & DepOn(2,1))

#########
# SOLVING
#########

# don't compile until you're finished adding all your constraints!
T = E.compile()
# E.introspect()
# after compilation (and only after), you can check some of the properties
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

if soln: 
    order = {}
    for p in POS:
        order[str(p)] = '_'

    for k in soln:
        if str(k)[2]=='@' and soln[k]:
            order[str(k)[4]] = str(k)[1]

    print("Dependencies: ", end="")
    for k in soln:
        if str(k)[2]=='>' and soln[k]:
            print(k, end="   ")
 
    print("\nPosition:     ", end="")
    for p in POS:
        print(p, end="    ")

    print("\nTask:         ", end="")
    for p in POS:
        print(order[str(p)][0], end="    ")

    print("\nlikelihood that specific atomic proposition is true:")
    for v,vn in zip([At(t,p) for t in TASK  for p in POS], [str(At(t,p)) for t in TASK  for p in POS]):
        # ensure that you only send these functions NNF formulas
        # literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
