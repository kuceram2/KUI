import random
from kuimaze2 import SearchProblem, Map, State


class Node:
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent

class Agent:
    """Simple example of a random agent."""

    def __init__(self, environment: SearchProblem):
        self.environment = environment

    def find_path(self) -> list[State]:
        #print("find path")
        path = []
        start_state = self.environment.get_start()
        costs = {start_state: 0.0} # do tohohle stavu se dostaneme za 0, je počáteční
        queue = [Node(start_state, None)]
        known_states = {start_state: True}
        #print(f"start: {start_state}")

        while len(queue) > 0:
            node = queue.pop(0)
            state = node.state
            if self.environment.is_goal(state):
                #print("creating path")
                path = self.create_path(node)
                self.environment.render(path=path, wait=True, use_keyboard=True)
                return path

            actions = self.environment.get_actions(state)
            #print(actions)
            for action in actions:
                new_state, cost = self.environment.get_transition_result(state, action)
                #print(new_state)
                if not new_state in known_states:
                    known_states[new_state] = True
                    costs[new_state] = costs[state] + cost
                    queue.append(Node(new_state, node))
                    
                    if self.environment.is_goal(new_state):
                        path = self.create_path(queue.pop())
                        self.environment.render(path=path, wait=True, use_keyboard=True)
                        return path
                    #print(len(queue))

                    self.environment.render(
                    current_state=state,
                    next_states=[new_state],
                    texts=costs,
                    colors=costs,
                    wait=True,)
                
        

    def create_path(self, node):
        current_node = node
        #print(node)
        path = []
        while current_node != None:
            #print("a")
            path.append(current_node.state)
            current_node = current_node.parent
        return path[::-1]

if __name__ == "__main__":
    # Create a Map instance
    MAP = """
    ..#..#.#
    .S.....#
    #.##....
    ...#G...
    ......#.
    """
    map = Map.from_string(MAP)
    # Create an environment as a SearchProblem initialized with the map
    env = SearchProblem(map, graphics=True)
    # Create the agent and find the path
    agent = Agent(env)
    path = agent.find_path()
    print(path)