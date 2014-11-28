#-- imports --#
from webClient import *
from MABsolver import *
from Config import *
import sys

###--- main program procedure (user code) ---###
#parse arguments
if len(sys.argv)<2:
    print "Not enough arguments!\n"
    print "Usage: Jackpot.exe <server url>\n"
    sys.exit()

url=sys.argv[1];
#url="http://celtra-jackpot.com/10"     #debug: override

try:
    server=url.split("/")[2]
    case=int(url.split("/")[3])
    prefix=sys.argv[2]
except:
    print "Wrong argument format!"
    print "Use form: http://celtra-jackpot.com/<case>"
    sys.exit(); 

if case<1:
    print "Wrong case number, must be >0!"
    sys.exit();


#settings
linUCBTweights = [1  ,-0.1,-0.4,0.8,-0.1,-0.3]
solv_initial_param_values = [linUCBTweights[0:3], linUCBTweights[3:6], [0,1], 43, 1.0]
solv_selection_policy = GLODEF_SELECTION_VOTER
solv_change_point_detector = GLODEF_CHANGEPOINT_HENKYPENKY
solv_change_point_test = DEFAULT_CHANGEPOINT_TEST
solv_reset_algorithm = GLODEF_RESET_ALGORITHM_RESET_ALL_TO_ZERO
solv_param_types = [GLODEF_PARAM_FUNCTION_LINEAR , GLODEF_PARAM_FUNCTION_LINEAR, GLODEF_PARAM_FUNCTION_LINEAR, GLODEF_PARAM_FUNCTION_DIRECT, GLODEF_PARAM_FUNCTION_DIRECT]
solv_param_num_inputs = [2, 2, 1, 0, 0]

#connect to server
print "Fetching case "+str(case)+" data..."
num_bandits=getNumMachines(server,case,prefix)
print "Number of machines: "+str(num_bandits)
max_pulls=getNumPulls(server,case,prefix)
print "Maximum number of pulls: "+str(max_pulls)

s=connect(server)
if s==None:
    print "Exiting."
    sys.exit()
print "Connected to server!"

#create solver
solver = MABsolver(solv_initial_param_values, solv_selection_policy, solv_change_point_detector, solv_change_point_test, solv_reset_algorithm, solv_param_types, solv_param_num_inputs)
solver.resetState(num_bandits)
solver.max_pulls=max_pulls;
total_reward=0;

for p in xrange(max_pulls) :
    
    if solver.config.selectionPolicy == GLODEF_SELECTION_POKER or solver.config.selectionPolicy == GLODEF_SELECTION_VOTER:
            if solver.config.params[2].function != GLODEF_PARAM_FUNCTION_DIRECT :
                solver.config.params[2].updateSingleInput ( 0 , max_pulls-p)
    if solver.config.params[0].function != GLODEF_PARAM_FUNCTION_DIRECT :
        solver.config.params[0].updateSingleInput ( 0 , max_pulls/30000.0)
        solver.config.params[0].updateSingleInput ( 1 , num_bandits/10.0)
    if solver.config.params[1].function != GLODEF_PARAM_FUNCTION_DIRECT :
        solver.config.params[1].updateSingleInput ( 0 , max_pulls/30000.0)
        solver.config.params[1].updateSingleInput ( 1 , num_bandits/10.0)

    selected_bandit = solver.selectBandit()         #apply selection policy

    reward=getMachineResponse(s, server, case, selected_bandit+1, p+1, prefix)
    print "Pull: "+str(p+1)+" reward: "+str(reward)
    solver.update(selected_bandit, reward, 1)
    total_reward += reward

print "Case: "+str(case)+" | total pulls: "+str(max_pulls)+" | total reward: "+str(total_reward)