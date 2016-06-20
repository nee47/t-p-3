# Tp3 
import sys

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0
class Cola():
    def __init__(self):
        self.datos = []

    def vacia(self):
        return len(self.datos) == 0

    def encolar(self, dato):
        self.datos.append(dato)
        return True

    def ver_tope(self):
        return self.datos[0]

    def desencolar(self):
        if self.vacia(): return None
        return self.datos.pop(0)

class Pila():
    def __init__(self):
        self.datos = []

    def vacia(self):
        return len(self.datos) == 0

    def apilar(self, dato):
        self.datos.append(dato)

    def desapilar(self):
        if self.vacia(): return None
        return self.datos.pop()    

def detener(actual, padre, orden, fin):
        if actual == fin:
            return False;

# pila = Pila()
# if pila.vacia()
# pila->destruir()
class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
    
    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
        self.__vertices = {}
        self.__datos = {}
        self.__dirigido = es_dirigido
        self.__aristas = {}
    #  { joseph : {Vilca: peso} }
    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return len(self.__vertices)
    
    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
        raise NotImplementedError()
        
    def keys(self):
        '''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
        return list(self.__vertices)
    
    
    def __getitem__(self, id):
        '''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
        return self.__datos[id]

    def __setitem__(self, id, valor):
        '''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
        En caso qe el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
        '''
        if not id in self.__vertices:
            self.__vertices[id] = []
        self.__datos[id] = valor
        self.__aristas[id] = {}
        return True
    
    def __delitem__(self, id):
        '''Elimina el vertice del grafo, y devuelve el valor asociado. Si no existe el identificador en el grafo, lanzara KeyError.
        Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
        '''
        for clave in self.__vertices[id]:
            if id in self.__vertices[clave]:
                self.__vertices[clave].remove(id)
        dato_salida = self.__datos[id]
        del self.__datos[id]
        del self.__aristas[id]
        del self.__vertices[id]
        return dato_salida
    
    def __contains__(self, id):
        ''' Determina si el grafo contiene un vertice con el identificador indicado.'''
        return id in self.__vertices
        
    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        self.__vertices[desde].append(hasta)
        #self.__aristas[desde] = {}
        self.__aristas[desde][hasta] = peso 
        if not self.__dirigido :
            self.__vertices[hasta].append(desde)
         #   self.__aristas[hasta] = {}
            self.__aristas[hasta][desde] = peso
        return True

    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
        '''
        self.__vertices[desde].remove(hasta)
        if self.__dirigido :
            self.__vertices[hasta].remove(desde)
        del self.__aristas[desde][hasta]

    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        if hasta not in self.__vertices[desde] : #or desde not in self.__vertices[hasta]:         
            return None
        return self.__aristas[desde][hasta]
        
    def adyacentes(self, id):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
        return self.__vertices[id]
    
    def bfs(self, visitar = visitar_nulo, extra = None, inicio=None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar   )
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
        '''
        visitados = {}
        for elemento in self.keys():
            visitados[elemento] = False
        fin = False
        #lista = []
        cola = Cola()
        cola2 = Cola()
        cola.encolar(inicio)
        padre = {}
        orden =  {}    
        ordencito = 0
        #print("EN|TRE ACA")
        while not cola.vacia() and not fin: 
            #print("Principio")
            #print("veer tope",cola.ver_tope())
            if visitar:
                if visitar(cola.ver_tope(), padre, orden, extra) == False:
                    fin = True
            #if fin : continue
            #print("pase ")

            v = cola.desencolar()
            #print(self.__vertices[v])
            #print("DESENCOLADO V : ", v)
            if not visitados[v]:
                visitados[v] = True
                if inicio == v :
                     padre[v] = None
                else:
                    padre[v] = cola2.desencolar()                    
                orden[v] = ordencito
                ordencito += 1
                #lista.append(v)
                desencolado = padre[v]
                if desencolado and len(self.__vertices[desencolado]) > 1:
                    cola2.encolar(desencolado)
                    #print("toy aki")
                else:
                    cola2.encolar(v)
                #print("MOSTRAR COLA2", cola2.datos)
                #print("VISITADOS", visitados)
                #print("par w en adyacentes")
                for w in self.__vertices[v]:
                    #print("EL VERTICE QUE TOMO ES:", w)
                    if not visitados[w]:
                        cola.encolar(w)
                        #print(w)	
        return (padre, orden)

    def dfs_visitar(self, w, padre, orden, ordencito, visitados, inicio):
        visitados[w] = True
        ordencito[0] += 1
        orden[w] = ordencito[0]
        for v in self.__vertices[w]:
            if not visitados[v]:
                if w != inicio:
                    padre[v] = w
                else:
                    padre[v] = None
                self.dfs_visitar(v, padre, orden, ordencito, visitados, inicio )
        #visitados[w] = True
        #ordencito[0] += 1       
    #Aun no funciona    
    def dfs(self, visitar = visitar_nulo, extra = None, inicio=None):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
        '''
        visitados = {}
        for clave in self.__vertices:
            #print("clave", clave)
            visitados[clave] = False
        #print(visitados)
        padre = {}
        orden = {}
        ordencito = [0]
        
        #if not visitados[w]:
        self.dfs_visitar(inicio, padre, orden, ordencito, visitados, inicio)   

        return (padre, orden)
    
    def componentes_conexas(self):
        '''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
        Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
        en caso de aplicarse a un grafo dirigido se lanzara TypeError'''
        raise NotImplementedError()
    

    def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
        A* en caso que la heuristica no sea nula. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None. 
        '''
        t = self.bfs(detener, destino, origen)
        d = t[0]
        #lista = 
        #while x :
        #print("padres:", t[0])
        output = []
        fin = False
        insertar = destino
        #print(t[0])
        while insertar:            
            output.insert(0, insertar)
            #print("AKA")
            insertar = d.get(insertar)

        #print("ordenes :", t[1])
        return output
        
    
    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        raise NotImplementedError()


    def mostrar(self):
        print("GRAFO VERTICES", self.__vertices)
        #print("GRAFO DATOS", self.__datos)
        #print("GRAFO ARISTAS", self.__aristas)
        print("GRAFO LEN ", self.__len__())


