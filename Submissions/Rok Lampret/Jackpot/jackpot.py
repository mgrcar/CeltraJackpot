#Rok Lampret
#Python3.4

#\imports
from urllib.request import urlopen
import sys
#imports/

#/methods
def testiraj_konstantnost():
	global prvi_procenti, zgodovina_procent

	for i,j in zip(prvi_procenti, zgodovina_procent):
		if (i - j) > (1.0/dolzina_zgodovine):
			return False

	return True

def poteg(masina): #simulira poteg -> poslje url na masino v argumentu, vrne 0/1 = uspeh potega
	global trenuten_poteg, rez, url
	print(trenuten_poteg)
	trenuten_poteg += 1

	val = preberiURL(url+"{}/{}".format(masina,trenuten_poteg), 3)

	if val == 1:
		rez += 1

	return val

def izracunaj_procent(masina): #izracuna procent za dano masino (vsota/dolzina)
	global zgodovina_procent, dolzina_zgodovine

	zgodovina_procent[masina-1] = sum(zgodovina[masina-1])/float(dolzina_zgodovine)

def resetiraj_zgodovino(): #zaporedno za vsako masino na novo napolni zgodovino potegov in popravi procente
	global trenuten_poteg, st_potegov, rez, zgodovina, url	
	
	for masina in range(1, st_masin+1):
		for p in range(0, dolzina_zgodovine):
			if trenuten_poteg < st_potegov:			
				zgodovina[masina-1][p] = poteg(masina)
			else:
				break

	for i in range(1, st_masin+1):
		izracunaj_procent(i)

def preberiURL(url, bitn): #odpre url, prebere bitn bitov, zapre preveri za napako, vrne odgovor na zahtevek
	f = urlopen(url)
	data = f.read(bitn)
	f.close()

	if data == "ERR":
		napaka("err: "+url)

	return int(data)

def napaka(msg): #printa napako in zakljuci program
	print(msg)
	exit()

def dolociDolzinoZgodovine():
	global st_potegov

	return int(8 + (st_potegov/2500))

def dolociStReset():
	global st_masin, st_potegov, dolzina_zgodovine
	return int((0.2*st_potegov)/(st_masin*dolzina_zgodovine))
#methods/

#/vars
if len(sys.argv) > 1:
	url = sys.argv[1]
else:
	url = input("URL: ")
if url[-1] != "/":
	url = url + "/"

st_masin = preberiURL(url+"machines", 3)
st_potegov = preberiURL(url+"pulls", 5)
dolzina_zgodovine = dolociDolzinoZgodovine()
st_reset = dolociStReset()
zgodovina = [0] * dolzina_zgodovine #belezi zgodovino za zadnjih n potegov
zgodovina = [zgodovina] * st_masin # belezi potege za vsako masino
zgodovina_procent = [0] * st_masin
prvi_procenti = []
rez = 0
trenuten_poteg = 0
#vars/

#/algoritem
resetiraj_zgodovino()

prvi_procenti = zgodovina_procent;

while trenuten_poteg < st_potegov:
	m = zgodovina_procent.index(max(zgodovina_procent)) + 1 #plus ena zaradi zamika indexa
	
	zgodovina[m-1].append(poteg(m))
	zgodovina[m-1].pop(0)

	izracunaj_procent(m)

	if trenuten_poteg%(st_potegov/st_reset) == 0 and\
	 trenuten_poteg != st_potegov and\
	 testiraj_konstantnost() == False:
		resetiraj_zgodovino()

print("uspesnih potegov: {0:d}/ procent: {2:.2f}%".format(rez, st_potegov, rez/float(st_potegov)*100))
#algoritem/
