from Config import *
from machine import *
from strategy import *
from changePointDetection import *
import types

class ParamFunction() :

    function = None
    weights = None
    numInputs = None
    lastInputs = None
    lastOutput = None

    def __init__(
        self,
        function = DEFAULT_PARAM_FUNCTIONS,
        numInputs = DEFAULT_PARAM_NUMINPUTS,
        weightValues = 0.0
        ) :

        self.function = function
        self.numInputs = numInputs
        self.lastInputs = [None] * numInputs
        if not isinstance(weightValues, types.ListType) :
            self.weights = [weightValues] * (self.numInputs + 1)
        elif len(weightValues) == (numInputs + 1):
            self.weights = weightValues
        else :
            print 'ERROR: class ParamFunction(): number of specified initial values mismatches the number of weights and inputs'

    def updateInputs(self, newInputs, calcOutputs = 0) :
        self.lastInputs = newInputs
        if calcOutputs == 1 :
            self.getValue()

    def updateSingleInput(self, selectedInput, newInput, calcOutputs = 0) :
        if selectedInput < self.numInputs :
            self.lastInputs[selectedInput] = newInput
        else :
            print 'WARNING: ParamFunction(): updateSingleInput(): update input out of index - IGNORED'

        if calcOutputs == 1 :
            self.getValue()

    def getValue(self) :
        if  (self.function == GLODEF_PARAM_FUNCTION_DIRECT) :
            self.lastOutput = self.weights[0]
        elif(self.function == GLODEF_PARAM_FUNCTION_LINEAR) :
            self.lastOutput = self.weights[0]
            for i in xrange(self.numInputs) :
                self.lastOutput += (self.weights[i+1]) * self.lastInputs[i]
        elif(self.function == GLODEF_PARAM_FUNCTION_NEURAL) :
            #TODO
            todo

        return self.lastOutput

# configuration structure for MABsolver
class MABsolver_config() :

    selectionPolicy = None
    changePointDetector = None
    changePointTest = None
    resetAlgorithm = None
    params = None

    infoNumOutputLines = 4

    def __init__(
        self,
        paramValues = None,
        selectionPolicy = DEFAULT_SELECTION_POLICY,
        changePointDetector = DEFAULT_CHANGEPOINT_DETECTOR,
        changePointTest = DEFAULT_CHANGEPOINT_TEST,
        resetAlgorithm = DEFAULT_RESET_ALGORITHM,
        paramFunctions = [DEFAULT_PARAM_FUNCTIONS] * DEFAULT_SOLVER_NUMPARAMS,
        paramNumInputs = [DEFAULT_PARAM_NUMINPUTS] * DEFAULT_SOLVER_NUMPARAMS

        ) :

        self.selectionPolicy = selectionPolicy
        self.changePointDetector = changePointDetector
        self.resetAlgorithm = resetAlgorithm
        self.changePointTest = changePointTest

        lenF = len(paramFunctions)
        lenI = len(paramNumInputs)
        if not(lenF == lenI) :
            print 'MABsolver_config(): ERROR_INIT: params configuration not equal length'
            print ''
            return

        if paramValues is None :

            paramValues = [0.0 , DEFAULT_PAR_CHANGEPOINT_THR, DEFAULT_PAR_CHANGEPOINT_INT, DEFAULT_PAR_CHANGEPOINT_NUM, DEFAULT_PAR_CHANGEPOINT_SOFT]

            if   selectionPolicy == GLODEF_SELECTION_EGREEDY :  paramValues[0] = DEFAULT_PAR_EGREEDY_E
            elif selectionPolicy == GLODEF_SELECTION_SOFTMAX :  paramValues[0] = DEFAULT_PAR_SOFTMAX_T
            elif selectionPolicy == GLODEF_SELECTION_UCB1 :     paramValues[0] = DEFAULT_PAR_UCB1_C
            elif selectionPolicy == GLODEF_SELECTION_UCBTUNED : paramValues[0] = DEFAULT_PAR_UCB1_C
            elif selectionPolicy == GLODEF_SELECTION_POKER :    paramValues[0] = DEFAULT_PAR_POKER_H
            elif selectionPolicy == GLODEF_SELECTION_VOTER :    paramValues[0] = DEFAULT_PAR_VOTER

            self.params = [ParamFunction(paramFunctions[i], paramNumInputs[i], paramValues[i]) for i in xrange(lenF)]

        else :
            lenV = len(paramValues)
            if not(lenV == lenI):
                print 'MABsolver_config(): ERROR_INIT: params configuration not equal length'
            self.params = [ParamFunction(paramFunctions[i], paramNumInputs[i], paramValues[i]) for i in xrange(lenF)]

    def info(self) :
        print 'MABsolver_config: algorithms: %s , %s , %s , %s' % (
            GLO_labels_selection_policies[self.selectionPolicy],
            GLO_labels_change_point_detectors[self.changePointDetector],
            GLO_labels_change_point_test[self.changePointTest],
            GLO_labels_reset_algorithms[self.resetAlgorithm]
            )

        print 'MABsolver_config: params: types: ',
        for i in range(len(self.params)) :
            print '%s ' % GLO_labels_param_function[self.params[i].function],
        print ''
        print 'MABsolver_config: params: numInputs: ',
        for i in range(len(self.params)) :
            print '%d ' % self.params[i].numInputs,
        print ''
        print 'MABsolver_config: params: weights: ',
        for i in range(len(self.params)) :
            print '[ ',
            for j in range(self.params[i].numInputs + 1) :
                print '%f ' % self.params[i].weights[j],
            print '] ',
        print ''

