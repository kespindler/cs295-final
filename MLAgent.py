from agent import Agent
from numpy import identity

class RLSSarsaAgent(Agent):
    """ Agent that learns on continuous or infinite state space
        using recursive least squares SARSA(lambda)
        [see Chen, Wei, 2008]
        [http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4667071&tag=1]
    """
    
    
    def __init__(self, stateDim, stateOffset, actionDesc,
                alpha = 0.1, gamma = 0.99, slambda = 0.9, epsilon = 0.01):
        super(RLSSarsaAgent, self).__init__()
        self.stateDim = stateDim
        self.stateOffset = stateOffset
        self.actionDesc = actionDesc
        self.actionDim = len(actionDesc)
        self.alpha = alpha
        self.gamma = gamma
        self.slambda = slambda
        self.epsilon = epsilon
        
        # init for rls-sarsa
        self.porder = 2
        self.featureNum = (self.stateDim + self.actionDim) * (self.porder + 1)
        self.delta = 1
        self.bmat = identity(self.featureNum) * self.delta
        self.bvec = zeros((self.featureNum, 1))
        self.weights = zeros((self.featureNum,1))
        self.epsilon = 0
        
        self.nextAction = None
    
    def choose_action(self, env, obs):
        """ Evaluate function using current weights for all actions
            Pick max
        """
        # TODO
    
    def feedback(self, obs, a, r, nextobs, nexta = None):
        """ Update epsilon, B, b, and weights
        """
        if nexta == None:
            nexta = self.choose_action(None, nextobs)
            self.nextAction = nexta
        
        obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]