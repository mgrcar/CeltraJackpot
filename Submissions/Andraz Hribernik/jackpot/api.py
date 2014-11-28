from urllib2 import Request, urlopen, URLError

MACHINES = "machines"
PULLS = "pulls"


class JackpotApi:
    def __init__(self, url):
        """
        Initialise JackpotApi class with parameter url
        :param url: jackpot api host name
        """
        self.url = url
        self.machines = self.call(MACHINES)
        self.pulls = self.call(PULLS)

    def call(self, param):
        """
        Create http request on jackpot api using param
        :param param: value that is sent through http request
        :return: int value returned from http request
        """
        url = "{}/{}".format(self.url, param)
        consecutive_err = 0
        while True:
            try:
                response = urlopen(url)
                return int(response.read())
            except URLError as e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                    print url
                elif hasattr(e, 'code'):
                    print 'The server couldn\'t fulfill the request.'
                    print 'Error code: ', e.code
                consecutive_err += 1
            except:
                consecutive_err += 1
            if consecutive_err > 5:
                print "Program has been stopped due to max. number of consecutive errors was reached."
                exit()

    def pull(self, bandit, sequence_n):
        """
        Pull :bandit with :sequence_n and receive reward 1 or 0
        :param bandit: slot machine number
        :param sequence_n:
        :return: slot machine reward (1 or 0)
        """
        return self.call("{}/{}".format(bandit, sequence_n))
