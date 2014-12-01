__author__ = 'p'
import requests
import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import threading
from time import sleep
from multiprocessing.dummy import Pool as ThreadPool
import random
from collections import deque
import sys
def get_all_data():
    primer_avtomat_poteg = []
    thread_list = []
    urls = []
    pool = ThreadPool(50)
    for primer in range(10):
        primer_avtomat_poteg.append([])
        print('http://celtra-jackpot.com/'+str(primer+1)+'/machines')
        r = requests.get('http://celtra-jackpot.com/'+str(primer+1)+'/machines')
        p = (int(requests.get('http://celtra-jackpot.com/'+str(primer+1)+'/pulls').text))
        print(p)
        for avtomat in range(int(r.text)):
            primer_avtomat_poteg[primer].append([])
            print(avtomat+1)
            for poteg in range(p):
                primer_avtomat_poteg[primer][avtomat].append([])
                # print ('http://celtra-jackpot.com/'+str(primer+1)+'/'+str(avtomat+1)+'/'+str(poteg+1))
                # print(int(requests.get('http://celtra-jackpot.com/'+str(primer+1)+'/'+str(avtomat+1)+'/'+str(poteg+1)).text))
                #t = threading.Thread(target=worker, args=(primer, avtomat, poteg))

                #thread_list.append(t)
                #urls.append('http://celtra-jackpot.com/'+str(primer+1)+'/'+str(avtomat+1)+'/'+str(poteg+1))
                sleep(0.008)
                primer_avtomat_poteg[primer][avtomat][poteg] = threading.Thread(target=worker2,args=('http://celtra-jackpot.com/'+str(primer+1)+'/'+str(avtomat+1)+'/'+str(poteg+1),0))
                primer_avtomat_poteg[primer][avtomat][poteg] = primer_avtomat_poteg[primer][avtomat][poteg].start()
    # for thread in thread_list:
    #     if
    #     thread.start()
    #
    #
    # for thread in thread_list:
    #     thread.join()
    #results = pool.map(worker2, urls)


    pickle.dump(primer_avtomat_poteg, open("./pickle6",'wb'))
    # primer_avtomat_poteg = pickle.load(open("./pickle", "rb"))
    # print(primer_avtomat_poteg[4][2][7440:8442])
    # for primer in primer_avtomat_poteg:
    #     for avtomat in primer:
    #         for poteg in avtomat[]:
    #             print(sum)


