##1.1
###Improvement
 - Epsilon-decreasing variation applied.

##1.0
###Big Improvement
 - Machine choosing is now done by Multi-armed Bandit strategy.
 - Epsilon-greedy variation applied.

##0.1
First release
###The idea
 - reads number of pulls and number of machines 
 - determine the minimal reasonable number for start pulls 
 - serial pulling the machines until start pulls are reached, determine the most profitable machine
 - exploits the most profitable machine, until it's ratio doesn't fall below the next profitable one

### Conclusion
 - not effective - the best approximation isn't really needed here