def lista_lineas(archivo):
	linea = archivo.readline()
	longitud = len(linea)
	vec_linea = linea[0: longitud-1].split("<")
	fin = vec_linea[0].find(">")
	vec_linea.insert(0, vec_linea[0][0: fin])
	vec_linea[1] = vec_linea[1][fin+1:]
	return vec_linea


print("ingrese nombre del archivo")
ruta = input()
if ruta == "1": 
	ruta = "Wiki-parsed.txt"
print("ingrese cantidad ")
n = input()

archivo_txt = open(ruta, encoding= sys.stdout.encoding, errors = "utf8")
grafo = Grafo(True)
valor = 1
for x in range(0, int(n)):
	vec = lista_lineas(archivo_txt)
	#print(vec)
	grafo.__setitem__(vec[0], valor)
	for elemento in vec:
		grafo.__setitem__(elemento, valor)
		grafo.agregar_arista(vec[0], elemento)
		


vert = grafo.keys()
#grafo.mostrar()
print("actualmente hay ", grafo.__len__(),"vertices")
print("INGRESA CUANTOS VERITCES validos KIERS VER")
vert_cant=input()
cun = 0
cm= 0
while cm < grafo.__len__() and cun< int(vert_cant):
	adya = grafo.adyacentes(vert[cm])
	while(cm+2 < grafo.__len__() and len(adya) < 10):
		cm += 1
		adya = grafo.adyacentes(vert[cm])
	#cm += 1
	cun += 1	
	print(vert[cm])
	cm += 1

print("INGRESA ORIGEN")
a = input()
print(a)
print("Ingresa destino")
b = input()
print(b)
while not grafo.__contains__(a) or not grafo.__contains__(b):
	print("INGRESA ORIGEN")
	a = input()
	print("Ingresa destino")
	b = input()


l = grafo.camino_minimo(a, b)
print(l)
archivo_txt.close()