# Tp3 
import sys





print("ingrese nombre del archivo")
ruta = input()
if ruta == "1": 
	ruta = "Wiki-parsed.txt"
print("ingrese cantidad ")
n = input()

archivo_txt = open(ruta, encoding= "utf8")

for i in range(0,int(n)):
	linea = archivo_txt.readline().encode("utf-8")	
	if linea: print(linea) 




archivo_txt.close()