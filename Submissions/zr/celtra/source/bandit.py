import urllib.request
from urllib.error import URLError
from scipy.stats import beta
import sys


def bandit(url):
    #stevec zmag
    wins = 0
    #stevilo avtomatov in potegov
    num_of_machines = int(urllib.request.urlopen(url + '/machines').read())
    num_of_pulls = int(urllib.request.urlopen(url + '/pulls').read())
    #stevec zmag posameznega avtomata
    machines = [0] * num_of_machines
    for j in range(num_of_pulls):
        samples = []
        #vzorcimo vsak avtomat iz njegove apriorne beta distribucije
        for k in range(num_of_machines):
            prior = beta(machines[k] + 1, 1 + j - machines[k])
            samples += [prior.rvs()]
        #izberemo avtomat z najvecjo vrednosjo vzorca
        selected = samples.index(max(samples))
        #potegnemo izbran avtomat, poveca se stevec zmag avtomata in stevec skupnih uspesnih potegov
        pull = -1
        trys = 0
        while pull == -1:
            trys += 1
            try:
                pull = int(urllib.request.urlopen(url + "/" + str(selected + 1) + "/" + str(j + 1)).read())
            except URLError as e:
                print("Srežnik ni odgovoril, poskušam ponovno.")
                if trys >= 5:
                    print("NAPAKA V POVEZAVI!")
                    return -1
        machines[selected] += pull
        wins += pull
    return wins






if __name__ == '__main__':
    rez = bandit(sys.argv[1])
    if rez != -1:
        print("Število uspešnih potegov = " + str(rez))
