from api import JackpotApi
from rpm import RPMTime
import sys


def simulate(api):
    """
    Run the whole jackpot session for given api
    :param api: JackpotApi instance
    :return: reward obtained in whole session
    """
    algo = RPMTime(int(api.pulls * 0.2))
    algo.initialize(api.machines)
    arm_pulls = [0 for i in range(api.machines)]
    reward_sum = 0
    for pull in range(api.pulls):
        pull += 1

        chosen_arm = algo.select_arm()
        reward = api.pull(chosen_arm + 1, pull)
        algo.update(chosen_arm, reward)

        reward_sum += reward
        arm_pulls[chosen_arm] += 1
    print arm_pulls
    return reward_sum

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Wrong arguments"
        exit()

    api = JackpotApi(sys.argv[1])
    print simulate(api)