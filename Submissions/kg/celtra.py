import urllib
from collections import deque
from scipy.stats import *
import sys
from operator import attrgetter

# konstante za detekcijo sprememb...
windowSize = 50
threshold = 0.001


class Case:
    def __init__(self, url):
        self.url = url
        self.pulls = 0
        self.numOfMachines = int(urllib.urlopen(url + "/machines").read())
        self.pullsAvailable = int(urllib.urlopen(url + "/pulls").read())
        self.machines = []
        for i in range(self.numOfMachines):
            self.machines.append(Machine(windowSize, threshold, url + "/" + str(i + 1) + "/"))
            # Zaradi casovne stiske nisem dokoncno optimiral zgornjih parametrov :(

    def clearMachineHistory(self):
        for machine in self.machines:
            machine.reset()


class Machine:
    def __init__(self, windowSize, threshold, url):
        self.url = url
        self.threshold = threshold
        self.window = deque(maxlen=windowSize)
        self.binomProb = 0
        self.prediction = 0.5
        self.pulls = 0
        self.wins = 0

    def reset(self):
        self.binomProb = 0
        self.prediction = 0.5
        self.pulls = 0
        self.wins = 0
        self.window.clear()

    def pull(self, pullNumber):
        value = int(urllib.urlopen(self.url + str(pullNumber + 1)).read())
        self.pulls += 1
        self.wins += value
        self.prediction = 1.0 * self.wins / self.pulls
        if self.prediction == 0:
            self.prediction = 0.0000001  # Zagotovi ustreznejse rezultate funkcije calcBinom()
        self.window.append(value)
        if len(self.window) == self.window.maxlen: #ce je okno polno
            if binom_test(self.window.count(1), len(self.window), self.prediction) < self.threshold:  # preverimo ce se je pojavila sprememba v verjetosti avtomata
                return -1
        return value


    # izracunamo kaksna je verjetnost da  presezemo najboljso verjetnost med avtomati(probability)
    # avtomatom z manjsim stevilom zmag damo malo prednosti in tako zmanjsamo verjetnost,
    # da kateremu od avtomatov zaradi nesrecnega nakljucja(npr.2 zaporedni nicli ob verjetnosti 0.8)
    # ne zagotovimo dovolj testnih potegov.
    def calcBinom(self, probability):
        self.binomProb = 1 - binom.sf( self.wins if self.wins < 2 else self.wins-1, self.pulls, probability)

def main():
    input = sys.argv[1]
    case = Case(input)
    for pullNum in range(case.pullsAvailable):
        bestProbability = max(machine.prediction for machine in case.machines)  # poiscemo najboljso izracunano verjetnost med avtomati
        for m in case.machines:
            m.calcBinom(bestProbability)  # izracunamo verjetnost, da avtomat preseze trenutno najboljso izracunano verjetnost
        bestMachine = max(case.machines, key=attrgetter('binomProb'))  # izberemo najbolj perspektiven avtomat
        value=bestMachine.pull(pullNum)# potegnemo najboljsi avtomat
        if value == -1:  #ce na avtomatu zaznamo spremembo
            case.clearMachineHistory()  # pobrisemo vse in znova zacnemo ocenjevanje verjetnosti


if __name__ == '__main__':
    main()