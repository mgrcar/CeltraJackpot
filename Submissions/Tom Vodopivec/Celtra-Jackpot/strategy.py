#Different strategies for tackling the problem
from Config import *
import random
from math import *
from machine import *


class ensemble():
    machines = None
    numMachines = None

    pulls = None
    total_rejected_pulls = None

    #last selected policy
    lastPolicy = None
    
    # Index of last machine played POKER Stuff
    lastPulledMachine = None
    machineMeanSum = None
    machineSigmaSum = None


    def __init__(self,nMachines=2):
        self.numMachines=nMachines
        pulls=0
        self.lastPulledMachine = 0
        self.machineMeanSum = 0.0
        self.machineSigmaSum = 0.0
        self.machines = [machine(m) for m in xrange(self.numMachines)]
        self.lastPolicy=0
        self.total_rejected_pulls = 0

    #params [voter C; main UCBT C; POKER param; POKER horizon]
    def UCBTVoter(self,secondary_machines,secondary_ucbt_machines, all_pulls, rejected_pulls, params= [1.0, 1.0, 1.0]):

        actions=self.machines
        bestVal = -1e30000
        numEqualBest = 1
        indicesBest = [-1]*len(actions)

        parC=params[0]
    
        #find best action among all available
        for i in range(len(actions)) :

            a = actions[i]

            #first try all the unexplored actions (those with zero visits)
            if a.pulls <= 0 :
                indicesBest[0] = i
                break

            #if all actions already explored, calculate their values
            else :
                try:
                    #UCBvalue = a.mean + parC*sqrt(2.0*log(all_pulls)/a.pulls)   #the UCB1 equation
                    V = a.variance+sqrt(2.0*log(self.pulls)/a.pulls)
                    UCBvalue = a.mean + parC * sqrt((log(self.pulls)/a.pulls)*min(1.0/4.0,V))

                    #store calculated value
                    a.storedValue = UCBvalue

                    #find action with highest value
                    if UCBvalue > bestVal :
                        bestVal = UCBvalue
                        numEqualBest = 1
                        indicesBest[numEqualBest-1] = i

                    #remember best
                    elif UCBvalue == bestVal :
                        numEqualBest += 1
                        indicesBest[numEqualBest-1] = i

                except:
                    print 'UCBT(): lol'

        #break ties randomly
        indicesBest[0] = indicesBest[random.randint(0,numEqualBest-1)]

        selected_policy = actions[indicesBest[0]] 
        not_selected_policy = actions[1-indicesBest[0]]

        #0 - UCBT
        #1 - POKER

        secondary_machine_selection=[UCBT(secondary_ucbt_machines,all_pulls,params[1]).id, POKER(secondary_machines,[self.lastPulledMachine, self.machineMeanSum, self.machineSigmaSum], params[2]).id]
        if secondary_machine_selection[0]==secondary_machine_selection[1]:
           self.lastPolicy=2
           selected_bandit=secondary_machine_selection[0]
        elif selected_policy.id==0:
             self.lastPolicy=0
             selected_bandit=secondary_machine_selection[0]
        else: 
            self.lastPolicy=1
            selected_bandit=secondary_machine_selection[1]
        
        self.lastPulledMachine=selected_bandit
        
        return secondary_machines[selected_bandit]
        
    
    def resetState(self):

        self.machines = [machine(m) for m in range(self.numMachines)]
        self.pulls = 0
        self.total_rejected_pulls = 0
        self.lastPulledMachine = 0
        self.machineMeanSum = 0.0
        self.machineSigmaSum = 0.0
        self.lastPolicy=0

    def update(self,M,reward, pull):
        if self.lastPolicy==2:
            for m in self.machines:
                m.update(reward,pull)
            #increase by two basically needs to be tested
            self.pulls+=1
        elif self.lastPolicy==0:
            self.machines[0].update(reward,pull)
        elif self.lastPolicy==1:
            self.machines[1].update(reward,pull)

            self.machineMeanSum += M[self.lastPulledMachine].mean
            self.machineSigmaSum += sqrt(M[self.lastPulledMachine].variance)
        self.pulls+=1
            