# The Multi-Armed-Bandit (MAB) solver structure
class MABsolver() :

    config = None
    machines = None
    ucbt_machines = None
    numMachines = None

    pulls = None
    total_rejected_pulls = None
    max_pulls = None

    # Index of last machine played
    lastPulledMachine = None
    machineMeanSum = None
    machineSigmaSum = None
    voter=None

    # initialization
    def __init__(
        self,
        paramValues = None,
        selectionPolicy = DEFAULT_SELECTION_POLICY,
        changePointDetector = DEFAULT_CHANGEPOINT_DETECTOR,
        changePointTest = DEFAULT_CHANGEPOINT_TEST,
        resetAlgorithm = DEFAULT_RESET_ALGORITHM,
        paramTypes = [DEFAULT_PARAM_FUNCTIONS] * DEFAULT_SOLVER_NUMPARAMS,
        paramNumInputs = [DEFAULT_PARAM_NUMINPUTS] * DEFAULT_SOLVER_NUMPARAMS,
        init_bandits = 0,
        ) :

        self.config = MABsolver_config(paramValues, selectionPolicy, changePointDetector, changePointTest, resetAlgorithm, paramTypes, paramNumInputs)
        self.voter=ensemble()
        self.resetState(init_bandits)
        

    # reset memory structures (preparation for new testcase)
    def resetState(self, num_bandits) :
        self.machines = [machine(m) for m in range(num_bandits)]
        self.ucbt_machines = [machine(m) for m in range(num_bandits)]
        self.numMachines = num_bandits

        self.pulls = 0
        self.total_rejected_pulls = 0
        self.lastPulledMachine = 0
        self.machineMeanSum = 0.0
        self.machineSigmaSum = 0.0
        self.voter.resetState()

        #self.epsilon_soft = self.config.params[0]
        #self.softMax_tao = self.config.params[1]
        #self.UCB1_parC = self.config.params[2]
        #self.change_point_threshold = self.config.params[3]

    # select a bandit from available stats
    def selectBandit(self, increase_pulls = 1) :

        #TODO PARAM_INPUTS if not direct parameter search (if linear or neural used...), update inputs in function approximator for parameters
        #example:
        # self.config.params[0].updateInputs( array_of_new_inputs )
        #or
        # self.config.params[0].lastInputs[0] = some_new_input1
        # self.config.params[0].lastInputs[1] = some_new_input2
        # self.config.params[1].lastInputs[0] = some_new_input1
        # self.config.params[1].lastInputs10] = some_new_input2
        # self.config.params[2].lastInputs[0] = some_new_input3

        #UCBTVoter C
        p0 = self.config.params[0].getValue()
        exploration_weight = p0
        
        # exploration_weight defined with both p0 and p1, where p0 is the initial value and p1 the final
        # (comment out to disable)
        #UCBTMain C
        p1 = self.config.params[1].getValue()
        exploration_weight = ( ( p1 - p0 ) / ( self.max_pulls - self.total_rejected_pulls ) ) * (self.pulls - self.total_rejected_pulls) + p0
        
        voterC=self.config.params[4].getValue()

        #Poker horizon
        if(len(self.config.params) > 2):
            horizon = self.config.params[2].getValue()
        
        POKER_params = [self.lastPulledMachine, self.machineMeanSum, self.machineSigmaSum]

        if   self.config.selectionPolicy == GLODEF_SELECTION_RANDOM:    selected_machine = self.machines[random.randint(0, self.numMachines - 1)]
        elif self.config.selectionPolicy == GLODEF_SELECTION_EGREEDY :  selected_machine = EGreedy(self.machines, exploration_weight)
        elif self.config.selectionPolicy == GLODEF_SELECTION_SOFTMAX :  selected_machine = SoftMax(self.machines, exploration_weight)
        elif self.config.selectionPolicy == GLODEF_SELECTION_UCB1 :     selected_machine = UCB1(self.machines, self.pulls - self.total_rejected_pulls, exploration_weight)
        elif self.config.selectionPolicy == GLODEF_SELECTION_UCBTUNED : selected_machine = UCBT(self.machines, self.pulls - self.total_rejected_pulls, exploration_weight)
        elif self.config.selectionPolicy == GLODEF_SELECTION_POKER : selected_machine = POKER(self.machines, POKER_params, horizon)
        elif self.config.selectionPolicy == GLODEF_SELECTION_VOTER : selected_machine = self.voter.UCBTVoter(self.machines, self.machines, self.pulls, self.total_rejected_pulls, [voterC, exploration_weight, horizon])
        self.pulls += increase_pulls

        return selected_machine.id


    # update stats and detect change point (if enabled)
    def update(self, machine_id, reward,suppress_output = 0) :

        #TODO PARAM_INPUTS if not direct parameter search (if linear or neural used...), update inputs in function approximator for parameters
        #example:
        # self.config.params[0].updateInputs( array_of_new_inputs )
        #or
        # self.config.params[0].lastInputs[0] = some_new_input1
        # self.config.params[0].lastInputs[1] = some_new_input2
        # self.config.params[1].lastInputs[0] = some_new_input1
        # self.config.params[1].lastInputs10] = some_new_input2
        # self.config.params[2].lastInputs[0] = some_new_input3

        self.machines[machine_id].update(reward, self.pulls)
        self.ucbt_machines[machine_id].update(reward, self.pulls)
        self.voter.update(self.machines, reward, self.pulls)

        # POKER stuff
        self.lastPulledMachine = machine_id
        self.machineMeanSum += self.machines[machine_id].mean
        self.machineSigmaSum += sqrt(self.machines[machine_id].variance)

        # change point detection
        rejected_pulls = 0
        rejected_pulls = detectChangePoint(self, machine_id)
        if rejected_pulls > 0 :
            # POKER reset to zero
            self.machineMeanSum = 0.0
            self.machineSigmaSum = 0.0
            self.voter.machineSigmaSum = 0.0
            self.voter.machineMeanSum = 0.0

            if not suppress_output :
                print 'MABsolver: changePointDetector: Global pull at change point: %d' + i
        self.total_rejected_pulls += rejected_pulls

    def listParams(self, selectiveList = None) :

        if selectiveList is None :
            selectedParams = range(len(self.config.params))
        else :
            selectedParams = selectiveList

        list = []
        for i in selectedParams :
            if not isinstance(i, types.ListType) :
                list = list + self.config.params[i].weights
            else :
                for j in i[1] :
                    list = list + [self.config.params[i[0]].weights[j]]

        return list

    def setParams(self, newValues, selectiveList = None) :

        if selectiveList is None :
            selectedParams = range(len(self.config.params))
        else :
            selectedParams = selectiveList

        c = 0
        for i in selectedParams :
            if not isinstance(i, types.ListType) :
                for j in xrange(len(self.config.params[i].weights)) :
                    self.config.params[i].weights[j] = newValues[c]
                    c += 1
            else :
                for j in i[1] :
                    self.config.params[i[0]].weights[j] = newValues[c]
                    c += 1

        if not (c == len(newValues)) :
           print 'MABsolver(): setParams(): ERROR: newValues list incorrect length'


    # output memorized stats
    def infoStats(self) :
        for m in self.machines:
                print 'MABsolver_stats: Machine '+str(m.id)+' Total reward: '+str(m.sum_total)+' Total pulls: '+str(m.pulls_total)+' Average reward: '+str(m.mean)
