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
        En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
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
        if self.__dirigido :
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
        lista = []
        cola = Cola()
        cola2 = Cola()
        cola.encolar(inicio)
        padre = {}
        orden =  {}    
        ordencito = 0
        while not cola.vacia() and not fin: 
            #print("comenzamos")
            print("veer tope",cola.ver_tope())
            if visitar:
                if visitar(cola.ver_tope(), padre, orden, extra) == False:
                    fin = True
            if fin : continue
            v = cola.desencolar()
            if not visitados[v]:
                visitados[v] = True
                if inicio == v :
                     padre[v] = None
                else:
                    padre[v] = cola2.desencolar()                    
                orden[v] = ordencito
                ordencito += 1
                lista.append(v)
                cola2.encolar(v)
                for w in self.__vertices[v]:
                    if not visitados[w]:
                        cola.encolar(w)
        return (padre, orden)

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
        raise NotImplementedError()
    
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
        raise NotImplementedError()
    
    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        raise NotImplementedError()


    def mostrar(self):
        print("GRAFO VERTICES", self.__vertices)
        print("GRAFO DATOS", self.__datos)
        print("GRAFO ARISTAS", self.__aristas)
        print("GRAFO LEN ", self.__len__())

'''grafo = Grafo(False)

print("agrego clave joseph valor 1", grafo.__setitem__("joseph", 5200))
print("ahora joseph pertence al grafo", grafo.__contains__("joseph"))
print("cantidad dle grafo es ", grafo.__len__())
print("agrego clave vilca valor 2", grafo.__setitem__("vilca", 2))
print("muestro el grafo: ", grafo.mostrar())
print("agrego clave vilca de nuevo", grafo.__setitem__("vilca", 4))
grafo.mostrar()
print("Muestro las claves con keys", grafo.keys())
print("get valor joseph", grafo.__getitem__("joseph"))
print("get valor vilca", grafo.__getitem__("vilca"))
print("agregar arista joseph->vilca", grafo.agregar_arista("joseph", "vilca", 40))
print("agregar vertice vargas", grafo.__setitem__("vargas", 10))
grafo.mostrar()
#print("agrgar arista invalida joseph-> X", grafo.agregar_arista("joseph", "X"))
print("El peso de la arista joseph->vilca", grafo.obtener_peso_arista("joseph", "vilca"))
print("Peso de arista que no ecsiste", grafo.obtener_peso_arista("joseph", "vargas"))
print("borrar arista joseph -> vilca", grafo.borrar_arista("joseph", "vilca"))
grafo.mostrar()
print("cantidad dde vertices :", grafo.__len__())
print("Vertices adyacentes a joseph", grafo.adyacentes("joseph"))
print("agregar arista joseph->vilca", grafo.agregar_arista("joseph", "vilca", 100))
print("agregar arista joseph->vargas", grafo.agregar_arista("joseph", "vargas", 200))
grafo.mostrar()
print("vertices adyacentes a joseph", grafo.adyacentes("joseph"))
print("obtener peso arista joseph->vargas", grafo.obtener_peso_arista("joseph", "vargas"))
#print("eliminar vertice Joseph ", grafo.__delitem__("joseph"))
grafo.mostrar()
print("agregar arista vilca -> vargas", grafo.agregar_arista("vilca", "vargas"))
listel = grafo.bfs(None, None, "vilca")
print(listel)
'''
grafo2 = Grafo(True)
print("agregar vertice A", grafo2.__setitem__("A", 1))
print("agregar vertice B", grafo2.__setitem__("B", 2))
print("agregar vertice C", grafo2.__setitem__("C", 3))
print("agregar vertice D", grafo2.__setitem__("D", 4))
print("agregar vertice E", grafo2.__setitem__("E", 5))

print("agregar arista A-C", grafo2.agregar_arista("A", "C"))
print("agregar arista B-A", grafo2.agregar_arista("B", "A"))
print("agregar arista D-C", grafo2.agregar_arista("D", "C"))
print("agregar arista C-E", grafo2.agregar_arista("C", "E"))

l = grafo2.bfs(None, None, "A")
print(l)
l = grafo2.bfs(None, None, "B")
print(l)
l = grafo2.bfs(None, None, "E")
print(l)
def parar(vertice, padre, orden, extra):
    extra += 1
    print(extra)
    if vertice == "E":
        
        print("toy aka")
        print("ACA TERMINA LA ITERACION ")
        return False


conti = 0
l = grafo2.bfs(parar, conti, "D")
print(l)
print(conti)
