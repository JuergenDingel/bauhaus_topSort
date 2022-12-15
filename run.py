
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import And, Or, Var, config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
# @constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_encoding():
    # Add custom constraints by creating formulas with the variables you created. 
    
    # E.add_constraint((a | b) & ~x)
    # E.add_constraint((a | b) & ~x)
    # Implication
    # E.add_constraint(y >> z)
    # Negate a formula    
#    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
#    constraint.add_exactly_one(E, a, b, c)

    E.add_constraint((a | ~a))
    return E
 

if __name__ == "__main__":

    E = example_encoding()
    # Don't compile until you're finished adding all your constraints!
    T = E.compile()
    T2 = Or([T,Var('W')]).negate()
    # E.introspect()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T2.satisfiable())
    print(" #solutions: %d" % count_solutions(T2))
    soln = T2.solve()
    # E.introspect(soln)    
    print("   Pretty print of theory:")
    E.pprint(T2, soln)
    print("   Solution: %s" % soln)
    print("\nVariable likelihoods:")
    for v,vn in zip([a], 'a'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
#        print(" %s: %s" % (vn, v))
    print("\nValid: %s" % T.valid())
    # print("\nNegating theory:")
    # T = T.negate()
    # print("\nNegation satisfiable: %s" % T.satisfiable())
    # soln = T.solve()    
    # print("   Solution: %s" % soln)    
    print()
