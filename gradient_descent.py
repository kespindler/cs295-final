from agent import Agent
from numpy import array, zeros, dot
from numpy.random import rand
from random import choice, random, randint

class GradientDescentSarsaAgent(Agent):
    """ Sarsa(lambda) using gradient descent (function approximation)
    """
    
    def __init__(self, stateDim, stateOffset, actionDesc,
                alpha = 0.01, gamma = 0.99, slambda = 0.9, epsilon = 0.01, decay = 0.99, traceThreshold = 0.0001):
        super(GradientDescentSarsaAgent, self).__init__()
        self.stateDim = stateDim
        self.stateOffset = stateOffset
        self.actionNum = actionDesc[0] # let's just assume this is an int for now
        self.alpha = alpha
        self.gamma = gamma
        self.slambda = slambda
        self.epsilon = epsilon
        self.decay = decay
        self.traceThreshold = traceThreshold
        
        # init for FA
        self.porder = 1
        self.featureNum = self.stateDim * self.porder + 1
        self.delta = 0.0001
        
        init = 1
        self.weights = zeros((self.actionNum,self.featureNum))
        self.weights[:,0] = init
        self.eligibility = zeros((self.actionNum,self.featureNum))
        
        self.nextAction = None
    
    def choose_action(self, env, obs):
        """ Evaluate function using current weights for all actions
            Pick max to find next action
        """
        o = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
        i = self.nextAction
        if i is None:
            if random() > self.epsilon:
                # choose greedily
                outputs = []
        
                # loop over actions and find estimated Q value for each paired with obs
                for j in range(0, self.actionNum, 1):
                    feat = self.poly_basis(o)
                    estQ = dot(self.weights[j], feat)
                    outputs.append(estQ)
                
                #print(outputs)
        
                # find the max action
                # if multiple exist pick randomly
                maxobj = max(outputs)
                i = choice([i for i, v in enumerate(outputs) if v == maxobj])
                i = array([i,])
                
            else:
                # choose randomly
                i = array((randint(0,self.actionNum),))
        
        # cleanup
        self.nextAction = None
        self.epsilon *= self.decay
        
        print(i)
        return i
    
    def feedback(self, obs, a, r, nextobs, nexta = None):
        if nexta == None:
            nexta = self.choose_action(None, nextobs)
            self.nextAction = nexta
        
        obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
        a = a[0]
        nextobs = nextobs[self.stateOffset:(self.stateOffset+self.stateDim)]
        nexta = nexta[0]
        
        feat = self.poly_basis(obs)
        aweights = self.weights[a]
        nextaweights = self.weights[nexta]
        q = dot(aweights, feat)
        nextfeat = self.poly_basis(nextobs)
        nextq = dot(nextaweights, nextfeat)
        
        delta = r + self.gamma * nextq - q
        self.eligibility *= self.gamma * self.slambda # decay over all traces!
        self.eligibility[a] += feat
        self.weights += self.alpha * delta * self.eligibility
        
        return
    
    def poly_basis(self, obs):
        vec = array([v for v in obs])
        feat = zeros((self.featureNum))
        feat[0] = 1 # constant term
        featSize = self.stateDim
        for i in range(1,self.porder+1):
            feat[((i-1)*featSize+1):(i*featSize)+1] = vec ** i
        
        return feat