from domains.pancake import Pancake
from solver.ida_star import IDAStar


def heuristic_value_pancake(state):
    return 0

p = Pancake([4, 5, 6, 1, 2, 3])
ida = IDAStar()
cost = ida.search(p, heuristic_value_pancake)
print('Cost: ', cost)