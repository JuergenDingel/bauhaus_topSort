
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class CoinComparisonPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Cmp.{self.data}"

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class CoinOrderingPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Ord.{self.data}"

# Atomic propositions capturing how the values of coins compare (atomic propositions for comparing coins)
c1ltc2 = CoinComparisonPropositions("c1ltc2")    # true iff value of coin c1 is less than value of coin c2
c1ltc3 = CoinComparisonPropositions("c1ltc3")
c2ltc1 = CoinComparisonPropositions("c2ltc1")
c2ltc3 = CoinComparisonPropositions("c2ltc3")
c3ltc1 = CoinComparisonPropositions("c3ltc1")
c3ltc2 = CoinComparisonPropositions("c3ltc2")

# Atomic propositions capturing where in the order a coin appears (APs for ordering coins)
c1Atp1 = CoinOrderingPropositions("c1@p1")    # true iff coin c1 appears in position 1
c1Atp2 = CoinOrderingPropositions("c1@p2")   
c1Atp3 = CoinOrderingPropositions("c1@p3")   
c2Atp1 = CoinOrderingPropositions("c2@p1")    # true iff coin c2 appears in position 1
c2Atp2 = CoinOrderingPropositions("c2@p2")   
c2Atp3 = CoinOrderingPropositions("c2@p3")   
c3Atp1 = CoinOrderingPropositions("c3@p1")    # true iff coin c3 appears in position 1
c3Atp2 = CoinOrderingPropositions("c3@p2")   
c3Atp3 = CoinOrderingPropositions("c3@p3")   

# Add constraints involving APs for comparing coins
def add_coinComparison_constraints():
    # change as appropriate to capture how coin values compare
    E.add_constraint(c3ltc2)    # c3 < c2
    E.add_constraint(c2ltc1)    # c2 < c1
    E.add_constraint(c3ltc1)    # c3 < c1

    E.add_constraint(c1ltc2 >> ~c2ltc1)     # anti-symmetry
    E.add_constraint(c1ltc3 >> ~c3ltc1)
    E.add_constraint(c2ltc1 >> ~c1ltc2)
    E.add_constraint(c2ltc3 >> ~c3ltc2)
    E.add_constraint(c3ltc1 >> ~c1ltc3)
    E.add_constraint(c3ltc2 >> ~c2ltc3)

    # E.add_constraint(~c1ltc2 >> c2ltc1)       # if c1ltc2 doesn't hold, then c2ltc1 does 
    # E.add_constraint(~c1ltc3 >> c3ltc1)       # does not seem to be required
    # E.add_constraint(~c2ltc1 >> c1ltc2)
    # E.add_constraint(~c2ltc3 >> c3ltc2)
    # E.add_constraint(~c3ltc1 >> c1ltc3)
    # E.add_constraint(~c3ltc2 >> c2ltc3)

    E.add_constraint((c1ltc2 & c2ltc3) >> c1ltc3)       # transitivity
    E.add_constraint((c1ltc3 & c3ltc2) >> c1ltc2)
    E.add_constraint((c2ltc1 & c1ltc3) >> c2ltc3)
    E.add_constraint((c2ltc3 & c3ltc1) >> c2ltc1)
    E.add_constraint((c3ltc1 & c1ltc2) >> c3ltc2)
    E.add_constraint((c3ltc2 & c2ltc1) >> c3ltc1)
    return E

