from api import JackpotApi
from python.algorithms.epsilon_greedy.standard import EpsilonGreedy
from python.algorithms.ucb.ucb1 import UCB1
from python.algorithms.ucb.ucb2 import UCB2
from python.algorithms.exp3.exp3 import Exp3
from rpm import RPM
from rpm import RPMTime
from rpm import RPMAnnealing
import sys
import matplotlib.pyplot as plt


def evaluate(api, repeat=20):
    """
    Evaluate different MAB algorithms and repeat every algorithm for :repeat times to get higher confidence in
    MAB algorithm performances
    :param api: JackpotApi instance
    :param repeat: Repeat given :api session for :repeat times
    """
    print "repeat: "+str(repeat)
    algos = [
        ('usb1', UCB1([], [])),
        ('ucb2 a=0.05', UCB2(0.05, [], [])),
        ('ucb2 a=0.1', UCB2(0.1, [], [])),
        ('ucb2 a=0.3', UCB2(0.3, [], [])),
        ('ucb2 a=0.5', UCB2(0.5, [], [])),
        ('ucb2 a=0.7', UCB2(0.7, [], [])),
        ('exp3 a=0.1', Exp3(0.1, [])),
        ('exp3 a=0.3', Exp3(0.3, [])),
        ('rpm', RPM([], [])),
        ('rpmTime: 0.1', RPMTime(int(api.pulls * 0.1))),
        ('rpmTime: 0.2', RPMTime(int(api.pulls * 0.2))),
        ('rpmTime: 0.3', RPMTime(int(api.pulls * 0.3))),
        ('rpmA 0.9999', RPMAnnealing(0.9999)),
        ('rpmA 0.99999', RPMAnnealing(0.99999)),
        ('rpmA 0.999999', RPMAnnealing(0.999999)),
        ('rpmA 0.999999999', RPMAnnealing(0.999999999)),
    ]

    for name, algo in algos:
        reward_sum = 0
        for r in range(repeat):
            algo.initialize(api.machines)
            arm_pulls = [0 for i in range(api.machines)]

            for pull in range(api.pulls):
                pull += 1

                chosen_arm = algo.select_arm()
                reward = api.pull(chosen_arm + 1, pull)
                algo.update(chosen_arm, reward)

                reward_sum += reward
                arm_pulls[chosen_arm] += 1
        print name + ": " + str(reward_sum / float(repeat))


def plot_dist(api, interval=100):
    """
    Plot arms distribution for given api in different times of session. These plots helps us to compare
    MAB algorithms between each other and with target arms distribution.
    :param api: JackpotApi instance
    :param interval: Plot interval...we do not need to plot arms distribution in every step of session
    """
    algos = [
        ('usb1', UCB1([], [])),
        ('ucb2 a=0.05', UCB2(0.05, [], [])),
        ('ucb2 a=0.1', UCB2(0.1, [], [])),
        ('ucb2 a=0.3', UCB2(0.3, [], [])),
        ('ucb2 a=0.5', UCB2(0.5, [], [])),
        ('ucb2 a=0.7', UCB2(0.7, [], [])),
        ('exp3 a=0.1', Exp3(0.1, [])),
        ('exp3 a=0.3', Exp3(0.3, [])),
        ('rpm', RPM([], [])),
        ('rpmTime: 0.1', RPMTime(int(api.pulls * 0.1))),
        ('rpmTime: 0.2', RPMTime(int(api.pulls * 0.2))),
        ('rpmTime: 0.3', RPMTime(int(api.pulls * 0.3))),
        ('rpmA 0.9999', RPMAnnealing(0.9999)),
        ('rpmA 0.99999', RPMAnnealing(0.99999)),
        ('rpmA 0.999999', RPMAnnealing(0.999999)),
        ('rpmA 0.999999999', RPMAnnealing(0.999999999)),
    ]

    for name, algo in algos:
        reward_sum = 0
        algo.initialize(api.machines)
        rpm_values = [[] for arm in range(len(algo.values))]
        for pull in range(api.pulls):
            pull += 1

            chosen_arm = algo.select_arm()
            reward = api.pull(chosen_arm + 1, pull)
            algo.update(chosen_arm, reward)

            reward_sum += reward
            if pull % interval == 0:
                for arm in range(len(algo.values)):
                    if sum(algo.counts[arm]) > 0:
                        rpm_values[arm].append(sum(algo.values[arm]) / float(sum(algo.counts[arm])))
                    else:
                        rpm_values[arm].append(0)

        for i, m in enumerate(rpm_values):
            print len(m)
            plt.plot(range(0,len(m) * interval, interval), m, label="machine %d" % (i + 1))
        plt.legend(loc=2)
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Wrong arguments"
        exit()

    api = JackpotApi(sys.argv[1])
    evaluate(api)
    #plot_dist(api)