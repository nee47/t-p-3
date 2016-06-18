# Tp3 
import sys
from bs4 import BeautifulSoup




print("ingrese nombre del archivo")
ruta = input()
if ruta == "1": 
	ruta = "Wiki-parsed.txt"
print("ingrese cantidad ")
n = input()

archivo_txt = open(ruta, encoding= "utf8")
repetidos = 0

for i in range(0,int(n)):
	linea = archivo_txt.readline()#.encode("utf-8")	
	soup = BeautifulSoup(linea, "html.parser")
	if soup.text.find("avena") != -1:
		repetidos += 1
	if linea: print(soup.text)#.encode("utf-8")) 
print("CANTIDAD REPETIDOS",repetidos)



archivo_txt.close()