from .local_search import LocalSearch
from .iterated_greedy import IteratedGreedy
from .initializer import Initializer

class Instance(Initializer, IteratedGreedy, LocalSearch):
    pass