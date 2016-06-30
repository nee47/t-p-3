visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0
import heapq
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
            self.__aristas[(desde, hasta)] = peso
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
        #del self.__aristas[desde][hasta]

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
        for elemento in self.__vertices:
            visitados[elemento] = False
        fin = False
        cola = Cola()
        padre = {}
        orden =  {}    
        ordencito = 0
        if inicio :
            padre[inicio] = None
            cola.encolar(inicio)

        while not cola.vacia() and not fin: 
            v = cola.desencolar()
            if visitar:
                if visitar(v, padre, orden, extra) == False:
                    fin = True
            #orden[v] = ordencito
            #ordencito += 1
            if not visitados[v]:
                orden[v] = ordencito
                ordencito += 1
                visitados[v] = True
                if fin:
                    continue
                for w in self.__vertices[v]:
                    if not visitados[w]:
                        cola.encolar(w)
                        padre[w] = v

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
        #improvisando
        #fin improvisando
        visitado = {}
        distancia = {}
        heap_minimo = []
        camino = {} # {'A': (peso, Vertice , padre)}
        for elemento in self.__vertices:
            visitado[elemento] = False
            distancia[elemento] =  999
        heapq.heappush(heap_minimo, (0, origen, None))
        cantidad = 0
        distancia[origen] = 0;
        camino[origen] = (1, None)
        while heap_minimo :
            u = heapq.heappop(heap_minimo)
            if not visitado[u[1]]:
                visitado[u[1]] = True
                if u[1] != origen :
                    camino[u[1]] = u[0],u[2]
                    if u[1] == destino:
                        break
                cantidad += 1
                if distancia[u[1]] > 20:
                    continue
                for w in self.__vertices[u[1]]:
                    if not visitado[w]:
                        peso = self.__aristas[(u[1], w)] + distancia[u[1]]
                        heapq.heappush(heap_minimo, (peso ,
                                                 w, u[1]))
                        distancia[w] = peso
                    #cantidad += 1
                        #distancia[]
        
        
                    
        # {'H:(0, A)  }
        print("distancia destino", distancia[destino], "cantidad", cantidad)
        if destino not in camino :
            print("no se encuentra camino")
            return None
       # print(camino)
        #return None
        lista_camino = []
        actual = destino
        #csc= input()
        #print("wa comenzar a empaquetar")
        while actual :
            #print(actual)
            lista_camino.insert(0, actual)
            #print(actual)
            c = camino.get(actual)
            if c : 
                actual = c[1]
            else : actual = None
        #print("Distancias", distancia)
        return lista_camino
 

    
    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        raise NotImplementedError()


    def mostrar(self):
        print("GRAFO VERTICES", self.__vertices)
        #print("GRAFO DATOS", self.__datos)
        #print("GRAFO ARISTAS", self.__aristas)
        print("cantidad vertices ", self.__len__())
        print("CANTIDAD E ARISTAS PRRO", len(self.__aristas))


grafo3 = Grafo(True)
valor = 122
grafo3.__setitem__("0", valor)
grafo3.__setitem__("1", valor)
grafo3.__setitem__("2", valor)
grafo3.__setitem__("3", valor)
grafo3.__setitem__("4", valor)
grafo3.__setitem__("5", valor)
grafo3.__setitem__("6", valor)
grafo3.__setitem__("7", valor)
grafo3.__setitem__("322", valor)
print("agrego 0 - 1")
print("agrego 1 - 3")
print("agrego 3 - 2")
print("agrego 2 - 1")
print("agrego 3 - 4")
print("agrego 4 - 5")
print("agrego 5 - 7")
print("agrego 7 - 6")
print("agrego 6 - 4")
grafo3.agregar_arista("0", "1")
grafo3.agregar_arista("1", "3")
grafo3.agregar_arista("3", "2")
grafo3.agregar_arista("2", "1")
grafo3.agregar_arista("3", "4")
grafo3.agregar_arista("4", "5")
grafo3.agregar_arista("5", "7")
grafo3.agregar_arista("7", "6")
grafo3.agregar_arista("6", "4")
grafo3.agregar_arista("322", "4")
grafo3.mostrar()
def parar(vertice, padre, orden, extra):
    extra += 1
    print(extra)
    if vertice == "3":
        
        print("toy aka")
        print("ACA TERMINA LA ITERACION ")
        return False

C= 0
t = grafo3.bfs(parar, C, "0")
print("PADRES BFS : ", t[0])
print("ORDEN : ", t[1])

print("BFS TEST")

t2 = grafo3.bfs(None, None, "0")

print("PADRES BFS SIN VISITAR: ", t2[0])
print("ORDEN SIN VISITAR", t2[1])

r_minimo = grafo3.camino_minimo("0", "3")

print("el cmaino minimo es", r_minimo)

g =  Grafo(True)

g.__setitem__("A", valor)
g.__setitem__("B", valor)
g.__setitem__("C", valor)
g.__setitem__("D", valor)
g.__setitem__("H", valor)
g.__setitem__("R", valor)
g.__setitem__("T", valor)
print("D-C")
print("D-B")
print("B-H")
print("C-R")
print("H-D")
print("H-A")
print("R-H")
print("H-T")

g.agregar_arista("D", "C")
g.agregar_arista("D", "B")
g.agregar_arista("B", "H")
g.agregar_arista("C", "R")
g.agregar_arista("H", "D")
g.agregar_arista("H", "A")
g.agregar_arista("R", "H")
g.agregar_arista("H", "T")

#extra
g.__setitem__("xxx", valor)
g.agregar_arista("xxx", "R")
g.mostrar()

g_t = g.bfs(None, None, "D")

print("PADRES G_T   :", g_t[0])
print("ORDEN G_t ", g_t[1])

g_t = g.dfs(None, None, "D")
print("PADRES G_T dfs  :", g_t[0])
print("ORDEN G_t dfs", g_t[1])

cam_min = g.camino_minimo("D","B")
print("CAMINO MINIMO ",cam_min)