#the UCB algorithm by Auer et al., 2002
def UCB1(actions, all_pulls, parC = 1.0):

    bestVal = -1e30000
    numEqualBest = 1
    indicesBest = [-1]*len(actions)

    #find best action among all available
    for i in range(len(actions)) :

        a = actions[i]

        #first try all the unexplored actions (those with zero visits)
        if a.pulls <= 0 :
            indicesBest[0] = i
            break

        #if all actions already explored, calculate their values
        else :
            UCBvalue = a.mean + parC*sqrt(2.0*log(all_pulls)/a.pulls)   #the UCB1 equation

            #store calculated value
            a.storedValue = UCBvalue

            #find action with highest value
            if UCBvalue > bestVal :
                bestVal = UCBvalue
                numEqualBest = 1
                indicesBest[numEqualBest-1] = i

            #remember best
            elif UCBvalue == bestVal :
                numEqualBest += 1
                indicesBest[numEqualBest-1] = i

    #break ties randomly
    indicesBest[0] = indicesBest[random.randint(0,numEqualBest-1)]

    return actions[indicesBest[0]]


def UCBT(actions, all_pulls, parC = 1.0):

    bestVal = -1e30000
    numEqualBest = 1
    indicesBest = [-1]*len(actions)
    
    #find best action among all available
    for i in range(len(actions)) :

        a = actions[i]

        #first try all the unexplored actions (those with zero visits)
        if a.pulls <= 0 :
            indicesBest[0] = i
            break

        #if all actions already explored, calculate their values
        else :
            try:
                #UCBvalue = a.mean + parC*sqrt(2.0*log(all_pulls)/a.pulls)   #the UCB1 equation
                V = a.variance+sqrt(2.0*log(all_pulls)/a.pulls)
                UCBvalue = a.mean + parC * sqrt((log(all_pulls)/a.pulls)*min(1.0/4.0,V))

                #store calculated value
                a.storedValue = UCBvalue

                #find action with highest value
                if UCBvalue > bestVal :
                    bestVal = UCBvalue
                    numEqualBest = 1
                    indicesBest[numEqualBest-1] = i

                #remember best
                elif UCBvalue == bestVal :
                    numEqualBest += 1
                    indicesBest[numEqualBest-1] = i

            except:
                print 'UCBT(): lol'

    #break ties randomly
    indicesBest[0] = indicesBest[random.randint(0,numEqualBest-1)]

    return actions[indicesBest[0]]


def SoftMax(M, tao):

    # hardcoded limitation due to numerical stability
    if tao > 0.005 :

        #average = 0.0
        #variance = 0.0

        #meanT = [0.0] * len(M)
        #for m in xrange(len(M)) :
        #    meanT[m] = (M[m].mean)
        #    old_avg = average
        #    average = average + (meanT[m] - average) / (m + 1)
        #    variance = variance + (meanT[m] - average) * (meanT[m] - old_avg)

        #deviation = sqrt(variance/len(M))

        #if deviation == 0.0 :
        #    values = [m.mean for m in M]
        #    return M[CompleteGreedy(values)]
        #Norm=[ (1.0 / (1.0 + exp(-(m-average)/deviation) ) ) for m in meanT]
        #E=[exp(a) for a in Norm]

        A=[m.mean for m in M]
        E=[exp(a/tao) for a in A]
        E_sum=sum(E)
        P=[e/E_sum for e in E]

        sp = 0.0
        rpoint = random.random()
        for i in xrange(len(P)):
            sp = sp + P[i]
            if rpoint < sp:
               return (M[i])

    # if temperature is close to zero, then the algorithm is pratically completely greedy
    else :
        values = [m.mean for m in M]
        return M[CompleteGreedy(values)]

def CompleteGreedy(valueList) :
    bestVal = -1e30000
    numEqualBest = 1
    indicesBest = [-1]*len(valueList)
    for i in xrange(len(valueList)) :

        #find action with highest value
        if valueList[i] > bestVal :
            bestVal = valueList[i]
            numEqualBest = 1
            indicesBest[numEqualBest-1] = i

        #remember best
        elif valueList[i] == bestVal :
            numEqualBest += 1
            indicesBest[numEqualBest-1] = i

    #break ties randomly
    indicesBest[0] = indicesBest[random.randint(0,numEqualBest-1)]

    return indicesBest[0]

