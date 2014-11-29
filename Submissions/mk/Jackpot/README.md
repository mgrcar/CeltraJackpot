Jackpot
=======

Jackpot Challenge, Celtra 2014

##Algorithm
 - It works on the principle of the Multi-armed Bandit, Epsilon-decreasing.
 - Default epsilon (E) is 50% and it decreases by every pull.
 - In E% cases algorithm chooses a random machine (this part is called exploration) and in other cases algorithm chooses the most profitable machine (called exploitation).
 - Exploration: algorithm from time to time checks if it is exploiting the most profitable machine.
 - Exploitation: At the beginnig, all machines have 0% gain, by time it increases according to their profitability.

##Example
 - [0/0, 0/0, 0,0] =(I.)=> [0/1, 0/0, 0,0] =(II.)=> [0/1, 1/1, 0,0] =(II.)=> [0/1, 1/2, 0,0] =(III.)=> ...
 - We have 3 machines and the first one is randomly chosen.
 - The first machine is pulled, but it returns zero gain.
 - Zero gains of zero pulls (100%) is better than zero gains of one pull (0%), so the second machine is choosen.
 - A pull on second machine is successfull, so this the most profitable option (100%) to continue.
 - The next pull on second machine is not successfull, profitability is now 50%, so the third machine is chosen.
   
   


