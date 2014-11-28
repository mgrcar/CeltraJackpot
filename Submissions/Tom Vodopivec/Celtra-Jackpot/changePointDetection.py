#
# Statistical tests to determine if the machine changed
#
from Config import *
from math import *

#rat=kumulativen povprecen reward na avtomat v t potezah
#rt=sestevek rewardow do t
#delta toleranca

#PH0=M0-m0=0
#PHt=Mt-mt=max(PH(t-1)-rt+rat-delta,0)

#Treshold 80

def detectChangePoint(solver, machine_id):
    rejected_pulls=0
    # self.config.params[0].updateInputs( array_of_new_inputs )
        #or
        # self.config.params[0].lastInputs[0] = some_new_input1
        # self.config.params[0].lastInputs[1] = some_new_input2
        # self.config.params[1].lastInputs[0] = some_new_input1
        # self.config.params[1].lastInputs10] = some_new_input2
        # self.config.params[2].lastInputs[0] = some_new_input3
    if solver.config.changePointDetector == GLODEF_CHANGEPOINT_Z_TEST :
            rejected_pulls = checkChange(solver,machine_id)
    elif solver.config.changePointDetector == GLODEF_CHANGEPOINT_HENKYPENKY :
            rejected_pulls=HankeyPankeyTest(solver,machine_id)
    
    
    return rejected_pulls

def HankeyPankeyTest(solver,m_id):
    threshold = solver.config.params[3].getValue()
    take_last_samples = int(solver.config.params[4].getValue())
    reset_algorithm=solver.config.resetAlgorithm
    M=solver.machines
    t=0
    m=M[m_id] 
    rejected=0
    s=take_last_samples
    if s<m.pulls:
        m.moving_sum[t]=m.moving_sum[t]-m.R[-(s+1)]
    m.moving_sum[t]=m.moving_sum[t]+m.R[-1]
    if s>=m.pulls:
        s=m.pulls-1
    Z=abs(M[m_id].CUSUM)

    #solver.config.params[1].updateInputs( [s] )
    #treshold = solver.config.params[1].getValue()

    if Z>=threshold:
        if(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_ALL_TO_ZERO):  rejected=resetAllToZero(M)
        elif(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_ALL_TO_MOVING_AVERAGE): rejected=resetAllToMovingMean(M,t,s)
        elif(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_ALL_TO_MOVING_AVERAGE_CUTOFF): rejected=resetAllToMovingMeanCutOff(M,m.P[-s-1])
        elif(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_TO_MOVING_AVERAGE): rejected=resetToMovingMean(m,t,s+1)
    return rejected


def checkChange(solver,m_id):
    threshold = solver.config.params[1].getValue()
    shrink_interval = solver.config.params[2].getValue()
    start_mv = solver.config.params[3].getValue()
    reset_algorithm=solver.config.resetAlgorithm
    M=solver.machines
    tp=range(10,100,10) + range(100,1000,100) + range(1000,6000,1000)
    m=M[m_id]
    rejected=0
    for t in range(0,len(tp)):
        s=tp[t]
        if s<m.pulls:
            m.moving_sum[t]=m.moving_sum[t]-m.R[-(s+1)]
        m.moving_sum[t]=m.moving_sum[t]+m.R[-1]
        if s>m.pulls:
            s=m.pulls
        if m.pulls>=2*s and s>=tp[0] and s>=start_mv:
            x=m.sum-m.moving_sum[t]
            y=m.moving_sum[t]
            xn=m.pulls-s
            yn=s
            #shrink:
            x=x*shrink_interval+((1.0-shrink_interval)/2.0)*xn
            y=y*shrink_interval+((1.0-shrink_interval)/2.0)*yn
            Z=testIfDistDiff(x,y,xn,yn)
        #print str(Z)
        # 95 % confidence interval
            if Z>=threshold:
                if(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_ALL_TO_ZERO):  rejected=resetAllToZero(M)
                elif(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_ALL_TO_MOVING_AVERAGE): rejected=resetAllToMovingMean(M,t,s)
                elif(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_ALL_TO_MOVING_AVERAGE_CUTOFF): rejected=resetAllToMovingMeanCutOff(M,m.P[-s-1])
                elif(reset_algorithm==GLODEF_RESET_ALGORITHM_RESET_TO_MOVING_AVERAGE): rejected=resetToMovingMean(m,t,s)
    return rejected
            
def resetAllToZero(M):
    rejected=0
    for m in M:
        rejected+=m.resetState(-1,0)

    return rejected

def resetAllToMovingMean(M, t, s):
    rejected=0
    for m in M:
        rejected+=m.resetState(t,s)

    return rejected

def resetAllToMovingMeanCutOff(M,last_pull):
    rejected=0
    for m in M:
        rejected+=m.resetState(-2,last_pull)
               
    return rejected

def resetToMovingMean(m,t,s):
    rejected=m.resetState(t,s)
    return rejected

#Davor statistical test (default)
def testIfDistDiff(X,Y,Nx,Ny):
    try:
        Z=abs(((float(X)/Nx)-(float(Y)/Ny))/sqrt((float(X)+float(Y))/(float(Nx)+float(Ny))*(1.0-(float(X)+float(Y))/(float(Nx)+float(Ny)))*(1.0/float(Nx)+1.0/Ny)))
    except:
        Z=0.0
    return Z

#Tom statistical test
def testIfSampleDiff(X,Y,Nx,Ny):

    Z1=sqrt((Nx*(X/Nx-Y/Ny)**2)/(X/Nx*(1-X/Nx)+0.00001))/2
    Z2=sqrt((Ny*(X/Nx-Y/Ny)**2)/(Y/Ny*(1-Y/Ny)+0.00001))/2

    Z=min(Z1,Z2)
    return Z

 