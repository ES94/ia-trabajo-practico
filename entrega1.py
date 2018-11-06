from simpleai.search import (SearchProblem, astar, depth_first, breadth_first,
                            greedy)
from simpleai.search.viewers import (ConsoleViewer, WebViewer, BaseViewer)
import random

MOVIMIENTOS = [(1,0),(-1,0),(0,1),(0,-1)]
ORILLA = []
for j in range(6):              #Se cargan las posiciones 'orillas'
    ORILLA.append((0,j))
for j in range(6):
    ORILLA.append((5,j))
for i in range(6):
    ORILLA.append((i,0))
for i in range(6):
    ORILLA.append((i,5))

# INICIAL = [(0,0) , [] , posiciones_Personas , False]

class RescatePersonas(SearchProblem):
    def is_goal(self, estado):
        if (len(estado[2]) == 0 and estado[3] == False): #Si rescató a todas las personas y tiene las manos vacías                                                         
            return True                                  #(ya que podría todavia estar cargando alguna y llevandola a la orilla).     
        else:
            return False

    def is_valid(self, estado, accion):
        pos_x, pos_y = estado[0][0], estado[0][1]
        pisados = estado[1]
        pos_x_new = pos_x + accion[0]
        pos_y_new = pos_Y + accion[1]        
        if (pos_x_new > 5 or pos_x_new < 0):
            return False
        if (pos_y_new > 5 or pos_y_new < 0):
            return False
        if ((pos_x_new,pos_y_new) in pisados):
            return False
        return True

    def actions(self, estado):
        acciones_disponibles = []
        for i in MOVIMIENTOS:
            if (is_valid(estado,i)) == True:
                acciones_disponibles.append(i)                
        return acciones_disponibles

    def result(self, estado, accion):
        pos_x = estado[0][0] + accion[0]
        pos_y = estado[0][1] + accion[1]
        pisados = estado[1]
        pos_personas = estado[2]
        ocupado = estado[3]
        for persona in range(0, len(pos_personas)):   #Rescate de personas. Cuando pisa la orilla el robot se 'desocupa', si estaba cargando a una persona.
            if ((pos_x,pos_y) == pos_personas[persona]):
                pos_personas.pop(persona)
                if not(ocupado):
                    ocupado = True
        if ((pos_x,pos_y) in ORILLA):
            if (ocupado):
                ocupado = False
        if ((pos_x,pos_y) not in ORILLA): #Si el robot se mueve a un casillero 'hundible', lo agrego a pisados.
            pisados.append((pos_x,pos_y))    
        
        return ([(pos_x,pos,y), pisados, pos_personas, ocupado])


    def cost(self, estado1, accion, estado2):
        return 1


    def heuristic(self, estado):
        


class ResultadoBusqueda:
    """Representa una salida formateada de un resultado de búsqueda."""

    def __init__(self, numero_de_caso, cantidad_nodos_visitados, 
        profundidad_solucion, costo_solucion, largo_maximo_frontera):
        self.numero_de_caso = numero_de_caso
        self.cantidad_nodos_visitados = cantidad_nodos_visitados
        self.profundidad_solucion = profundidad_solucion
        self.costo_solucion = costo_solucion
        self.largo_maximo_frontera = largo_maximo_frontera
    
    def __str__(self):
        return ('{caso}: {cant_vis}, {prof_sol}, {cost_sol}, ' + 
            '{larg_max_front}'.format(caso=self.numero_de_caso, 
            cant_vis=self.cantidad_nodos_visitados, 
            prof_sol=self.profundidad_solucion, cost_sol=self.costo_solucion,
            larg_max_front=self.largo_maximo_frontera))


