from urllib2 import Request, urlopen, URLError
import random
import sys


def choose_machine(last, val, history):
    if last >= 1:
        temp_list = list(history)
        temp_list.pop(last - 1)
        if val == 1:
            return last
        else:
            return history.index(max(temp_list)) + 1
    else:
        return random.randint(1, len(history))


def call_api(conn_string):
    request = Request(conn_string)

    try:
        response = urlopen(request)
        api_answer = response.read()
        return int(api_answer)
    except URLError, e:
        print 'API crashed :(', e


try:
    comand_line_argument = str(sys.argv[1])
except:
    print "Fail"
    exit(0, 1)


number_of_machines = call_api(comand_line_argument + 'machines')
number_of_pulls = call_api(comand_line_argument + 'pulls')

history_of_wins = [0.0] * number_of_machines
history_of_pulls = [0.0] * number_of_machines

last_machine = 0
last_val = 0
for pull_number in range(1, number_of_pulls + 1):

    history = []
    for a, b in enumerate(history_of_wins):
        if history_of_pulls[a] == 0.0:
            history.append(0.0)
        else:
            history.append(history_of_wins[a]/history_of_pulls[a])

    machine_number = choose_machine(last_machine, last_val, history)
    buff = comand_line_argument + str(machine_number) + '/' + str(pull_number)
    answer = call_api(buff)

    last_machine = machine_number
    last_val = answer
    history_of_wins[last_machine - 1] += last_val
    history_of_pulls[last_machine - 1] += 1

print 'Od ' + str(number_of_pulls)
print ' primerov, sem zadel ' + str(sum(history_of_wins)) + '\n' +'z natancnostjo: '
print sum(history_of_wins) / number_of_pulls
