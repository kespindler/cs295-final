from numpy import cos, pi
from agent import Agent
from numpy import array, zeros, dot
from numpy.random import rand
from random import choice, random, randint

class GradientDescentSarsaAgent(Agent):
    """ Sarsa(lambda) using gradient descent (function approximation)
    """
    def __init__(self, stateDim, stateOffset, actionDesc,
                alpha = 0.0000001, gamma = 0.99, slambda = 0, epsilon = 0.5, decay = 0.995, traceThreshold = 0.0001):
        super(GradientDescentSarsaAgent, self).__init__()
        print(alpha)
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
        self.porder = 5
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
                i = self.get_greedy_action(o)
                
            else:
                # choose randomly
                i = array((randint(0,self.actionNum-1),))
        
        # cleanup
        self.nextAction = None
        self.epsilon *= self.decay
        
        return i
    
    def get_greedy_action(self,o):
        # choose greedily
        outputs = []
        
        # loop over actions and find estimated Q value for each paired with obs
        for j in range(0, self.actionNum, 1):
            feat = self.fourier_basis(o)
            estQ = dot(self.weights[j], feat)
            outputs.append(estQ)
                
        print(outputs)
        
        # find the max action
        # if multiple exist pick randomly
        maxobj = max(outputs)
        i = choice([i for i, v in enumerate(outputs) if v == maxobj])
        i = array([i,])
        
        return i
    
    def feedback(self, obs, a, r, nextobs, nexta = None, env=None):
        obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
        a = a[0]
        nextobs = nextobs[self.stateOffset:(self.stateOffset+self.stateDim)]
        if nexta == None:
            nexta = self.get_greedy_action(nextobs)

        nexta = nexta[0]
        
        feat = self.fourier_basis(obs)
        nextfeat = self.fourier_basis(nextobs)
        aweights = self.weights[a]
        nextaweights = self.weights[nexta]
        q = dot(aweights, feat)
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
    
    def fourier_basis(self, obs):
        """ Fourier basis, hardcoded to order 3 for now
        """
        vec = array(obs)
        vec = vec * pi
        vec = array([[cos(v), cos(2*v), cos(3*v), cos(4*v), cos(5*v)] for v in vec])
        feat = zeros((self.featureNum))
        feat[0] = 1
        for i in range(0,self.stateDim):
            feat[self.porder*i+1:self.porder*(i+1)+1] = vec[i]
            
        return feat
    
    def full_fourier_basis(self, obs):
        
        
        feat = zeros((self.featureNum))
        return feat
    
    def full_fourier_coef(self):
        nterms = (order+1)**self.stateDims
        mult = zeros((nterms, self.stateDims))
        return