# Add constraints involving APs for ordering coins
def add_coinOrdering_constraints():
    # ordering must respect coin values
    E.add_constraint((c1Atp1 & c2Atp2) >> c1ltc2)     # if c1 at l1 and c2 at l2, then c1 less than c2
    E.add_constraint((c1Atp1 & c3Atp2) >> c1ltc3)
    E.add_constraint((c2Atp1 & c1Atp2) >> c2ltc1)
    E.add_constraint((c2Atp1 & c3Atp2) >> c2ltc3)
    E.add_constraint((c3Atp1 & c1Atp2) >> c3ltc1)
    E.add_constraint((c3Atp1 & c2Atp2) >> c3ltc2)

    E.add_constraint((c1Atp2 & c2Atp3) >> c1ltc2)     # if c1 at l1 and c2 at l3, then c1 less than c2
    E.add_constraint((c1Atp2 & c3Atp3) >> c1ltc3)
    E.add_constraint((c2Atp2 & c1Atp3) >> c2ltc1)
    E.add_constraint((c2Atp2 & c3Atp3) >> c2ltc3)
    E.add_constraint((c3Atp2 & c1Atp3) >> c3ltc1)
    E.add_constraint((c3Atp2 & c2Atp3) >> c3ltc2)

    # every coin is at least one position 
    E.add_constraint(c1Atp1 | c1Atp2 | c1Atp3)
    E.add_constraint(c2Atp1 | c2Atp2 | c2Atp3)
    E.add_constraint(c3Atp1 | c3Atp2 | c3Atp3)

    # every coin is at most one position
    E.add_constraint(c1Atp1 >> ~(c1Atp2 | c1Atp3))     # if c1 is at p1, then it is not at p2 or p3
    E.add_constraint(c1Atp2 >> ~(c1Atp1 | c1Atp3))
    E.add_constraint(c1Atp3 >> ~(c1Atp1 | c1Atp2))
    E.add_constraint(c2Atp1 >> ~(c2Atp2 | c2Atp3))
    E.add_constraint(c2Atp2 >> ~(c2Atp1 | c2Atp3))
    E.add_constraint(c2Atp3 >> ~(c2Atp1 | c2Atp2))
    E.add_constraint(c3Atp1 >> ~(c3Atp2 | c3Atp3))
    E.add_constraint(c3Atp2 >> ~(c3Atp1 | c3Atp3))
    E.add_constraint(c3Atp3 >> ~(c3Atp1 | c3Atp2))

    # every position has at least one coin
    E.add_constraint(c1Atp1 | c2Atp1 | c3Atp1)
    E.add_constraint(c1Atp2 | c2Atp2 | c3Atp2)
    E.add_constraint(c1Atp3 | c2Atp3 | c3Atp3)

    # every position has at most one coin
    E.add_constraint(c1Atp1 >> ~(c2Atp1 | c3Atp1))
    E.add_constraint(c2Atp1 >> ~(c1Atp1 | c3Atp1))
    E.add_constraint(c3Atp1 >> ~(c1Atp1 | c2Atp1))
    E.add_constraint(c1Atp2 >> ~(c2Atp2 | c3Atp2))
    E.add_constraint(c2Atp2 >> ~(c1Atp2 | c3Atp2))
    E.add_constraint(c3Atp2 >> ~(c1Atp2 | c2Atp2))
    E.add_constraint(c1Atp3 >> ~(c2Atp3 | c3Atp3))
    E.add_constraint(c2Atp3 >> ~(c1Atp3 | c3Atp3))
    E.add_constraint(c3Atp3 >> ~(c1Atp3 | c2Atp3))

    return E


if __name__ == "__main__":

    E = add_coinComparison_constraints()
    E = add_coinOrdering_constraints()

    # Don't compile until you're finished adding all your constraints!
    T = E.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print(" #solutions: %d" % count_solutions(T))
    soln = T.solve()
    # print("   Pretty print of theory:")
    # E.pprint(T, soln)
    # print("\n   Using 'print_theory':")
    # T.print_theory()
    print("   Solution: %s" % soln)
    order = {}
    for k in soln:
        if 'Ord' in str(k) and soln[k]:
            print(k)
            order[str(k)[5]] = str(k)[8]
    
    for i in ['1','2','3']:
        print(f'pos {i}: coin {order[i][0]}')

    print("\nVariable likelihoods:")
    for v,vn in zip([c1Atp1,c1Atp2,c1Atp3,c2Atp1,c2Atp2,c2Atp3,c3Atp1,c3Atp2,c3Atp3], ["c1@p1","c1@p2","c1@p3","c2@p1","c2@p2","c2@p3","c3@p1","c3@p2","c3@p3"]):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
#        print(" %s: %s" % (vn, v))

    print("\nNegating theory:")
    T = T.negate()
    print("\nNegation satisfiable: %s" % T.satisfiable())
