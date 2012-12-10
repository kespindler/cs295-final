from agent import Agent

class RLSSarsaAgent(Agent):
    """ Agent that learns on continuous or infinite state space
        using recursive least squares SARSA(lambda)
        [see Chen, Wei, 2008]
        [http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4667071&tag=1]
    """
    
    def __init__(self, statedim, actiondim,
                alpha = 0.1, gamma = 0.99, slambda = 0.9, epsilon = 0.01)

class RLSSarsa(object):
    """ Implementation of Recursive Least Sqaures Sarsa(lambda) from 
    """
    