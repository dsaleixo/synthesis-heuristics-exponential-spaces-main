import numpy as np

class Pancake:
    def __init__(self, permutation):
        self._permutation = np.array(permutation)
    
    def get_actions(self, parent=None):
        actions = list(np.arange(0, len(self._permutation) - 1, 1))

        if parent is not None:
            actions.remove(parent)
        
        return actions

    def apply_action(self, action):
        self._permutation[action:] = self._permutation[action:][::-1]

    def copy(self):
        return Pancake(np.copy(self._permutation))

    def is_goal(self):
        for i in range(0, len(self._permutation)):
            if i + 1 != self._permutation[i]:
                return False
        return True

# p = Pancake([1, 2, 3, 4, 5, 6])
# actions = p.get_actions()

# print(actions, p._permutation, p.is_goal())

# for a in actions:
#     child = p.copy()
#     child.apply_action(a)

#     print(child._permutation, child.is_goal())
        

    