from agent import Agent
from numpy import array, zeros, identity, dot, where
from random import choice, random, randint
from sklearn import linear_model

class NaiveLinApproxAgent(Agent):
	""" Homebrewed linear approximator
        Probably won't work...
    """

	def __init__(self, stateDim, stateOffset, actionDesc,
				alpha = 0.1, gamma = 0.99, slambda = 0.9, epsilon = 0.01, decay = 0.99, traceThreshold = 0.0001):
		super(NaiveLinApproxAgent, self).__init__()
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
		self.featureNum = self.stateDim * (self.porder + 1)
		self.histories = []
		self.approxers = []
		for i in range(0, self.actionNum):
			self.histories.append([])
			self.approxers.append(linear_model.LinearRegression())
		
		self.nextAction = None
		self.initq = 1.

	def choose_action(self, env, obs):
		obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
		feat = self.poly_basis(obs).transpose()
		i = self.nextAction
		if i is None:
			if random() > self.epsilon:
				# greedy
				outputs = []
				
				for j in range(0, self.actionNum):
					currApprox = self.approxers[j]
					if hasattr(currApprox, 'coef_'):
						est = currApprox.predict(feat)
						outputs.append(est[0])
					else:
						outputs.append(self.initq)
                
				maxobj = max(outputs)
				i = choice([i for i, v in enumerate(outputs) if v == maxobj])
				i = array([i,])
            
			else:
				# choose randomly
				i = array((randint(0,self.actionNum),))

		# cleanup
		self.nextAction = None
		self.epsilon *= self.decay
		super(NaiveLinApproxAgent, self).choose_action(env, obs)
		
		return i

	def feedback(self, obs, a, r, nextobs, nexta = None):
		if nexta == None:
			nexta = self.choose_action(None, nextobs)
			self.nextAction = nexta

		obs = obs[self.stateOffset:(self.stateOffset+self.stateDim)]
		a = a[0]
		nextobs = nextobs[self.stateOffset:(self.stateOffset+self.stateDim)]
		nexta = nexta[0]

		currHistory = self.histories[a]
		qhist = zeros((len(currHistory)+1,1))
		nextHistory = self.histories[nexta]
		currApprox = self.approxers[a]
		nextApprox = self.approxers[nexta]

		feat = self.poly_basis(obs).transpose()
		currHistory.append(feat[0])
		nextfeat = self.poly_basis(obs).transpose()
		
		q = self.initq
		nextq = self.initq
		if hasattr(currApprox, 'coef_'):
			q = currApprox.predict(feat)
		if hasattr(nextApprox, 'coef_'):
			nextq = nextApprox.predict(nextfeat)
		
		delta = r + self.gamma * nextq - q
		newq = q + self.alpha * delta
		qhist[len(qhist)-1,0] = newq
		
		eligibility = self.slambda
		for i in range(len(qhist)-2, -1, -1):
			backupfeat = currHistory[i]
			backupq = currApprox.predict(backupfeat)
			# backupq = backupq + self.alpha * delta * eligibility
			qhist[i,0] = backupq
			eligibility *= self.slambda
		
		currApprox.fit(array(currHistory), qhist)
		# do I need to go in and change other histories? this is gonna backup only runs in same action!!!

	def poly_basis(self, vec):
		""" convert observations to polynomial basis of degree self.featureNum
		"""
		vec = array([[v] for v in vec])
		feat = zeros((self.featureNum,1))
		featSize = self.stateDim
		for i in range(0, self.porder+1, 1):
			if i is 0:
				feat[:featSize] = 1 # constant term is easy to compute
			else:
				feat[(i*featSize):((i+1)*featSize)] = vec ** i

		return feat