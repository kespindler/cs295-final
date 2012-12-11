from agent import Agent
from numpy import array, zeros, identity, dot, where
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
        self.gamma = gamma
        self.slambda = slambda
        self.epsilon = epsilon
        self.decay = decay
        
        # init for rls-sarsa
        self.porder = 10
        self.actionFeatures = self.stateDim * self.porder
        self.featureNum = self.actionFeatures * self.actionNum + 1
        self.delta = 0.0001
        
        self.bmat = identity(self.featureNum) * self.delta
        self.bvec = zeros((self.featureNum, 1))
        self.weights = zeros((self.featureNum,1))
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
        """ Update epsilon, B, b, and weights
        """
        if nexta == None:
            nexta = self.choose_action(None, nextobs)
            self.nextAction = nexta
        
        obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
        a = a[0]
        nextobs = nextobs[self.stateOffset:(self.stateOffset+self.stateDim)]
        nexta = nexta[0]
        
        # convert feedback to feature vector
        feat = self.poly_basis(obs,a)
        nextfeat = self.poly_basis(nextobs,nexta)
        
        # update eligibility
        self.eligibility = self.slambda * self.gamma * self.eligibility + feat
        
        # update b mat
        # start by computing common components
        lastb = feat - self.gamma * nextfeat
        lastb = lastb.transpose()
        lastb = dot(lastb, self.bmat)
        # numerator
        numerator = dot(self.bmat, dot(self.eligibility, lastb))
        denominator = 1 + dot(lastb,self.eligibility)
        self.bmat = self.bmat - (numerator / denominator)
        
        # update b vec
        self.bvec = self.bvec + r * self.eligibility
        
        # update weights
        self.weights = dot(self.bmat, self.bvec)
    
    def poly_basis(self, obs, a):
        vec = array([[v] for v in obs])
        feat = zeros((self.featureNum,1))
        feat[0] = 1 # constant term
        featSize = self.stateDim
        actionOffset = self.actionFeatures * a + 1
        for i in range(1,self.porder+1):
            feat[((i-1)*featSize+actionOffset):(i*featSize+actionOffset)] = vec ** i
		
        return feat
    
    def episode_finished(self):
        print("EPISODE FINISHED: STEPS: " + str(self.stepCount))
        super(RLSSarsaAgent, self).episode_finished()
        self.eligibility = zeros((self.featureNum,1))
