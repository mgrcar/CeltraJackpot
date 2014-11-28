__author__ = 'Gasper Zgajnar, 63090178'

import urllib2
import random
import time
#import matplotlib.pyplot as plt
import sys
#from scipy.fftpack import fft

config = {
    "server": "http://celtra-jackpot.com",
    "pulls": "pulls",
    "machines": "machines",
    "n_examples": [], #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "n_repeat": 1
}


def get_response(url):
    try:
        response = urllib2.urlopen(url).read()
        return -1 if response == "ERR" else response
    except Exception as e:
        #print "exception", e.message
        return -1


def get_number_of(server_url, example, type):
    """Return number of machines/pulls for current example."""
    url = server_url + "/" + str(example) + "/" + type
    return int(get_response(url))


def get_pull_response(server_url, example, machine, pull):
    """Return pull response for example on machine for pull number."""
    url = server_url + "/" + str(example) + "/" + str(machine) + "/" + str(pull)
    return int(get_response(url))


def evaluate(config, func):
    """[For testing] Return number of positive responses for all examples."""
    n_positive = 0
    n_all = 0
    for example in config["n_examples"]:
        positive = 0
        all = 0
        for i in xrange(config["n_repeat"]):
            n_machines = get_number_of(config["server"], example, config["machines"])
            n_pulls = get_number_of(config["server"], example, config["pulls"])
            pos, a = func(config, example, n_machines, n_pulls)
            positive += pos
            all += a
        print "Example nr.:", example, positive/float(config["n_repeat"]), all, n_machines, positive/float(all if all > 0 else 1)
        n_positive += positive
        n_all += all

    return n_positive, n_all, n_positive/float(n_all if n_all > 0 else 1)


def calculate_all_probabilities(config):
    """[For testing]Calculate probabilities for all machines for each example"""
    for example in config["n_examples"]:
        n_machines = get_number_of(config["server"], example, config["machines"])
        n_pulls = get_number_of(config["server"], example, config["pulls"])
        probs = []
        for m in xrange(1, n_machines+1):
            n_positive = 0
            n_all = 0
            for pull in xrange(1, n_pulls+1):
                response = get_pull_response(config["server"], example, m, pull)
                n_positive += response if response != -1 else 0
                n_all += (response != -1)
            probs.append(n_positive/float(n_all if n_all > 0 else 1))
        print probs


def evaluate_test(pulls, n, func):
    """[For testing] Return number of positive responses for all examples."""
    positive = 0
    all = 0
    for i in xrange(n):
        pos, a = func(None, None, 2, pulls)
        positive += pos
        all += a
    print "Example nr.:", positive/float(n), all, positive/float(all if all > 0 else 1)


##############################################################
#random: number of positive responses = 2504.0               #
#10 repeats 1 example: 250.4
#number of all requests: 110500                              #
##############################################################
def random_machine(config, example, n_machines, n_pulls):
    """[For testing] Use random machine."""
    n_positive = 0
    n_all = 0
    for pull in xrange(1, n_pulls+1):
        response = get_pull_response(config["server"], example, random.randint(1, n_machines), pull)
        n_positive += response if response != -1 else 0
        n_all += (response != -1)
    return n_positive, n_all
#------------------------------------------------------------#


##############################################################
#number of positive responses (10 repeats, 1. example):295.57#
#number of all requests: 15000                               #
##############################################################
def algorithm_1(config, example, n_machines, n_pulls, percent=0.1):
    """For the n_pulls*percent times try to calculate probabilities for all machines,
       for all other cases each pull pick the best machine and recalculate its probability."""
    n_positive = 0
    n_all = 0
    #machine probabilities (p, pos, all): p-cur. probability, pos-all positive, all
    pm = [(0, 0, 0)]*n_machines
    for pull in xrange(1, n_pulls+1):
        machine = (pull % n_machines if pull < n_pulls*percent else pm.index(max(pm))) + 1
        response = get_pull_response(config["server"], example, machine, pull)
        #response = test_example(pull, machine)
        p, pos, all = pm[machine-1]
        pos += response if response != -1 else 0
        all += (response != -1)
        pm[machine-1] = (pos/float(all), pos, all)

        n_positive += response if response != -1 else 0
        n_all += (response != -1)
    return n_positive, n_all
