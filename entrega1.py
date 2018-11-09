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

# INICIAL = ((0,0) , () , posiciones_Personas , False)

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
        pisados = list(estado[1])
        pos_personas = list(estado[2])
        ocupado = estado[3]

        if (pos_x, pos_y) in pos_personas:     # Rescate de personas. Cuando
            pos_personas.remove((pos_x, pos_y))  # pisa la orilla el robot se 
            if not ocupado:                    # 'desocupa', si estaba 
                ocupado = True                 # cargando a una persona.

        if (pos_x,pos_y) in ORILLA:
            if ocupado:
                ocupado = False
        if ((pos_x,pos_y) not in ORILLA):  # Si el robot se mueve a un 
            pisados.append((pos_x,pos_y))  # casillero 'hundible', lo agrego a
                                           # pisados.
        return ((pos_x, pos_y), tuple(pisados), tuple(pos_personas), ocupado)

    def cost(self, estado1, accion, estado2):
        return 1

    def heuristic(self, estado):  #Sumatoria de distancia de robot a persona y de esa persona a la orilla mas cercana.
        costos_heuristica = []
        pos_personas = tuple(estado[2])
        pos_robot = list(estado[0])

        if pos_personas:
            for pos_per in pos_personas:
                distanciaX = abs(pos_robot[0] - pos_per[0])
                distanciaY = abs(pos_robot[1] - pos_per[1]) 
                distanciaXY = distanciaX + distanciaY
                mas_cercanas = [pos_per[0], pos_per[1], 5 - pos_per[0], 
                                    5 - pos_per[1]]
                costos_heuristica.append(min(mas_cercanas) + distanciaXY)  #guardo el costo de distancia desde la persona a la orilla mas cercana + la distancia del robot a la persona
            
            return max(costos_heuristica)
        else:
            return 0


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
    ESTADO_INICIAL = ((0,0) , (), posiciones_personas , False)
    problema = RescatePersonas(ESTADO_INICIAL)

    if metodo_busqueda == 'astar':
        return astar(problema, graph_search=True)
    elif metodo_busqueda == 'depth_first':
        return depth_first(problema, graph_search=True)
    elif metodo_busqueda == 'breadth_first':
        return breadth_first(problema, graph_search=True)
    elif metodo_busqueda == 'greedy':
        return greedy(problema, graph_search=True)


if __name__ == "__main__":
    my_viewer = BaseViewer()
    ESTADO_INICIAL = ((0,0) , (), ((2, 1), (3, 4), (4, 2)) , False)
    problema = RescatePersonas(ESTADO_INICIAL)
    
    result = astar(problema, graph_search=True, viewer=my_viewer)
    print("Stats: ",my_viewer.stats)
    print("Solucion: ",result.state)
    print("profundidad_solucion: ",len(result.path()))
    print("costo_solucion:", result.cost)