def worker(primer, avtomat, poteg):
    try:
        a = int(requests.get('http://celtra-jackpot.com/'+str(primer+1)+'/'+str(avtomat+1)+'/'+str(poteg+1)).text)
    except:
        print (primer, avtomat, poteg, "NAPAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        sleep(3)
        return worker(primer, avtomat, poteg)
    print(primer+1, avtomat+1, poteg+1, a)
    return a

def worker2(a,x=0):
    try:
        b = int(requests.get(a).text)
        print(a, b, x)
    except:
        print (a, "NAPAKAAA", x)
        sleep(5)
        return worker2(a, x+1)
    return b


def compose_pickles():
    p = []
    p.append(pickle.load(open("./pickle", "rb")))
    p.append(pickle.load(open("./pickle2", "rb")))
    p.append(pickle.load(open("./pickle3", "rb")))
    p.append(pickle.load(open("./pickle4", "rb")))
    for i in range(1,4):
        for je,j in enumerate(p[i]):
            for ke, k in enumerate(j):
                for le, l in enumerate(k):
                    p[0][je][ke][le] += p[i][je][ke][le]
    primer = 5
    pl = plt
    pl.figure(figsize=(25,1) )
    for i in range(len(p[0][primer])):
        x= p[0][primer][i]
        smoothed = np.convolve(x, np.ones(100), mode='same')
        pl.plot(x, hold=True)
        pl.plot(smoothed, hold=True)

    pl.show()

def get_value_on():
    sum = 0
    n = 111
    for i in range(n):
        sum += int(requests.get('http://celtra-jackpot.com/'+str(7)+'/'+str(1)+'/'+str(101)).text)
    print(sum/n)

def st_prim_avt_pot():
    for primer in range(10):
        r = requests.get('http://celtra-jackpot.com/'+str(primer+1)+'/machines')
    p = (int(requests.get('http://celtra-jackpot.com/'+str(primer+1)+'/pulls').text))
    print('http://celtra-jackpot.com/'+str(primer+1)+'/machines')
    print(p)
    print(int(r.text))

def emulator(primer, avtomat, poteg):
    if primer == 1:
        if avtomat == 1:
                return random.random() < 0.3875
        elif avtomat == 2:
                return random.random() < 0.611
        else:
            return ("ni takega avtomata!")
    elif primer == 2:
        if avtomat == 1:
            return random.random() < 0.029975
        elif avtomat == 2:
            return random.random() < 0.0135
        else:
            return ("ni takega avtomata!")
    elif primer == 3:
        if avtomat == 1:
            return random.random() < 0.19775
        elif avtomat == 2:
            return random.random() < 0.15075
        elif avtomat == 3:
            return random.random() < 0.103
        else:
            return ("ni takega avtomata!")
    elif primer == 4:
        if avtomat == 1:
            return random.random() < 0.018725
        elif avtomat == 2:
            return random.random() < 0.01925
        elif avtomat == 3:
            return random.random() < 0.02505
        elif avtomat == 4:
            return random.random() < 0.0227
        else:
            return ("ni takega avtomata!")
    elif primer == 5:
        if avtomat == 1:
            return random.random() < 0.00985
        elif avtomat == 2:
            return random.random() < 0.009825
        elif avtomat == 3:
            return random.random() < 0.009625
        elif avtomat == 4:
            return random.random() < 0.009425
        elif avtomat == 5:
            return random.random() < 0.01005
        elif avtomat == 6:
            return random.random() < 0.009925
        elif avtomat == 7:
            return random.random() < 0.010525
        elif avtomat == 8:
            return random.random() < 0.01055
        elif avtomat == 9:
            return random.random() < 0.010975
        elif avtomat == 10:
            return random.random() < 0.01315
        else:
            return ("ni takega avtomata!")
    elif primer == 6:
        if avtomat == 1:
            if poteg<500:
                return random.random() < 0.4
            else:
                return random.random() < 0.6
        elif avtomat == 2:
            if poteg>500:
                return random.random() < 0.6
            else:
                return random.random() < 0.4
        else:
            return ("ni takega avtomata!")
    elif primer == 7:
        if avtomat == 1:
            if poteg >3500 and poteg <11500:
                return random.random() < 0.04
            else:
                return random.random() < 0.02
        elif avtomat == 2:
            if poteg >3500 and poteg <11500:
                return random.random() < 0.02
            else:
                return random.random() < 0.032
            return ("ni takega avtomata!")
    elif primer == 8:
        if avtomat == 1:
            if poteg >1500 and poteg <2250:
                return random.random() < 0.3
            elif poteg > 2250:
                return 0
            else:
                return random.random() < 0.015
        elif avtomat == 2:
            if poteg >1500 and poteg <2250:
                return random.random() < 0.0
            else:
                return random.random() < 0.02
        elif avtomat == 3:
            return random.random() < 0.09525
        else:
            return ("ni takega avtomata!")
    elif primer == 9:
        if avtomat == 2 or avtomat == 4:
            return 0
        if avtomat == 1 or avtomat == 3:
            if poteg > 12000:
                return random.random() < 0.020
        else:
            return ("ni takega avtomata!")
    elif primer == 10:
        if avtomat == 1 or avtomat == 2 or avtomat == 7 or avtomat == 8:
            if poteg > 6000 and poteg <12000:
                return random.random() < 0.02
            else:
                return random.random() < 0.01
        if avtomat == 3 or avtomat == 9 or avtomat == 10:
            if poteg > 12000 and poteg <24000:
                return random.random() < 0.02
            else:
                return random.random() < 0.01
        if avtomat == 4 or avtomat == 5 or avtomat == 6:
            if poteg > 24000:
                return random.random() < 0.02
            else:
                return random.random() < 0.01
        else:
            return ("ni takega avtomata!")


def delezi_pravilnih_potegov():
    p = []
    p.append(pickle.load(open("./pickle", "rb")))
    p.append(pickle.load(open("./pickle2", "rb")))
    p.append(pickle.load(open("./pickle3", "rb")))
    p.append(pickle.load(open("./pickle4", "rb")))
    for i in range(1,4):
        for je, j in enumerate(p[i]):
            for ke, k in enumerate(j):
                for le, l in enumerate(k):
                    p[0][je][ke][le] += p[i][je][ke][le]

    for primer in range(10):
        for avtomat in range(len(p[0][primer])):
            print("avtomat",avtomat,"primer", primer)
            iskani = p[0][primer][avtomat]
            print (len(iskani), sum(iskani)/4, (sum(iskani)/4)/len(iskani))

def igralec(primer):
    m = int(requests.get('http://celtra-jackpot.com/'+str(primer)+'/machines').text)
    p = int(requests.get('http://celtra-jackpot.com/'+str(primer)+'/pulls').text)
    print(m, p)
    ###parametri###
    resolucija = 7
    abs_resolucija = int(p/resolucija)
    round_robin_length = int(abs_resolucija/2)
    obcutljivost = 2

    avtomat_poteg = []
    potegi = [None for i in range(p)]
    counter = 0
    mov_avg_values= [0 for i in range(p)]

    def pull_until_change(avtomat, counter):
        print("menjam na:",avtomat)
        while counter < p:                                               #vleci dokler lahko
            print(counter)
            zadnjih_x = 0
            if counter-abs_resolucija >0:
                zadnjih_x = counter-abs_resolucija
            mov_avg_sect= potegi[zadnjih_x:counter]
            mov_avg_values[counter] = sum(mov_avg_sect)/len(mov_avg_sect)
            if  mov_avg_values[counter]*obcutljivost < mov_avg_values[int(zadnjih_x/2)]:
                pull_until_change(avtomat +1, counter)
            else:
                potegi[counter] = int(requests.get('http://celtra-jackpot.com/'+str(primer)+'/'+str(avtomat+1)+'/'+str(counter+1)).text)
                avtomat_poteg[avtomat][counter] = potegi[counter]
                counter +=1
        return

    for avtomat in range(m):
        avtomat_poteg.append([-10000 for i in range(p)])
        for poteg in range(round_robin_length):
            potegi[counter] = int(requests.get('http://celtra-jackpot.com/'+str(primer)+'/'+str(avtomat+1)+'/'+str(counter+1)).text)
            avtomat_poteg[avtomat][counter] = potegi[counter]
            counter += 1
    zacetni_avtomat = 0
    zacet_vred = 0
    for a1, avtomat in enumerate(avtomat_poteg):
        if sum(avtomat) > zacet_vred:
             zacetni_avtomat = a1
    pull_until_change(zacetni_avtomat, counter)
    return sum(potegi)


def main(argv):
    #compose_pickles()
    #get_value_on()
    #get_all_data()
    print(argv, argv[1])
    print(igralec(argv[1]))

if __name__ == "__main__":
    main(sys.argv)

    exit(0)

