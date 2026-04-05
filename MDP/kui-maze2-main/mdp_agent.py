#!/usr/bin/env python3

import random
import copy
from typing import Optional

from kuimaze2 import MDPProblem
from kuimaze2.typing import VTable, QTable, Policy
from kuimaze2.map_image import map_from_image

from kuimaze2.map import Action, Map, State



class MDPAgent:
    """Base class for VI and PI agents"""

    # Can be used to define common data/methods of both agents (algorithms)

    def __init__(self, env: MDPProblem, gamma: float = 0.9, epsilon: float = 0.001):
        self.env = env # enviroment
        self.gamma = gamma # discount factor
        self.epsilon = epsilon # max error
        
        self.values = {}
        self.qvalues = {}
        self.termination_req = False

        

    def render(
        self,
        values: Optional[VTable] = None,
        qvalues: Optional[QTable] = None,
        policy: Optional[Policy] = None,
        **kwargs,
    ):      
        """Render the environment with added agent's data"""
        #values = {state: -1 + 2 * random.random() for state in self.env.get_states()}
        value_texts = {state: f"{value:.2f}" for state, value in values.items()}
        
        # print("QVALUES: ", qvalues)
        qvalue_texts = {
            (state, action): f"{q:.2f}"
            for state, actions in qvalues.items()
            for action, q in actions.items()
        }
        # Prepare policy for rendering
        
        #policy_texts = {state: f"{policy[state]}" for state in self.env.get_states()}
        policy_texts = {}
        for state in self.env.get_states():
            policy_texts[state] = policy[state]
        
        #policy_texts = {state: f"X" for state in self.env.get_states()}
        self.env.render(
            square_colors=values,
            square_texts=value_texts,
            triangle_colors=qvalues,
            triangle_texts=qvalue_texts,
            middle_texts=policy_texts,
            **kwargs,
        )

    def init_values(self) -> VTable:
        """Initializes state values to 0"""
        values = {}
        for state in self.env.get_states():
            if self.env.is_terminal(state): values[state] = self.env.get_reward(state)
            else: values[state] = 0   
        
        return values

    def init_qvalues(self) -> QTable:
        """Initializes qvalues to 0"""
        qvalues = {
            state: {
                action: 0
                for action in self.env.get_actions(state)
            }
            for state in self.env.get_states()
        }
        return qvalues

    def get_qvalue(self, state: State, action: Action):
        new_states = self.env.get_next_states_and_probs(state=state, action=action)
        qval = 0
        for new_state in new_states:
            print(new_state, self.values[new_state[0]])
            qval += new_state[1] * (self.env.get_reward(state) + (self.gamma * self.values[new_state[0]]))
        return qval
            
    def get_best_action(self, state: State):
        actions = self.env.get_actions(state)
        
        for action in actions:
            #print(action)
            self.qvalues[state][action] = self.get_qvalue(state, action)
            #print(self.qvalues[state])
            best_action = max(self.qvalues[state], key=self.qvalues[state].get)
        return best_action

class ValueIterationAgent(MDPAgent):
        #return {state: 0 for state in self.env.get_non_terminal_states()}
        
    def find_policy(self) -> Policy:
        self.values = self.init_values()
        self.states = self.env.get_states()
        self.actions = self.env.get_actions(self.states[0])
        self.qvalues = self.init_qvalues()
        self.policy = {}
        
        # print("values: ",self.values)
        # print("actions: ", self.actions)

        #fabricate policy so the visualization can run
        for state in self.states:
            self.policy[state] = self.actions[1]
            
        # print("test action:", self.actions[1])
        # print("example qvalue: ", self.qvalues[self.states[0]][self.actions[0]])
        
        while not self.termination_req:
            print("=========== New round ===========")
            self.termination_req = True
            for state in self.env.get_non_terminal_states():
                self.bellman_update(state)
                self.render(values = self.values, policy=self.policy, qvalues= self.qvalues, wait= True)
        
        self.create_policy()
        
        return self.policy

    def bellman_update(self, state: State):
        
        best_action = self.get_best_action(state)
        new_value = self.qvalues[state][best_action]
        if not self.tuning_done(self.values[state], new_value): self.termination_req = False 
        self.values[state] = new_value
        print("MAX: ",self.values[state])
                      
    def tuning_done(self, old_val, new_val):
        if (abs(old_val - new_val) <= (self.epsilon*(1 - self.gamma)/self.gamma)):
            print("Reqired precision reached")
            return True
        else: 
            print("---------Big improvement")
            return False
   
    def create_policy(self):
        for state in self.env.get_non_terminal_states():
            self.policy[state] = max(self.qvalues[state], key=self.qvalues[state].get)



class PolicyIterationAgent(MDPAgent):

    def init_policy(self) -> Policy:
        """Create a random policy"""
        return {
            state: random.choice(self.env.get_actions(state))
            for state in self.env.get_states()
        }

    #returns found policy as a dictionary: (state, action)
    def find_policy(self) -> Policy:
        self.values = self.init_values()
        self.policy = self.init_policy()
        self.qvalues = self.init_qvalues()
        self.new_policy = self.init_policy()
        
        while not self.termination_req:
            self.termination_req = True
            self.eval_policy(self.policy)
            self.render(values = self.values, qvalues=self.qvalues, policy=self.policy, wait= True)
            self.imporve_policy()
            self.render(values = self.values, qvalues=self.qvalues, policy=self.policy, wait= True)

        return self.policy


    def eval_policy(self, policy: Policy):
        for state in self.env.get_non_terminal_states():
            action = policy[state]
            self.values[state] = self.get_qvalue(state, action)
            print(f"value of {state} updated: { self.values[state]} ")
            
    def imporve_policy(self):
        for state in self.env.get_non_terminal_states():
            self.new_policy[state] = self.get_best_action(state)
        if not self.policy_unchanged(): self.termination_req = False
        
    def policy_unchanged(self):
        for key in self.policy:
            if self.policy[key] != self.new_policy[key]:
                self.policy = copy.deepcopy(self.new_policy)
                return False
        self.policy = copy.deepcopy(self.new_policy)
        return True
                
            
            

if __name__ == "__main__":
    from kuimaze2 import Map
    from kuimaze2.map_image import map_from_image

    MAP = """
    ..#..#.
    ...G.D.
    .#.D...
    S.D....
    ..#...D
    """
    #map = Map.from_string(MAP)
    map = map_from_image("./maps/normal/normal3.png")
    env = MDPProblem(
        map,
        action_probs=dict(forward=0.8, left=0.1, right=0.1, backward=0.0),
        graphics=True,
    )

    print(env.get_states())
    #agent = ValueIterationAgent(env, gamma=0.9, epsilon=0.001)
    agent = PolicyIterationAgent(env, gamma=0.9, epsilon=0.001)
    policy = agent.find_policy()
    print("Policy found:", policy)
    agent.render(policy=policy, values=agent.values, qvalues=agent.qvalues ,wait=True)
    input()   