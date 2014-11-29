jackpot - How much money does you algorithm make?
================================================

This is a solution for Celtra challenge. The goal is to write an algorithm, which could autonomously
select the most rewarding slot machine. Game settings are very easy. User has limited number of pulls and
he should select the most rewarding slot machine to maximise his profit.

Run an algorithm
================
1. Install python 2.7
2. Run command
```
python jackpot.py http://<host_name>/<example_number>
```

Celtra Jackpot API
===========
1. Get number of machines for given example
```
#Request
http://celtra-jackpot.com/3/machines
#Response
2
```
2. Get number of pulls for given example
```
#Request
http://celtra-jackpot.com/3/pulls
#Response
10000
```
3. Pull slot machine for given example and sequence number
```
#Request http://<host_name>/<example_number>/<slot_machine_number>/<sequence_number>
http://celtra-jackpot.com/3/1/1
#Response (0 or 1)
0
```
In case that you would like to run Jackop API locally, open directory server-local for further information

Development Requirements
========================
We have used some external libraries during development phase. You should be able to run all scripts in this
 repository by following these two steps.

1. Install python 2.7 & pip
2. Run command
```
pip install -r requirements.txt
```


