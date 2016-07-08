# Tp3
# 97240 -James, Vilca
# 2016 

import sys
import heapq
from time import time

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

    def vacia(self)    :
        return len(self.datos) == 0

    def apilar(self, dato):
        self.datos.append(dato)

    def desapilar(self):
        if self.vacia(): return None
        return self.datos.pop()    

def detener(actual, padre, orden, fin):
        if actual == fin:
            return False;

class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
    
    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
        self.__vertices = {}
        self.__datos = {}
        self.__dirigido = es_dirigido
        self.__aristas = {}

    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return len(self.__vertices)
    
    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
        return iter(self.keys())
        
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
        if desde == hasta:
            return False
        self.__vertices[desde].append(hasta)
        self.__aristas[(desde, hasta)] = peso 
        if not self.__dirigido :
            self.__vertices[hasta].append(desde)
            self.__aristas[(hasta, desde)] = peso
        return True

    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
        '''
        self.__vertices[desde].remove(hasta)
        del self.__aristas[(desde, hasta)]
        if not self.__dirigido :
            self.__vertices[hasta].remove(desde)
            self.__aristas[(hasta, desde)]

    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        if hasta not in self.__vertices[desde] : 
            return None
        return self.__aristas[(desde, hasta)]
        
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
        distancia = {}
        for elemento in self.__vertices:
            visitados[elemento] = False
            distancia[elemento] = 9999
        
        fin = False
        cola = Cola()
        padre = {}
        orden =  {}    
        etapa = 0
        if inicio :
            padre[inicio] = None
            cola.encolar(inicio)
        else:
            for vertice in self.__vertices:
                cola.encolar(vertice)

        distancia[inicio] = 0 
        while not cola.vacia() and not fin: 
            v = cola.desencolar()
            if visitar:
                if visitar(v, padre, distancia, extra) == False:
                    fin = True
            if not visitados[v]:
                orden[v] = etapa
                etapa += 1
                visitados[v] = True
                if fin:
                    continue
                for w in self.__vertices[v]:
                    if not visitados[w]:
                        if distancia[w] > distancia[v] +1:
                            distancia[w] = distancia[v] + 1
                        cola.encolar(w)
                        padre[w] = v

        return (padre, orden, distancia)

    def dfs_visitar(self, w, padre, orden, etapa, visitados, inicio, visitar, extra):
        visitados[w] = True
        etapa[0] += 1
        orden[w] = etapa[0]
        if visitar and visitar(w, padre, orden, extra) == False:
            return 1
            
        for v in self.__vertices[w]:
            if not visitados[v]:
                if w != inicio:
                    padre[v] = w
                else:
                    padre[v] = None
                self.dfs_visitar(v, padre, orden, etapa, visitados, inicio, visitar, extra )

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
            visitados[clave] = False
        padre = {}
        orden = {}
        etapa = [0]
        
        self.dfs_visitar(inicio, padre, orden, etapa, visitados, inicio, visitar, extra)   

        return (padre, orden)

    def __compo_nexas(self, actual, padre, orden, extra):
        extra.append(actual)
        return True

    
    def componentes_conexas(self):
        '''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
        Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
        en caso de aplicarse a un grafo dirigido se lanzara TypeError'''
        if self.__dirigido :
            raise TypeError

        compo_conexas = []
        guardado = {}
        for v in self.__vertices:
            guardado[v] = False 

        for v in self.__vertices:
            lista = []
            if not guardado[v] :
                self.dfs(self.__compo_nexas, lista, v)
                for item in lista:
                    guardado[item] = True
                compo_conexas.append(lista)
        
        return compo_conexas

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
        visitado = {}
        distancia = {}
        heap_minimo = []
      
        camino = {} 
        for elemento in self.__vertices:
            visitado[elemento] = False
            if not (origen, elemento) in self.__aristas:
                distancia[elemento] =  999
            else:
                distancia[elemento] = self.__aristas[(origen, elemento)]
                
        heapq.heappush(heap_minimo, (0, origen, None))
        cantidad = 0
        distancia[origen] = 0;
        camino[origen] = (0, None)
        while heap_minimo :
            u = heapq.heappop(heap_minimo)
            
            if not visitado[u[1]]:
                visitado[u[1]] = True
                if u[1] != origen :
                    camino[u[1]] = u[0],u[2]
                    if u[1] == destino:
                        
                        break
                cantidad += 1
                if heuristica and heuristica(u[1], destino) > distancia[u[1]]:
                    continue
                for w in self.__vertices[u[1]]:
                
                    if not visitado[w]:
                        if distancia[w] >= distancia[u[1]]+ self.__aristas[(u[1], w)] :
                            distancia[w] = distancia[u[1]] + self.__aristas[(u[1], w)]
                            
                            heapq.heappush(heap_minimo, (distancia[w],w, u[1]))
                            
        # Se devuelven todos los caminos
        if not destino :
            return camino
        
        # Se devuelve el camino en particular
        if destino not in camino :
            return None
            
        return self.reconstruir_camino(camino, origen, destino)

    
    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        
        " " 

    def centralidad(self):
        centra = {} 
        guardado = {}
        for vertice in self.__vertices:
            guardado[vertice] = False
            centra[vertice] = 0 
            
        vector_caminos = []
        dic_caminos = {}
        heap = []
        vec = []
        for vertice in self.__vertices: # O(V(A LOG V))
                camino = self.camino_minimo(vertice, None, None)
                dic_caminos[vertice] = camino
                vec.insert(0, vertice)
                
        i = 0
        for vertice in self.__vertices:
            #if vec[i] 
            
            recorrido = self.reconstruir_camino(dic_caminos[vertice], vertice, vec[i])
            anterior = len(recorrido)
            for v in recorrido:
                centra[v] +=  anterior 
                anterior -= 1
            i += 1
            
        return centra
        
    def reconstruir_camino(self, recorrido, inicio, final):
       
        actual = final
        lista = []

        while actual:
            lista.insert(0, actual)
            c = recorrido.get(actual)
            if c :
                actual = c[1]
            else :
                actual = None
            
        return lista
        
        
 
# Convierte las lineas de un archivo parseado en forma (a1<a2>a3>...>an) en una
# lista con esas lineas. [a1, a2, a3,...,an]

def lista_lineas(archivo, opcion= False):
    linea = archivo.readline()	
    vec_linea = []
    if opcion == True: 
        vec_linea = linea.split("<")
    fin = vec_linea[0].find(">")
    vec_linea.insert(0, vec_linea[0][0: fin])
    if opcion == True: vec_linea[1] = vec_linea[1][fin+1:]
    return vec_linea


# Dada una ruta de archivo una cantidad y el grafo vacio, lo carga con n 
# articulos. 
def cargar_grafo(grafo, ruta, n):
    archivo_txt = open(ruta, "r")
    vec = []
    dic = {}
    for x in range(int(n)):
        vec = lista_lineas(archivo_txt, True)
        dic[vec[0]] = vec[1:]
        grafo.__setitem__(vec[0], 0)
        
    archivo_txt.close()
    vertices = grafo.keys()
    for v in vertices:
        for w in dic[v]:
            if grafo.__contains__(w):
                grafo.agregar_arista(v, w)

# Escoge la funcion pasada por parametro y ejecuta esa funcion
# En caso de no existir el comando o escribirlo mal, se informara por pantalla
def evaluar(grafo, accion, linea, pRank):
    if accion == "camino_mas_corto":
        camino_corto(grafo, linea)
 
    elif accion == "calcular_pagerank":
        calcular_pagerank_k(grafo, linea, pRank)
    
    elif accion == "mostrar_pagerank":
        mostrar_pagerank(grafo, linea, pRank)

    elif accion == "mostrar_top_pagerank":
        mostrar_top_pagerank(grafo, linea, pRank)

    elif accion == "centralidad":
        centralidad(grafo, linea)

    elif accion == "distancias":
        distancias(grafo, linea)
    

    elif accion == "diametro":
        diametro(grafo)
    else:
        print("Comando no reconocido")


def camino_corto(grafo, origen_destino):
    aux = origen_destino.split(",")
    if len(aux) < 2:
        print("uso: camino_mas_corto <Articulo1>,<Articulo2>")
        return 1
    aux[0] = aux[0][1:]
    if not grafo.__contains__(aux[0]) or not grafo.__contains__(aux[1]):
        print("Alguno de los articulos no se encuentran")
        return 1
    inicial = time()
    l = grafo.camino_minimo(aux[0], aux[1], None)
    salida = ""
    for articulo in l :
        salida += "->"+articulo

    print(salida[2:])
    tiempo_ejecucion  = time() - inicial
    print("el tiempo de la busqueda fue %0.10f s"% tiempo_ejecucion)

#0.85
d = 0.85


def pagerank(grafo, pRank, k):
    vertices = grafo.keys()
    N= len(vertices)

    for x in vertices : 
        pRank[x] = (1-d)/N
     
    for i in range(k):
        pRank_auxiliar = {}
        for x in vertices : 
            pRank_auxiliar[x] = (1-d)/N

        for x in vertices :
            adya = grafo.adyacentes(x)
            L = len(adya)
            for adyacentes in adya:
                pRank_auxiliar[adyacentes] += d*pRank[x] / L
              #  pRank[adyacentes] = pRank_auxiliar[adyacentes]
                            
        for verti in pRank:
            pRank[verti] = pRank_auxiliar[verti]
  
        
            
def calcular_pagerank_k(grafo, linea, pRank):
    k = int(linea[1:])
    inicial = time()
    pagerank(grafo, pRank, k)
    t_ejecucion = time() - inicial
    print("Tiempo de ejecucion calcular pr FUE %0.10f" % t_ejecucion)
    
        
def mostrar_pagerank(grafo, linea, pRank):
    articulo = linea[1:]
    if not grafo.__contains__(articulo):
        print("Este articulo no se encuentra")
        return 1

    print("page rank :", pRank[articulo]) 


def mostrar_top_pagerank(grafo, linea, pRank):
    
    k = linea[1:]
    if not k.isdigit():
        print("la cantidad no es valida")
    heap = []
        
    for vertices in pRank:        
        if len(heap) < int(k) or pRank[vertices] > heap[0][0]:
            heapq.heappush(heap, (pRank[vertices], vertices))
            if pRank[vertices] > heap[0][0]:
                heapq.heappop(heap)
    pila = Pila()
    while len(heap) != 0 :
        salida = heapq.heappop(heap)
        linea_salida = salida[1]+" : "+str(salida[0]) 
        pila.apilar(linea_salida)
    indice = 1
    while not pila.vacia():
        print(str(indice)+". "+pila.desapilar())
        indice += 1


def centralidad(grafo, linea):
    k = int(linea[1:])
    inicial = time()
    vertices = grafo.keys()
    centra =  grafo.centralidad()
    heap = []
    heapq.heappush(heap, (0, None))
    for item in centra:
        if heap[0][0] < centra[item]:
            heapq.heappush(heap, (centra[item], item))
    
    t_ejecucion = time() - inicial 
    # 0          k      n
    l = len(grafo.keys())
    for i in range(l) :
        par = heapq.heappop(heap)
        if i >= l-k:
            print(par[0], " : ", par[1])
    print("tiempo de ejecucion es %0.10f"% t_ejecucion)


def distancias(grafo, linea):
    
    articulo = linea[1:]
    if not grafo.__contains__(articulo):
        print("No se encuentra el articulo")
        return 1
    dist = {}
    
    recorrido = grafo.bfs(None, None, articulo)
    
    maximo = 0
    distancias = recorrido[2]
    print("len distancias ", len(distancias))
    for vertice in distancias:
        d = distancias[vertice]
        if d > maximo and d != 9999 :
            maximo = d

        if not d in dist:
            dist[d] = []
        else:
            dist[d].append(vertice)

    salida = "" 
    for i  in range(1, maximo):
        print("A DISTANCIA: %d "% i)
        for v in dist[i]:
            salida += v+", "
 
        print(salida)
        

# 0 = artic , 1 = padre, 2 = k

def diametro(grafo):
    inicial = time()
    
    vertices = grafo.keys()
    v_recorridos =  []
    vv = []
    for vertice in vertices:
        recorrido = grafo.camino_minimo(vertice, None)
        v_recorridos.append(recorrido)
        vv.insert(0, vertice)
        
    maximo = 0
    i = 0
    max_recorrido = []
    for v in vertices: # O(V )
        
        camino = grafo.reconstruir_camino(v_recorridos[i], v, vv[i])
        
        l = len(camino)
        if l > maximo :
            maximo = l
            max_recorrido = camino 
        i += 1

    print("Diametro :", maximo)
    print(max_recorrido)
    t_ejecucion = time() - inicial
    print("tiempo de ejecucion es %0.10f" % t_ejecucion)


# Main
# 10 000 - 3.39s 
# 2da imple 15 000 - 5.9s

def tp3_main():
    print("TP3 Modelacion de internet. Wikipedia")

    if len(sys.argv) !=  3:
        print("Uso : ./tp3.py <archivo> <cantidad>")
        return 1
    if not sys.argv[2].isdigit():
        print("Cantidad no valida !")
        return 1
            
            # Archivo txt
        
    ruta = ""
    if sys.argv[1] == "wiki":
        ruta = "Wiki-parsed.txt"
    else:
        ruta = sys.argv[1]


    inicial = time()
    grafo = Grafo(True)
    n = int(sys.argv[2])
    cargar_grafo(grafo, ruta, n )
    pRank = {}
    tiempo_ejecucion = time()- inicial
    print("El tiempo de carga fue %0.10f s"% tiempo_ejecucion)
    comando = input()
    
    while (comando != "fin"):
        accion = comando.split(" ")[0]
        
        evaluar(grafo, accion, comando[len(accion):], pRank)
        
        comando = input()
        


tp3_main()
