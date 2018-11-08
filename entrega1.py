from simpleai.search import (SearchProblem, astar, depth_first, breadth_first,
                            greedy)
from simpleai.search.viewers import (ConsoleViewer, WebViewer, BaseViewer)
import random

MOVIMIENTOS = ((1,0),(-1,0),(0,1),(0,-1))
ORILLA = []
for j in range(6):              #Se cargan las posiciones 'orillas'
    ORILLA.append((0,j))
for j in range(6):
    ORILLA.append((5,j))
for i in range(6):
    ORILLA.append((i,0))
for i in range(6):
    ORILLA.append((i,5))

# INICIAL = ((0,0) , [] , posiciones_Personas , False)

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
        pos_y_new = pos_y + accion[1]        
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
            if (self.is_valid(estado,i) == True):
                acciones_disponibles.append(i)                
        return tuple(acciones_disponibles)

    def result(self, estado, accion):
        pos_x = estado[0][0] + accion[0]
        pos_y = estado[0][1] + accion[1]
        pisados = estado[1]
        pos_personas = estado[2]
        ocupado = estado[3]
        for persona in range(0, len(pos_personas)):  # Rescate de personas. 
                                                     # Cuando pisa la orilla 
                                                     # el robot se 'desocupa',
                                                     # si estaba cargando a 
                                                     # una persona.
            if ((pos_x,pos_y) == pos_personas[persona]):
                pos_personas.pop(persona)
                if not(ocupado):
                    ocupado = True
        if ((pos_x,pos_y) in ORILLA):
            if (ocupado):
                ocupado = False
        if ((pos_x,pos_y) not in ORILLA):  # Si el robot se mueve a un 
                                           # casillero 'hundible', lo agrego a
                                           # pisados.
            pisados.append((pos_x,pos_y))    
        
        return ([(pos_x, pos_y), pisados, pos_personas, ocupado])

    def cost(self, estado1, accion, estado2):
        return 1

    """
    def heuristic(self, estado):
        costo_heuristica = 0
        pos_robot = list(estado[0])
        pos_personas = tuple(estado[2])

        # Sumarizar las distancias Manhattan de las personas.
        for pos_per in pos_personas:
            costo_heuristica += (abs(pos_per[0] - pos_robot[0]) + 
                                abs(pos_per[1] - pos_robot[1]))
            pos_robot = [pos_per[0], pos_per[1]]
        costo_heuristica += min(pos_robot[0], pos_robot[1], 5 - pos_robot[0], 
                                5 - pos_robot[1])  # Distancia mínima a una 
                                                   # orilla.
        return costo_heuristica
    """

    """
    def heuristic(self, estado):
        costo_heuristica = 0
        pos_personas = tuple(estado[2])

        # Sumarizar las distancias Manhattan de las personas.
        for pos_per in pos_personas:
            costo_heuristica += max(pos_per[0], pos_per[1], 
                                5 - pos_per[0], 5 - pos_per[1])
        return costo_heuristica
    """
    def heuristic(self, estado):  #Sumatoria de distancia de robot a persona y de esa persona a la orilla mas cercana.
        costos_heuristica = []
        pos_personas = tuple(estado[2])
        pos_robot = list(estado[0])

        for pos_per in pos_personas:
            distanciaX = abs(pos_robot[0] - pos_per[0])
            distanciaY = abs(pos_robot[1] - pos_per[1])
            
            distanciaXY = distanciaX + distanciaY
            mas_cercanas = []
            for i in ORILLA:
                pos_orilla_x = i[0]
                pos_orilla_y = i[1]
                pos_orilla = pos_orilla_x + pos_orilla_y
                mas_cercanas.append(abs(distanciaXY - pos_orilla))

            costos_heuristica.append(min(mas_cercanas) + distanciaXY)  #guardo el costo de distancia desde la persona a la orilla mas cercana + la distancia del robot a la persona

        return (max(costos_heuristica))     
                
    


def resolver(metodo_busqueda, posiciones_personas):
    """ Devuelve un nodo resultado, a partir de una búqueda especificada.

    Argumentos:
    metodo_busqueda -- nombre de método a usar (string);
    posiciones_personas -- lista de tuplas. Cada tupla representa la posicion 
    de una persona en la grilla (aún por rescatar).

    """
        
    """
    Estado inicial: Lista compuesta de 4 posiciones:
    1era posicion: Tupla. Posicion del robot en la grilla.
    2da posicion: Lista de tuplas. Posiciones de la grilla que el robot va 
    hundiendo (inutilizando).
    3era posicion: Lista de tuplas. Posiciones de la grilla donde se ubican 
    las personas aún no rescatadas.
    4ta posicion: Booleano. Es True si el robot esta 'ocupado' (esta cargando 
    personas), caso contrario False.
    """
    visor = BaseViewer()
    ESTADO_INICIAL = ((0,0) , (), posiciones_personas , False)
    problema = RescatePersonas(ESTADO_INICIAL)

    if metodo_busqueda == 'astar':
        result = astar(problema, graph_search=True, viewer=visor)
    
    if metodo_busqueda == 'depth_first':
        result = depth_first(problema, graph_search=True, viewer=visor)
    
    if metodo_busqueda == 'breadth_first':
        result = breadth_first(problema, graph_search=True, viewer=visor)

    if metodo_busqueda == 'greedy':
        result = greedy(problema, graph_search=True, viewer=visor)


if __name__ == "__main__":
    my_viewer = BaseViewer()
    ESTADO_INICIAL = ((0,0) , (), ((2, 1), (3, 4), (4, 2)) , False)
    problema = RescatePersonas(ESTADO_INICIAL)
    result = breadth_first(problema, graph_search=True, viewer=my_viewer)
    print("Stats: ",my_viewer.stats)
    print("Solucion: ",result.state)
    print("profundidad_solucion: ",len(result.path()))
    print("costo_solucion:", result.cost)
