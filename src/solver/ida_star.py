from domains.pancake import Pancake


class Node:
    def __init__(self, state, g, h, parent_action):
        self._state = state
        self._parent_action = parent_action
        self._g = g
        self._h = h
        self._f = g + h

class IDAStar:

    def dfs(self, node, bound):
        if node._f > bound:
            if self._next_bound is None or node._f < self._next_bound:
                self._next_bound = node._f

            return False, None
        
        self._nodes_expanded += 1
        actions = node._state.get_actions(node._parent_action)
        for a in actions:
            child = node._state.copy()
            child.apply_action(a)

            if child.is_goal():
                return True, node._g + 1

            child_node = Node(child, node._g + 1, self._h_function(child), a)

            has_solved, cost = self.dfs(child_node, bound)

            if has_solved:
                return has_solved, cost
        return False, None
        

    def search(self, start, h_function):
        bound = h_function(start)
        node_start = Node(start, 0, 0, None)
        self._h_function = h_function
        
        self._nodes_expanded = 0

        has_solved = False
        print('Bound: ', bound, end=' ')
        while not has_solved:
            self._next_bound = None
            has_solved, cost = self.dfs(node_start, bound)
            print('Expanded: ', self._nodes_expanded)
            bound = self._next_bound
            print('Bound: ', bound, end=' ')

        return cost