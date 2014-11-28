import urllib2
import urllib
import socket

#get number of machines available in the case
def getNumMachines(server,case):
    try:
        response = urllib2.urlopen("http://"+server+"/" + str(case) + '/machines')
        numMachines = response.read()
        if numMachines != 'ERR':
            return int(numMachines)
    except urllib2.URLError as e:
        #print e.reason
        #print '\n'
        return -1
    return -1

#get number of pulls available in the case
def getNumPulls(server,case):
    try:
        response = urllib2.urlopen("http://"+server+"/" + str(case) + '/pulls')
        numPulls = response.read()
        if numPulls != 'ERR':
            return int(numPulls)
    except urllib2.URLError as e:
        #print e.reason
        #print '\n'
        return -1
    return -2
   
def connect(server):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, 80))
    except:
        print "Could not connect to server!"
        return None
    return s

def disconnect(s):
    s.close()


def getMachineResponse(s, server, case, machine, pull):
    args=str(case)+'/'+str(machine)+'/'+str(pull)
    try:
        s.send("GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n" % (args, server))
        data = s.recv(1024)
        if data:
            data.split("\n\r")
            data=data[-1]
            if data != 'ERR':
                return int(data[-1])
    except:
        disconnect(s)
        s.connect((server,80))
        return -1
    return -2


#pull the machine and get response   
#def getMachineResponse(case, machine, pull):
#    try:
#        response = urllib2.urlopen('http://celtra-jackpot.com/' + str(case) + '/' + str(machine) + '/' + str(pull))
#        pullResponse = response.read()
#        if pullResponse != 'ERR':
#            return int(pullResponse)
#    except urllib2.URLError as e:
#        #print e.reason
#        #print '\n'
#        return -1
#    return -2