#-----------------------------------------------------------#


##############################################################
#Ex.7: (450, 15000)
##############################################################
def algorithm_2(config, example, n_machines, n_pulls):
    """Alternating between random machines and using calculating max probability among all machines
       this way changes in machine probabilities can be detected."""
    n_positive = 0
    n_all = 0
    percent_random = 0.1
    percent_prob = 0.2
    rand = 1    #number of iterations where machine probability is determined
    prob = 0    #number of iterations where machine probability is applied
    #machine probabilities (p, pos, all): p-cur. probability, pos-all positive, all
    pm = [[(0, 0, 0)]*n_machines]
    for pull in xrange(1, n_pulls+1):

        machine = (pull % n_machines if pull < (n_pulls*percent_random*rand + n_pulls*percent_prob*prob)
                   else pm[prob].index(max(pm[prob]))) + 1

        if pull >= n_pulls*percent_random*rand + n_pulls*percent_prob*(prob+1):
            rand += 1
            prob += 1
            #append new list for new estimations of probabilities
            pm.append([(0, 0, 0)] * n_machines)
            #print pm

        #print machine, pull
        response = get_pull_response(config["server"], example, machine, pull)
        #response = test_example(pull, machine)

        p, pos, all = pm[prob][machine-1]
        pos += response if response != -1 else 0
        all += (response != -1)
        pm[prob][machine-1] = (pos/float(all), pos, all)

        n_positive += response if response != -1 else 0
        n_all += (response != -1)
    return n_positive, n_all
#-----------------------------------------------------------#


def algorithm_2_2(config, example, n_machines, n_pulls):
    """Alternating between random machines and using calculating max probability among all machines
       this way changes in machine probabilities can be detected. Different parameters."""
    n_positive = 0
    n_all = 0
    percent_random = 0.1
    percent_prob = 0.3
    rand = 1    #number of iterations where machine probability is determined
    prob = 0    #number of iterations where machine probability is applied
    #machine probabilities (p, pos, all): p-cur. probability, pos-all positive, all
    pm = [[(0, 0, 0)]*n_machines]
    for pull in xrange(1, n_pulls+1):

        machine = (pull % n_machines if pull < (n_pulls*percent_random*rand + n_pulls*percent_prob*prob)
                   else pm[prob].index(max(pm[prob]))) + 1

        if pull >= n_pulls*percent_random*rand + n_pulls*percent_prob*(prob+1):
            rand += 1
            prob += 1
            #append new list for new estimations of probabilities
            pm.append([(0, 0, 0)] * n_machines)

        response = get_pull_response(config["server"], example, machine, pull)

        p, pos, all = pm[prob][machine-1]
        pos += response if response != -1 else 0
        all += (response != -1)
        pm[prob][machine-1] = (pos/float(all if all>0 else 1), pos, all)

        n_positive += response if response != -1 else 0
        n_all += (response != -1)
    return n_positive, n_all
#-----------------------------------------------------------#


