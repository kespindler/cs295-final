from agent import SarsaAgent
from gradient_descent import GradientDescentSarsaAgent
from random import random
from utility import enum
from agent_options import KeyCOption, LockCOption, DoorCOption
from options import ActionOption, KeyOption, LockOption, DoorOption
from numpy import array

class PCOptionAgent(SarsaAgent):
    """ Combines problem space / action space
    """
    
    def __init__(self, stateDesc, agentStateOffset, actionDesc):
        agentStateDim = len(stateDesc - agentStateOffset)
        self.options = [
            KeyCOption(stateDim, agentStateOffset, actionDesc),
            LockCOption(stateDim, agentStateOffset, actionDesc),
            DoorCOption(stateDim, agentStateOffset, actionDesc),
            KeyOption(stateDesc, actionDesc),
            LockOption(stateDesc, actionDesc),
            DoorOption