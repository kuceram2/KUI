import math
#from queue import PriorityQueue
import heapq as hq
from kuimaze2 import SearchProblem, Map, State
from kuimaze2.map_image import map_from_image



class Node:
    def __init__(self, state, parent, cost, priority):
        # cost = cost of travel to the node, priority = cost + heuristics
        self.state = state
        self.parent = parent
        self.cost:float  = cost
        self.priority:float = priority
    
    def __lt__(self, other):
        return self.priority < other.priority

class Agent:
    """Simple example of a random agent."""

    def __init__(self, environment: SearchProblem):
        self.environment = environment

    def find_path(self) -> list[State]:
        #print("find path")
        path = []
        start_state = self.environment.get_start()
        costs = {start_state: 0.0,} # cena cesty, cena+heuristika
        heuristics = {}
        #queue = PriorityQueue(maxsize=100)
        queue = []
        first_node = Node(start_state, None, 0, 0)
        hq.heappush(queue, (0,first_node ))
        known_states = {start_state: first_node}
        #print(f"start: {start_state}")


        while len(queue) > 0:
            item = hq.heappop(queue)
            node = item[1]
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
                
                node_cost = float(costs[state] + cost)
                is_cheaper = False


                if new_state in known_states: # pokud už je stav známý
                    loaded_node = known_states[new_state]
                    if(node_cost < loaded_node.cost): # pokud jsme se tam dostali levněji než předtím
                        #print("updating node cost")
                        is_cheaper =True



                if (not new_state in known_states) or is_cheaper:
                    # known_states[new_state] = True
                    #print(known_states)
                    node_heuristic = self.get_heuristics(new_state)
                    node_priority = round(node_cost + node_heuristic, 2)
                    costs[new_state] = node_cost
                    heuristics[new_state] = "c: " + str(node_cost) + "\nh: " + str(node_heuristic) + "\np: " + str(node_priority)
                    
                    new_node = Node(new_state, node, node_cost, node_priority)
                    known_states[new_state] = new_node
                    hq.heappush(queue, (node_priority, new_node))
                    
            self.environment.render(
            current_state=state,
            next_states=[new_state],
            texts=heuristics,
            colors=costs,
            wait=True,)
                
    def get_heuristics(self, state):
        goals = self.environment.get_goals()
        #print(goals[0][0], goals[0][1])
        shortest_dist = math.inf
        for goal in goals:
            #dist = self.get_eucul_dist_from_goal(state, goal)
            dist = self.get_mann_dist_from_goal(state, goal)
            if(dist < shortest_dist): shortest_dist = dist
        return round(shortest_dist, 2)

    def get_eucul_dist_from_goal(self, state, goal):
        # returns euculidian distance between nodes
        x_dist = abs(state[0] - goal[0])
        y_dist = abs(state[1] - goal[1])
        dist = math.sqrt(x_dist**2 + y_dist**2)
        return dist*2
    
    def get_mann_dist_from_goal(self, state, goal):
        x_dist = abs(state[0] - goal[0])
        y_dist = abs(state[1] - goal[1])
        return x_dist + y_dist

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
    G........S............
    ......................
    ......................
    ......................
    ......................
    .....................
    ......................
    ......................
    ......................
    G.....................
    ......................
    .....................G
    """
    dMAP = """
    G...S...
    ........
    ........
    .......G
    """

    #map = Map.from_string(MAP)
    map = map_from_image("./maps/normal/normal10.png")
    # Create an environment as a SearchProblem initialized with the map
    env = SearchProblem(map, graphics=True)
    # Create the agent and find the path
    agent = Agent(env)
    path = agent.find_path()
    print(path)