##############################################################
##############################################################
def algorithm_3(config, example, n_machines, n_pulls):
    """Try to detect change in machine probability."""
    n_positive = 0
    n_all = 0
    percent_random = 0.06666
    percent_history = 0.06666
    random_length = int(n_pulls * percent_history)/2
    prob_threshold_value = 0
    prob_threshold_percent = 0.2
    start_prob = 0
    nr_random = n_pulls * percent_random   #number of random iterations
    #machine probabilities (p, pos, all): p-cur. probability, pos-all positive, all
    pm = [(0, 0, []) for i in xrange(n_machines)]
    for pull in xrange(1, n_pulls+1):
        machine = pull % n_machines + 1 if pull < nr_random else pm.index(max(pm)) + 1

        #response = get_pull_response(config["server"], example, machine, pull)
        response = test_example(pull, machine)

        prob, pos, hist = pm[machine-1]
        if response != -1:
            hist.append(response)
            pos += response
            prob = pos/float(len(hist))
            pm[machine-1] = (prob, pos, hist)
            n_positive += response
            n_all += 1

        if pull >= nr_random:
            #check if probabilities of machines have changed
            if len(hist) >= random_length:
                histprob = hist[-random_length:].count(1)/float(random_length)
                #print machine, pull, histprob, start_prob, prob_threshold_value
                if abs(start_prob-histprob) > prob_threshold_value:
                    nr_random = pull + n_pulls*percent_history
                    pm = [(0, 0, []) for i in xrange(n_machines)]
        else:
            start_prob = max(pm)[0]
            #threshold set to x% of current probability
            prob_threshold_value = start_prob*prob_threshold_percent

    return n_positive, n_all
#-----------------------------------------------------------#


##############################################################
##############################################################
def algorithm_4(config, example, n_machines, n_pulls):
    """[For testing] Draw chart showing probability of current machine through time."""
    n_positive = 0
    n_all = 0
    percent_random = 0.1
    percent_history = 0.1
    random_length = int(n_pulls * percent_history)/2
    prob_threshold_value = 0
    prob_threshold_percent = 1
    start_prob = 0
    nr_random = int(round(n_pulls * percent_random))   #number of random iterations
    #machine probabilities (p, pos, all): p-cur. probability, pos-all positive, all
    pm = [(0, 0, []) for i in xrange(n_machines)]
    a = 0
    p1 = []
    sp1 = []
    h1 = []
    h2 = []
    v = []
    pulse = []
    pulse2 = []
    diff = []
    hist2 = []
    sumprob = []
    for pull in xrange(1, n_pulls+1):
        machine = pull % n_machines + 1 if pull < nr_random else pm.index(max(pm)) + 1

        #response = get_pull_response(config["server"], example, machine, pull)
        response = test_example(pull, machine)

        prob, pos, hist = pm[machine-1]
        if response != -1:
            hist.append(response)
            pos += response
            prob = pos/float(len(hist))
            pm[machine-1] = (prob, pos, hist)
            n_positive += response
            n_all += 1

        def parts_prob(history, n):
            """Calculate probability for n equal parts from the values in history."""
            probs = []
            l = len(history)
            for i in xrange(n):
                h = history[i*l/n: (i+1)*l/n]
                probs.append(h.count(1)/float(len(h)))
            return probs

        if pull > nr_random:
            #check if probabilities of machines have changed
           # print prob, pos, len(hist), machine, pull
            a += 1
            if len(hist) >= random_length:
                histprob = hist[-random_length:].count(1)/float(random_length)

                hist2.append(histprob)
                aa.append(round(abs(histprob-start_prob), 5))
                p1.append(prob)
                sp1.append(start_prob)
                h1.append(histprob)
                v.append((prob+histprob))
                diff.append(abs(start_prob-histprob-0.01))
                sumprob.append(sum(p1)/float(len(p1)))

                if len(hist2)>1000:
                    h2.append(sum(hist2[-1000:])/1000)
                else:
                    h2.append(histprob)

        elif pull == nr_random:
            print "START", pull
            aa = []
            start_prob = prob
            start_prob_parts = parts_prob(hist, 3)
            #threshold set to x% of current probability
            prob_threshold_value = start_prob*prob_threshold_percent

    r = range(len(p1))
    print len(r), len(p1), len(sp1), len(h1), len(v), len(h2), len(diff)

    odv = []
    for i in range(len(h1)):
        if i<1:
            odv.append(0)
        else:
            odv.append((2*sp1[i]+h1[i])/3)

        if abs(sp1[i]-p1[i]) <= 0.015:
            pulse2.append(sp1[i])

        else:
            pulse2.append(p1[i])

        pulse.append((sp1[i]+p1[i])/2)

    #plt.plot(r, p1, "r", r, sp1, "b", r, h1, "g")
    #plt.show()
    return n_positive, n_all