def resolver(metodo_busqueda, posiciones_personas):
    """Devuelve un nodo resultado, a partir de una búqueda especificada.

    Argumentos:
    metodo_busqueda -- nombre de método a usar (string);
    posiciones_personas -- lista de tuplas. Cada tupla representa la posicion de una persona en la grilla (aún por rescatar).

    """
        
    """
    Estado inicial: Lista compuesta de 4 posiciones:
    1era posicion: Tupla. Posicion del robot en la grilla.
    2da posicion: Lista de tuplas. Posiciones de la grilla que el robot va hundiendo (inutilizando).
    3era posicion: Lista de tuplas. Posiciones de la grilla donde se ubican las personas aún no rescatadas.
    4ta posicion: Booleano. Es True si el robot esta 'ocupado' (esta cargando personas), caso contrario False.
    """
    ESTADO_INICIAL = [(0,0) , [] , posiciones_Personas , False]
    problema = RescatePersonas(ESTADO_INICIAL)

    if metodo_busqueda == 'astar':
        return astar(problema, graph_search=True, viewer=ConsoleViewer())
    
    if metodo_busqueda == 'depth_first':
        return depth_first(problema, graph_search=True, 
                viewer=ConsoleViewer())
    
    if metodo_busqueda == 'breadth_first':
        return breadth_first(problema, graph_search=True, 
                viewer=ConsoleViewer())

    if metodo_busqueda == 'greedy':
        return greedy(problema, graph_search=True, viewer=ConsoleViewer())

def Nodos_Visitados():
    pass

def Largo_Max_Frontera():
    pass

if __name__ == "__main__":
    for i in range(5):
        """Como máximo pueden haber 16 personas en la grilla"""
        Personas = random.randint(1,16) #Numero aleatorio de personas a rescatar.

        """Las posiciones de las personas son aleatorias"""
        Pos_Personas = []
        while (Personas != len(Pos_Personas)): #Carga de posiciones de personas aleatoriamente.
            Pos_x, Pos_y = random.randint(1,4) , random.randint(1,4)
            if ((Pos_x,Pos_y) not in Pos_Personas):        
                Pos_Personas.append((Pos_x,Pos_y))
                
        r = resolver('astar', Pos_Personas)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)

    for i in range(5):
        """Como máximo pueden haber 16 personas en la grilla"""
        Personas = random.randint(1,16) #Numero aleatorio de personas a rescatar.

        """Las posiciones de las personas son aleatorias"""
        Pos_Personas = []
        while (Personas != len(Pos_Personas)): #Carga de posiciones de personas aleatoriamente.
            Pos_x, Pos_y = random.randint(1,4) , random.randint(1,4)
            if ((Pos_x,Pos_y) not in Pos_Personas):        
                Pos_Personas.append((Pos_x,Pos_y))
                
        r = resolver('depth_first', Pos_Personas)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)
    
    for i in range(5):
        """Como máximo pueden haber 16 personas en la grilla"""
        Personas = random.randint(1,16) #Numero aleatorio de personas a rescatar.

        """Las posiciones de las personas son aleatorias"""
        Pos_Personas = []
        while (Personas != len(Pos_Personas)): #Carga de posiciones de personas aleatoriamente.
            Pos_x, Pos_y = random.randint(1,4) , random.randint(1,4)
            if ((Pos_x,Pos_y) not in Pos_Personas):        
                Pos_Personas.append((Pos_x,Pos_y))
                
        r = resolver('breadth_first', Pos_Personas)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)
    
    for i in range(5):
        """Como máximo pueden haber 16 personas en la grilla"""
        Personas = random.randint(1,16) #Numero aleatorio de personas a rescatar.

        """Las posiciones de las personas son aleatorias"""
        Pos_Personas = []
        while (Personas != len(Pos_Personas)): #Carga de posiciones de personas aleatoriamente.
            Pos_x, Pos_y = random.randint(1,4) , random.randint(1,4)
            if ((Pos_x,Pos_y) not in Pos_Personas):        
                Pos_Personas.append((Pos_x,Pos_y))
                
        r = resolver('greedy', Pos_Personas)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)
