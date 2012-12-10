from agent import Agent
from numpy import identity, dot, where
from random import choice, random, randint

class RLSSarsaAgent(Agent):
    """ Agent that learns on continuous or infinite state space
        using recursive least squares SARSA(lambda)
        [see Chen, Wei, 2008]
        [http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4667071&tag=1]
    """
    
    def __init__(self, stateDim, stateOffset, actionDesc,
        gamma = 0.99, slambda = 0.9, epsilon = 0.01, decay = 0.99):
        super(RLSSarsaAgent, self).__init__()
        self.stateDim = stateDim
        self.stateOffset = stateOffset
        self.actionNum = actionDesc # let's just assume this is an int for now
        self.alpha = alpha
        self.gamma = gamma
        self.slambda = slambda
        self.epsilon = epsilon
        self.decay = decay
        
        # init for rls-sarsa
        self.porder = 2
        self.featureNum = (self.stateDim + self.actionDim) * (self.porder + 1)
        self.delta = 1
        self.bmat = identity(self.featureNum) * self.delta
        self.bvec = zeros((self.featureNum, 1))
        self.weights = zeros((self.featureNum,1))
        self.epsilon = zeros((self.featureNum,1))
        
        self.nextAction = None
    
    def choose_action(self, env, obs):
        """ Evaluate function using current weights for all actions
            Pick max to find next action
        """
        obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
        i = self.nextAction
        if i is None:
            if random() > self.epsilon:
                # choose greedily
                outputs = []
        
                # loop over actions and find estimated Q value for each paired with obs
                for i in range(0, self.actionNum, 1):
                    feat = self.poly_basis(obs+tuple(i))
                    estQ = dot(self.weights.transpose(), feat)
                    outputs.append(estQ)
        
                # find the max action
                # if multiple exist pick randomly
                maxobj = max(outputs)
                i = choice([i for i, v in enumerate(outputs) if v == maxobj])
            else:
                # choose randomly
                i = array(tuple(randint(0, self.actionNum)))
        
        # cleanup
        self.nextAction = None
        self.epsilon *= self.decay
        
        return i
    
    def feedback(self, obs, a, r, nextobs, nexta = None):
        """ Update epsilon, B, b, and weights
        """
        if nexta == None:
            nexta = self.choose_action(None, nextobs)
            self.nextAction = nexta
        
        obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
        a = tuple(a)
        nextobs = nextobs[self.stateOffset:(self.stateOffset+self.stateDim)]
        nexta = tuple(nexta)
        
        # convert feedback to feature vector
        feat = self.poly_basis(obs+a)
        nextfeat = self.poly_basis(nextobs+nexta)
        
        # update epsilon
        self.epsilon = self.slambda * self.gamma * self.epsilon + feat
        
        # update b mat
        # start by computing common components
        lastb = feat - self.gamma * nextfeat
        lastb = lastb.transpose()
        lastb = dot(lastb, self.bmat)
        # numerator
        numerator = dot(self.bmat, dot(self.epsilon, lastb))
        denominator = 1 + dot(lastb,e)
        self.bmat = self.bmat - (numerator / denominator)
        
        # update b vec
        self.bvec = self.bvec + r * self.epsilon
        
        # find weights
        self.weights = dot(self.bmat, self.bvec)
    
    def poly_basis(self, vec):
        """ convert observations to polynomial basis of degree self.featureNum
        """
        vec = array(vec)
        feat = zeros((self.featureNum,1))
        for i in range(0, self.porder, 1):
            if i is 0:
                feat[:self.stateDim] = 1 # constant term is easy to compute
            else:
                feat[(i*self.stateDim):((i+1)*self.stateDim)] = vec ** i
        
        return feat