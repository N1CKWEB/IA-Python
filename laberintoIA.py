class Nodo():
    def __init__(self,_estado,_padre,distancia):#,_accion):
        self.estado=_estado   #Entendemos por estado (fila,columna)
        self.padre=_padre     
        #self.accion=_accion   #Accion es simplemente un texto
                              #que diga que accion se realizo, ejemplo (Arriba,Abajo,Izquierda,Derecha)
                              #No es fundamental para el funcionamiento
        self.distancia = distancia

class FronteraStack():
    def __init__(self):
        self.frontera=[]
    def agregar_nodo(self,_nodo):
        #Agregar el nodo pasado por parametro a la frontera
        self.frontera.append(_nodo)
    def quitar_nodo(self):
        #Quitar nodo de la frontera (respetar el tipo de frontera)
        return self.frontera.pop()
    def esta_vacia(self):
        #Comprobar si la frontera está vacia o no
        return len(self.frontera)==0
    
    def contiene_estado(self,_estado):
        #Comprobar si el estado pasado por parametro ya se encuentra en la frontera
        #La frontera contiene nodos y no estados sueltos
        for nodo in self.frontera:
            if nodo.estado == _estado:
                return True
        return False
    
class FronteraQueue(FronteraStack):
    '''Aplicar herencia con FronteraStack
       La unica diferencia entre ambas es como
       se quitan los nodos
    '''
    def quitar_nodo(self):
        #Quitar nodo de la frontera (respetar el tipo de frontera)
        return self.frontera.pop(0)
    
class FronteraDistancia(FronteraQueue):
    def quitar_nodo(self):
        self.frontera = sorted(self.frontera, key=lambda x: x.distancia)
        return self.frontera.pop(0)
    
    
    
    
