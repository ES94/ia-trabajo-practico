from simpleai.search import (SearchProblem, astar, depth_first, breadth_first,
                            greedy)
from simpleai.search.viewers import (ConsoleViewer, WebViewer, BaseViewer)


class RescatePersonas(SearchProblem):
    def is_goal(self, estado):
        pass


    def actions(self, estado):
        pass


    def result(self, estado, accion):
        pass


    def cost(self, estado1, accion, estado2):
        pass


    def heuristic(self, estado):
        pass


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
    posiciones_personas -- lista de posiciones donde se encuentran personas 
    (tuple<tuple<int>>)

    """

    ESTADO_INICIAL = ((0, 0), (), posiciones_personas)
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


if __name__ == "__main__":
    for i in range(5):
        PERSONAS = ()  # Generar cantidad y posición de personas 
                       # aleatoriamente.
        r = resolver('astar', PERSONAS)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)

    for i in range(5):
        PERSONAS = ()  # Generar cantidad y posición de personas 
                       # aleatoriamente.
        r = resolver('depth_first', PERSONAS)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)
    
    for i in range(5):
        PERSONAS = ()  # Generar cantidad y posición de personas 
                       # aleatoriamente.
        r = resolver('breadth_first', PERSONAS)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)
    
    for i in range(5):
        PERSONAS = ()  # Generar cantidad y posición de personas 
                       # aleatoriamente.
        r = resolver('greedy', PERSONAS)
        resultado_busqueda = ResultadoBusqueda(i, cantidad_nodos_visitados, 
                                r.depth, r.cost, largo_maximo_frontera)
        print(resultado_busqueda)