def EGreedy(M, E):
    Avg=[m.mean for m in M]
    maxM=Avg.index(max(Avg))
    P=[float(E)/len(M)]*len(M)
    P[maxM]=1-E+E/len(M)
    sp = 0.0
    rpoint = random.random()
    for i in xrange(len(P)):
        sp = sp + P[i]
        if rpoint < sp:
            return (M[i])

# Algorithm POKER (Vermorel & Mohri 2005)
def POKER(M,params,horizon):

    # Cummulative Normal Function
    def normcdf(x, mu, sigma):
        t = x-mu;
        y = 0.5*erfc(-t/(sigma*sqrt(2.0)));
        if y>1.0:
            y = 1.0;
        return y


    leverCount = len(M)

    lastPulledLever = params[0]
    leverMeanSum = params[1]
    leverSigmaSum = params[2]
    #allPulls = params[3]
    #horizon = H - allPulls


    # determine observedLeverCount and twiceObservedLeverCount
    observationCounts = [m.pulls for m in M]
    observedLeverCount = sum([obs>0 for obs in observationCounts])
    twiceObservedLeverCount = sum([obs>1 for obs in observationCounts])

    rewardSums = [m.sum for m in M]
    rewardSquareSums = [m.sum_squared for m in M]
    rewardMeans = [m.mean for m in M]


    # initialization: observing at least two levers twice
    # FIX: the default sigma must not be null
    if (observedLeverCount < 1 or leverSigmaSum == 0):
        # playing twice the same lever
        if observationCounts[lastPulledLever] == 1:
            return M[lastPulledLever]

        # if all machines have been pulled at least twice, select best one
        if twiceObservedLeverCount == leverCount:
            max_index = rewardSums.index(max(rewardSums))
            return M[max_index]

        # random machine
        lastPulledLever = random.randint(0, leverCount-1)
        return M[lastPulledLever]

    # computing the delta
    means = [rewardMeans[i] for i in xrange(leverCount) if observationCounts[i]]
    #means = [0 for i in xrange(observedLeverCount)];
    #for i in xrange(leverCount):
    #    if observationCounts[i] > 0:
    #        means.append(rewardSums[i] / observationCounts[i])
    means.sort()
    k = int(ceil(sqrt(len(means))))
    delta = means[-1] - means[-k]
    maxMean = means[-1]

    # if k equals 1, then just play randomly (delta could not be estimated)
    if(k <= 1):
        rndMachine = random.randint(0, leverCount-1)
        return M[rndMachine]

    delta /= (k - 1);

    # computing the prices of the observed levers
    maxPrice =  float("-inf")
    maxPriceIndex = -1 # dummy initialization

    for i in xrange(leverCount):
        if observationCounts[i] > 0:
            mean = rewardMeans[i]

    		# empirical estimate of the standard deviation is avaiblable
            sigma = 0
            if observationCounts[i] > 1:
                try:
            	    sigma = sqrt(float(rewardSquareSums[i]) / observationCounts[i] - mean * mean) #sqrt(M[i].variance)
                except:
                    print "rewardSquareSum= "+str(rewardSquareSums[i])+"Observation counts= "+str(observationCounts[i])+"mean= "+str(mean)
                    raise

    			# FIX: sigma must not be null
            if sigma == 0:
    			sigma = float(leverSigmaSum) / twiceObservedLeverCount

            # using the avg standard deviation among the levers
            else:
    			sigma = float(leverSigmaSum) / twiceObservedLeverCount

    		# computing an estimate of the lever optimality probability
            proba = (1 - normcdf(maxMean + delta,mean,sigma / sqrt(observationCounts[i])))

    		# price = empirical mean + estimated long term gain
            price = mean + horizon * delta * proba

            if maxPrice < price:
    			maxPrice = price
    			maxPriceIndex = i


    # computing the price for the unobserved levers
    if(observedLeverCount < leverCount):
    	unobservedPrice = float(leverMeanSum) / observedLeverCount + horizon * delta / observedLeverCount

        if unobservedPrice > maxPrice:
            maxPrice = unobservedPrice

        	# Choosing randomly an unobserved lever
            uIndex = random.randint(0, leverCount-observedLeverCount)
            uCount = 0
            for i in xrange(leverCount):
                if observationCounts[i] == 0:
                    if uCount == uIndex:
                    	maxPriceIndex = i
                    	break
                    else:
                        uCount+=1

    return (M[maxPriceIndex])




