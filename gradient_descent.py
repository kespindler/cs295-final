from agent import Agent
from numpy import array, zeros, dot
from numpy.random import rand
from random import choice, random, randint

class GradientDescentSarsaAgent(Agent):
    """ Sarsa(lambda) using gradient descent (function approximation)
    """
    
    def __init__(self, stateDim, stateOffset, actionDesc,
                alpha = 0.1, gamma = 0.99, slambda = 0.9, epsilon = 0.01, decay = 0.99, traceThreshold = 0.0001):
        super(GradientDescentSarsaAgent, self).__init__()
        self.stateDim = stateDim
        self.stateOffset = stateOffset
        self.actionNum = actionDesc # let's just assume this is an int for now
        self.alpha = alpha
        self.gamma = gamma
        self.slambda = slambda
        self.epsilon = epsilon
        self.decay = decay
        self.traceThreshold = traceThreshold
        
        # init for FA
        self.porder = 1
        self.actionFeatures = self.stateDim * self.porder
        self.featureNum = self.actionFeatures * self.actionNum + 1
        self.delta = 0.0001
        
        self.weights = zeros((self.featureNum,1))
        self.weights[0] = 1
        self.eligibility = zeros((self.featureNum,1))
        
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
                for j in range(0, self.actionNum, 1):
                    feat = self.poly_basis(obs,j)
                    estQ = dot(self.weights.transpose(), feat)[0][0]
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
    
    def feedback(self, obs, a, r, nextobs, nexta = None, env=None):
        if nexta == None:
            nexta = self.choose_action(None, nextobs)
            self.nextAction = nexta
        
        obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
        a = a[0]
        nextobs = nextobs[self.stateOffset:(self.stateOffset+self.stateDim)]
        nexta = nexta[0]
        
        feat = self.poly_basis(obs,a)
        q = dot(self.weights.transpose(), feat)
        nextfeat = self.poly_basis(nextobs,nexta)
        nextq = dot(self.weights.transpose(), nextfeat)
        
        delta = r + self.gamma * nextq - q
        self.eligibility *= self.gamma * self.slambda
        self.eligibility += feat
        self.weights += self.alpha * delta * self.eligibility
        
        return
    
    def poly_basis(self, obs, a):
        vec = array([[v] for v in obs])
        feat = zeros((self.featureNum,1))
        feat[0] = 1 # constant term
        featSize = self.stateDim
        actionOffset = self.actionFeatures * a + 1
        for i in range(1,self.porder+1):
            feat[((i-1)*featSize+actionOffset):(i*featSize+actionOffset)] = vec ** i
        
        return feat
