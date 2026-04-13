import random
import time
from typing import Optional

from kuimaze2 import Action, RLProblem, State
from kuimaze2.typing import Policy, QTable, VTable

T_MAX = 300 # Max steps in episode, when
DEBUG = False # if running in debug mode,
              # renders window after every step
TIMEOUT = 19.5 # time limit for learning q_vals

class RLAgent:
    """Implementation of Q-learning algorithm."""

    def __init__(
        self,
        env: RLProblem,
        gamma: float = 0.9,
        alpha: float = 0.1,
    ):
        self.env = env
        self.gamma = gamma
        self.alpha = alpha
        self.init_q_table()
        self.init_act_ctr_table()
        self.start_time = time.time()

    def init_q_table(self) -> None:
        """Create and initialize the q-table

        It is initialized as a dictionary of dictionaries;
        it can be used as 'self.q_table[state][action]'.
        """
        self.q_table = {
            state: {action: 0.0 for action in self.env.get_action_space()}
            for state in self.env.get_states()
        }        

    def init_act_ctr_table(self) -> None:
        """Create and init dict of dicts storing numer of times
        action has been selected"""
        
        self.act_ctr_table = {
            state: {action: 0 for action in self.env.get_action_space()}
            for state in self.env.get_states()
        }  

    def get_values(self) -> VTable:
        """Return the state values derived from the q-table"""
        return {
            state: max(q_values.values()) for state, q_values in self.q_table.items()
        }

    def get_max_q_value(self, state: State):
        """Return highest q-value of given state"""
        if state == None: return 0
        return max(self.q_table[state].values())
    
    def choose_action(self, state: State) -> Action:
        """Return least-explored action of given state"""
        
        if state == None: action = self.env.get_action_space()[0]
        else: action = min(self.act_ctr_table[state], key=self.act_ctr_table[state].get)
        self.act_ctr_table[state][action] += 1
        return action

    def render(
        self,
        current_state: Optional[State] = None,
        action: Optional[Action] = None,
        values: Optional[VTable] = None,
        q_values: Optional[QTable] = None,
        policy: Optional[Policy] = None,
        *args,
        **kwargs,
    ) -> None:
        """Visualize the state of the algorithm"""
        values = values or self.get_values()
        q_values = q_values or self.q_table
        # State values will be displayed in the squares
        sq_texts = (
            {state: f"{value:.2f}" for state, value in values.items()} if values else {}
        )
        # State-action value will be displayed in the triangles
        tr_texts = {
            (state, action): f"{value:.2f}"
            for state, action_values in q_values.items()
            for action, value in action_values.items()
        }
        # If policy is given, it will be displayed in the middle
        # of the squares in the "triangular" view
        actions = {}
        if policy:
            actions = {state: str(action) for state, action in policy.items()}
        # The current state and chosen action will be displayed as an arrow
        state_action = (current_state, action)
        if current_state is None or action is None:
            state_action = None
        self.env.render(
            *args,
            square_texts=sq_texts,
            square_colors=values,
            triangle_texts=tr_texts,
            triangle_colors=q_values,
            middle_texts=actions,
            state_action_arrow=state_action,
            wait=True,
            **kwargs,
        )

    def extract_policy(self) -> Policy:
        """Extract policy from Q-values"""
        policy = {
            state: max(action_values, key=action_values.get)
            for state, action_values in self.q_table.items()
        }
        return policy

    def learn_policy(self) -> Policy:
        """Run Q-learning algoritm to learn a policy"""

        # Print a table header
        print(
            f"{'State':^9}{'Action':^9}{'Next state':^11}{'Reward':>9}"
            f"{'Old Q':>9}{'Trial':>9}{'New Q':>9}",
        )
        ctr = 0
        elapsed_time = 0
        if DEBUG:
            for i in range(300):
                self.run_episode
        else:
            while(elapsed_time < TIMEOUT ):
                elapsed_time = time.time() - self.start_time
                print(elapsed_time)
                self.run_episode()
                ctr += 1
        print("episodes: ", ctr)
        return self.extract_policy()

    def run_episode(self):
        t = 0 # num of steps taken
        episode_finished = False
        next_state = self.env.reset(random_start=True) # reset and get starting state
        path = [next_state] # var for tracking traveled route
        while not episode_finished and t < T_MAX:
            t += 1
            state = next_state
            action = self.choose_action(state)
            if DEBUG: print("DEBUG: chosen action: ",action, " count", self.act_ctr_table[state].items())
            next_state, reward, episode_finished = self.env.step(action)
            if next_state is not None:
                path.append(next_state)

            # Remember the old q-value for printing it in the table
            old_q = self.q_table[state][action]
            sample = reward + self.gamma * self.get_max_q_value(next_state)
            
            self.q_table[state][action] = old_q + self.alpha * (sample - old_q)         
        
            if DEBUG:
                print(
                f"{str(state):^9}{str(action):^9}{str(next_state):^9}{reward:>9.2f}"
                f"{old_q:>9.2f}{sample:>9.2f}{self.q_table[state][action]:>9.2f}"
                ) 
                policy = self.extract_policy()
                self.render(current_state=state, action=action, path=path, policy=policy)

                if episode_finished:
                    print(f"Episode finished in a terminal state after {t} steps.")
                else:
                    print("Episode did not reach any terminal state. Maximum time horizon reached!")

if __name__ == "__main__":
    from kuimaze2 import Map
    from kuimaze2.map_image import map_from_image

    MAP = """
    ...G
    .#.D
    S...
    """
    #map = Map.from_string(MAP)
    map = map_from_image("./maps/normal/normal11.png")
    env = RLProblem(
        map,
        action_probs=dict(forward=0.8, left=0.1, right=0.1, backward=0.0),
        graphics=True,
    )

    agent = RLAgent(env, gamma=0.9, alpha=0.1)
    policy = agent.learn_policy()
    print("Policy found:", policy)
    agent.render(policy=policy, use_keyboard=True)
    input()
