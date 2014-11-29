import random
from collections import deque


def ind_max(x):
    m = max(x)
    return x.index(m)


class RPM():
    def __init__(self, counts, values):
        """
        Initialise parameters :counts and :values as private attributes of RPM class
        :param counts:
        :param values:
        """
        self.counts = counts
        self.values = values
        return

    def initialize(self, n_arms):
        """
        Initialise attributes self.counts and self.values for given number of arms (:n_arms)
        :param n_arms: number of arms
        """
        self.counts = [0 for col in range(n_arms)]
        self.values = [0 for col in range(n_arms)]
        return

    def select_arm(self):
        """
        Compute arm index which is optimal regarding previous statistics of arms
        :return: Return index of arm which is recommended by RPM algorithm
        """
        n_arms = len(self.counts)
        rpm_values = [0.0 for arm in range(n_arms)]
        for arm in range(n_arms):
            rpm_values[arm] = random.betavariate(self.values[arm] + 1, self.counts[arm] - self.values[arm] + 1)
        return ind_max(rpm_values)

    def update(self, chosen_arm, reward):
        """
        Update arms' statistics (attributes self.counts & self.values) regarding obtained reward in last pull
        :param chosen_arm: pulled arm in last pull
        :param reward: int value 1 or 0
        """
        self.counts[chosen_arm] += 1
        self.values[chosen_arm] += reward
        return


class RPMAnnealing():
    def __init__(self, annealing_factor, counts=[], values=[]):
        """
        Initialise parameters :counts and :values as private attributes of RPMAnnealing class
        and set annealing_factor
        :param annealing_factor:
        :param counts:
        :param values:
        """
        self.counts = counts
        self.values = values
        self.anneal_fac = annealing_factor
        return

    def initialize(self, n_arms):
        """
        Initialise attributes self.counts and self.values for given number of arms (:n_arms)
        :param n_arms:
        """
        self.counts = [0 for col in range(n_arms)]
        self.values = [0 for col in range(n_arms)]
        return

    def select_arm(self):
        """
        Compute arm index which is optimal regarding previous statistics of arms
        :return: Return index of arm which is recommended by RPM algorithm
        """
        n_arms = len(self.counts)
        rpm_values = [0.0 for arm in range(n_arms)]
        for arm in range(n_arms):
            rpm_values[arm] = random.betavariate(self.values[arm] + 1, self.counts[arm] - self.values[arm] + 1)
        return ind_max(rpm_values)

    def update(self, chosen_arm, reward):
        """
        Update arms' statistics (attributes self.counts & self.values) regarding obtained reward in last pull
        and multiply previous counts and values with annealing_factor
        :param chosen_arm:
        :param reward:
        """
        for arm in range(len(self.counts)):
            self.counts[arm] *= self.anneal_fac
            self.values[arm] *= self.anneal_fac

        self.counts[chosen_arm] += 1
        self.values[chosen_arm] += reward
        return


class RPMTime():
    def __init__(self, history):
        """
        Initialise parameters :counts and :values as private attributes of RPMTime class
        and set attribute history. Every arm stores stats information of previous pulls and rewards only for
        :history part of length of the whole stream
        :param history: float number between 0 and 1
        """
        self.history = history
        self.counts = []
        self.values = []
        return

    def initialize(self, n_arms):
        """
        Initialise attributes self.counts and self.values for given number of arms (:n_arms)
        :param n_arms:
        """
        self.counts = [deque([]) for col in range(n_arms)]
        self.values = [deque([]) for col in range(n_arms)]
        return

    def select_arm(self):
        """
        Compute arm index which is optimal regarding previous statistics of arms
        :return: Return index of arm which is recommended by RPM algorithm
        """
        n_arms = len(self.counts)
        rpm_values = [0.0 for arm in range(n_arms)]
        for arm in range(n_arms):
            rpm_values[arm] = random.betavariate(
                sum(self.values[arm]) + 1,
                sum(self.counts[arm]) - sum(self.values[arm]) + 1
            )
        return ind_max(rpm_values)

    def update(self, chosen_arm, reward):
        """
        Update arms' statistics (attributes self.counts & self.values) regarding obtained reward in last pull.
        :param chosen_arm:
        :param reward:
        """
        for arm in range(len(self.counts)):
            if arm == chosen_arm:
                self.counts[arm].append(1)
                self.values[arm].append(reward)
            else:
                self.counts[arm].append(0)
                self.values[arm].append(0)
            if len(self.values[arm]) > self.history:
                self.counts[arm].popleft()
                self.values[arm].popleft()
        return