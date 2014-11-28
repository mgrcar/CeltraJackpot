# README #

This is an application developed for Celtra student challenge 2014. I picked the first challenge; it is explained on http://www.celtra-jackpot.com/ (Slovene only).

### How do I get set up? ###

To run this application you need to install Python. It comes preinstalled on UNIX/Linux systems, for Windows installation check Python official web page (do not forget to set environment variable PYTHONPATH).
To check if you have Python, open terminal or command prompt (console) and type "python". If there is no error, Python interpreter should show up (to exit interpreter write quit()).     

After downloading the application move in your console to the downloaded directory. There should be file Jackpot.py. To run this file execute command: *python Jackpot.py "http://<ime_domene>/<številka_primera\>"* where *<ime_domene\>* is the name of the domain where the server for generating *pulls* is located and *<številka_primera\>* is number of the example to be run.
By default the application prints to the standard output number of positive responses (number of all responses with value 1). To disable this behaviour you can run the application with additional parameter: *python Jackpot.py "http://<ime_domene>/<številka_primera\>" False*

### Recap: ###
* run with print on:
*python Jackpot.py "http://<ime_domene>/<številka_primera\>"*

* run with print off:
*python Jackpot.py "http://<ime_domene>/<številka_primera\>" False*

### Who do I talk to? ###

* Repo owner