class Laberinto():
    def  __init__(self,_algoritmo, _path):
        '''Dentro del init podemos ejecutar funciones
           para ir definiendo los atributos de la clase.
           Les dejo lista la parte de leer el laberinto
           del archivo de texto, y la detección del inicio,
           meta y paredes.
        '''
        with open(_path,'r') as archivo:
            laberinto=archivo.read()     #Con read() leemos todo el archivo y lo guardamos en laberinto
        self.laberinto=laberinto.splitlines() #Con splitlines() separamos el laberinto en lineas, eliminando el \n
        self.ancho=len(self.laberinto[0])    #El ancho del laberinto es la cantidad 
                                        #de caracteres de la primer linea 
                                        #(O de cualquiera suponiendo que todas tienen el mismo ancho)
        self.alto=len(self.laberinto)        #El alto del laberinto es la cantidad de lineas
        self.paredes=[]                 #Lista de paredes

        for fila in range(self.alto):   #Recorremos todas las filas
            fila_paredes=[]             #Creamos una lista vacia para las paredes de la fila actual
            for columna in range(self.ancho): #Recorremos todas las columnas
                if self.laberinto[fila][columna]==' ': #Si el caracter es # es una pared
                    fila_paredes.append(False) #Agregamos la pared a la lista de paredes de la fila actual
                elif self.laberinto[fila][columna]=='I':   #Si el caracter es I es el inicio
                    self.inicio=(fila,columna)         #Guardamos el inicio
                    fila_paredes.append(False)
                elif self.laberinto[fila][columna]=='M':   #Si el caracter es M es la meta
                    self.meta=(fila,columna)           #Guardamos la meta
                    fila_paredes.append(False)
                else:
                    fila_paredes.append(True)
            self.paredes.append(fila_paredes)         #Agregamos la lista de paredes de la fila actual a la lista de paredes
        #De este modo ya tenemos identificadas las paredes, el inicio y la meta
        self.solucion = []
        self.algoritmo=_algoritmo #String en el que pasamos el nombre del algoritmo a utilizar

    def expandir_nodo(self,_nodo):
        '''Dentro de _nodo.estado tenemos la posicion actual del nodo
           Debemos comprobar en todas las direcciones si podemos movernos
           descartando las que sean paredes o esten fuera del laberinto                 (fila-1,col)     --->   (fila-1,columna)
           Utilicen el grafico que está en el Notion para guiarse      (fila,col-1) (fila actual,columna actual) (fila,col+1)
           Devolver una lista de vecinos posibles (nodos hijo)                          (fila+1,col)     --->   (fila+1,columna)
        '''
        #_nodo.estado = (fila,columna)
        fila, columna = _nodo.estado
        vecinos = []
        candidatos = [(fila-1,columna),(fila,columna-1),(fila,columna+1),(fila+1,columna)]
        
        for f,c in candidatos:
            if 0 <= f < self.alto and 0 <= c < self.ancho and not self.paredes[f][c]:
                vecinos.append((f,c))
        return vecinos
    

    def tomar_distancia(self,estado):
            x1, y1 = estado
            x2, y2 = self.meta
            dixt_y = abs(y2 - y1)
            dixt_x = abs(x2 - x1)
            return dixt_x + dixt_y
    
    
    def dibujar_solucion(self):
        laberinto_str = ""
        for fila in range(self.alto):
            filas = []
            for columna in range(self.ancho):
                if self.laberinto[fila][columna] == '#':
                    filas.append("#")
                elif self.laberinto[fila][columna] == 'I':
                    filas.append("I")
                elif self.laberinto[fila][columna] == 'M':
                    filas.append("M")
                elif self.laberinto[fila][columna] == ' ':
                    filas.append(" ")
                    
                nodo_actual = None
                for nodo in self.solucion:
                    if nodo.estado == (fila, columna):
                        nodo_actual = nodo
                        break

                if nodo_actual and nodo_actual.estado != self.inicio:
                    filas[columna] = "+"

            laberinto_str += "".join(filas) + "\n"
        print(laberinto_str)

    def resolver(self):
        '''
        Acá tienen que implementar el algoritmo de busqueda
        La idea es intentar replicar el pseudocodigo que vimos en clase
        1- Inicializar la frontera con el nodo inicial
        2- Inicializar el conjunto de explorados como vacio
        3- Repetimos:
            3.1- Si la frontera esta vacia, no hay solucion
            3.2- Quitamos un nodo de la frontera
            3.3- Si el nodo contiene un estado que es meta, devolver la solucion
            3.4- Agregar el nodo a explorados
            3.5- Expandir el nodo, agregando los nodos hijos a la frontera
        '''
        if self.algoritmo=='BFS':
            #Crear la frontera que corresponda
            frontera = FronteraQueue()
        elif self.algoritmo=='DFS':
            #Crear la frontera que corresponda
            frontera = FronteraStack()
        elif self.algoritmo == "GBFS" or  self.algoritmo== "A*":
            frontera = FronteraDistancia()
        #-------------------------------------
        #------------------------------------------------------------------------
        costo = 0
        if self.algoritmo == "GBFS":
            nodo_inicial = Nodo(self.inicio,None, self.tomar_distancia(self.inicio))
        elif self.algoritmo== "A*":
            nodo_inicial = Nodo(self.inicio,None, self.tomar_distancia(self.inicio)+costo)
        else:
            nodo_inicial = Nodo(self.inicio,None, None)
        frontera.agregar_nodo(nodo_inicial)
        print(frontera)
        self.explorados = set()

        
        while True:

            if frontera.esta_vacia():
                print("No hay solucion")
                return
            nodo_actual = frontera.quitar_nodo()
            if nodo_actual.estado == self.meta:
                print("Estamos en la meta")
                #Aca deberiamos recorrer los padres partiendo desde el
                #ultimo nodo, para encontrar todo el camino hacia el inicio
                while nodo_actual.padre is not None:
                    self.solucion.append(nodo_actual.padre)
                    nodo_actual = nodo_actual.padre
                self.solucion.reverse()
                self.dibujar_solucion()
                return self.solucion
            

            self.explorados.add(nodo_actual.estado)
            vecinos = self.expandir_nodo(nodo_actual)
            costo+=1
            for vecino in vecinos:
                    #vecino contiende dentro una tupla (fila,columna)
                    #crear cada Nodo pasandole ese vecino como estado
                    #el nodo_actual es el padre
                if not frontera.contiene_estado(vecino) and vecino not in self.explorados:
                    if self.algoritmo == "GBFS":
                        nodo_hijo = Nodo(vecino, nodo_actual, self.tomar_distancia(vecino))
                    elif self.algoritmo == "A*":
                        nodo_hijo = Nodo(vecino, nodo_actual, self.tomar_distancia(vecino)+costo)
                    else:
                        nodo_hijo = Nodo(vecino, nodo_actual, None)
                    frontera.agregar_nodo(nodo_hijo)