#-----------------------------------------------------------#


def test_example(pull, machine):
    """[For testing]"""
    """if pull <= 2000:
        p = [0.02, 0.04, 0.06]
    elif pull <= 5000:
        p = [0.01, 0.03, 0.01]
    elif pull <= 10000:
        p = [0.06, 0.04, 0.02]
    elif pull <= 12000:
        p = [0.03, 0.02, 0.05]
    else:
        p = [0.02, 0.04, 0.04]"""
    if pull <= 6000:
        p = [0.02, 0.04]
    else:
        p = [0.05, 0.02]

    return 1 if random.random() <= p[machine-1] else 0


def algorithm_2_2_FINAL(config, example):
    """Same as algorithm_2_2, just different parameters for release version.
       Alternating between random machines and using calculating max probability among all machines
       this way changes in machine probabilities can be detected. Different parameters."""
    n_machines = get_number_of(config["server"], example, config["machines"])
    n_pulls = get_number_of(config["server"], example, config["pulls"])
    if n_machines == -1 or n_pulls == -1:
        return -1

    n_positive = 0
    n_all = 0
    percent_random = 0.1
    percent_prob = 0.3
    rand = 1    #number of iterations where machine probability is determined
    prob = 0    #number of iterations where machine probability is applied
    #machine probabilities (p, pos, all): p-cur. probability, pos-all positive, all
    pm = [[(0, 0, 0)]*n_machines]
    for pull in xrange(1, n_pulls+1):

        machine = (pull % n_machines if pull < (n_pulls*percent_random*rand + n_pulls*percent_prob*prob)
                   else pm[prob].index(max(pm[prob]))) + 1

        if pull >= n_pulls*percent_random*rand + n_pulls*percent_prob*(prob+1):
            rand += 1
            prob += 1
            #append new list for new estimations of probabilities
            pm.append([(0, 0, 0)] * n_machines)

        response = get_pull_response(config["server"], example, machine, pull)

        p, pos, all = pm[prob][machine-1]
        pos += response if response != -1 else 0
        all += (response != -1)
        pm[prob][machine-1] = (pos/float(all if all > 0 else 1), pos, all)

        n_positive += response if response != -1 else 0
        n_all += (response != -1)
    return n_positive, n_all
#-----------------------------------------------------------#


if __name__ == "__main__":
   # start = time.time()
   # print "Random:"
   # print evaluate(config, random_machine)

   # print "Algorithm 1"
   # print evaluate(config, algorithm_1)

   # print "Algorithm 2"
   # print evaluate(config, algorithm_2)

   # print "Algorithm 2_2"
   # print evaluate(config, algorithm_2_2)

   # evaluate_test(15000, 1, algorithm_4)

   # end = time.time()
   # print "Evaluated in ", (end - start)
    args = sys.argv
    if len(args) < 2:
        print "Not enough arguments. To run a program specify location of the server: pytohn Jackpot.py 'http://<ime_domene>/<stevilka_primera>'"
    else:
        try:
            server = args[1].replace("'", "").replace('"', "").split("/")
            config["server"] = "/".join(server[:-1 if server[-1] != "" else -2])
            example = int(server[-1 if server[-1] != "" else -2])

            is_print = True
            if len(args) == 3:
                try:
                    is_print = False if args[2]=="False" else True
                except Exception:
                    print "Form of the third argument is wrong. It should be True, False or blank"
                    print "pytohn Jackpot.py 'http://<ime_domene>/<stevilka_primera> False"
                    print "By default it is set to True. It is not necessary to specify this argument."

            result = algorithm_2_2_FINAL(config, example)
            if result == -1:
                print "Error trying to get number of machines or number of pulls. Check if number of the example exists."
            elif is_print:
                print result[0]

        except ValueError:
            print "<stevilka_primera> should be integer"
        except Exception as e:
            print "Form of the second argument is wrong. It should be as 'http://<ime_domene>/<stevilka_primera>'."