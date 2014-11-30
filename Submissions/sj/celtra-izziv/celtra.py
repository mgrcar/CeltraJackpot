import urllib2
import time
import sys

def send_request(url):
    """
    Poslje HTTP zahtevo na dan url ter vrne odgovor kot celo stevilo.
    """
    while True:
        try:
            answer = int(urllib2.urlopen(url).read())
            return answer
        except IOError:
            time.sleep(0.1)
            continue

def select_machine():
    """
    Izbere trenutno najboljsi avtomat ter vrne njegovo stevilko in natancnost.
    """
    global num_pull
    global num_hits
    hits_per_machine  = {i:0 for i in range(1,machines+1)}
    c=0
    #Ponavljamo dokler ne izlocimo vseh razen enega avtomata
    while(len(hits_per_machine)>1):
        for machine_num in hits_per_machine:
            #Avtomate potegujemo v serijah vsakega po 5
            for i in range(0,ELIMINATION_THRESHOLD):
                #Med izbiranjem avtomata nam lahko zmanjka stevilo potegov
                if num_pull>pulls:
                    return
                #Posiljanje zahteve ter zapomnitev rezultata
                pull =send_request(example_url+"/"+str(machine_num)+"/"+str(num_pull))
                hits_per_machine[machine_num] += pull
                num_hits += pull
                num_pull += 1
        max_hits = max(hits_per_machine.values())
        for machine_num, machine_hits in hits_per_machine.items():
            #Avtomate, ki imajo 5 potegov manj, kot trenutno najboljsi avtomat izlocimo
            if(machine_hits <= max_hits - ELIMINATION_THRESHOLD):
                del hits_per_machine[machine_num]
        c+=1
    if num_pull>pulls:
        return
    return (hits_per_machine.keys()[0],max_hits/(c * ELIMINATION_THRESHOLD))

#inicializacija konstant ter ostalih globalnih spremenljivk
ELIMINATION_THRESHOLD = 5;
SENSITIVITY = 0.5;
RESELECT_M_EVERY = 1000;

example_url = sys.argv[1]
num_pull = 1
num_hits = 0
machines = send_request(example_url+"/machines")
pulls = send_request(example_url+"/pulls")

last_pulls = list()
best_machine = 0
while num_pull<=pulls:
    if len(last_pulls)==300 or not best_machine:
        last_pulls_accuracy = sum(last_pulls)/300.0
        #Izberemo najboljsi avtomat, v primeru ce se nimamo izbranega avtomata
        #ali se je natancnost avtomata opazno spremenila ali pa ze dolgo nismo izbrali najboljsega avtomata
        if not best_machine or\
           last_pulls_accuracy<=best_machine_accuracy*(1.0-SENSITIVITY) or \
           last_pulls_accuracy>=best_machine_accuracy*(1.0+SENSITIVITY) or \
           since_last_machine_select>=RESELECT_M_EVERY:
                machine_result = select_machine()
                #Med izbiro avtomata nam lahko zmanjka stevilo potegov
                if(not machine_result):
                    break
                best_machine = machine_result[0]
                best_machine_accuracy = machine_result[1]
                since_last_machine_select = 0
                last_pulls = list()
        else:
            #Hranimo zadnjih 300 potegov na izbranem avtomatu
            del last_pulls[0]
    #Poteg avtomata ter pomnjenje rezultata
    pull = send_request(example_url+"/"+str(best_machine)+"/"+str(num_pull))
    last_pulls.append(pull)
    num_hits += pull
    num_pull += 1
    since_last_machine_select += 1
