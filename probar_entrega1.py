# coding: utf-8
from datetime import datetime
import inspect
import os
import sys



problemas = []
recomendaciones = []
advertencias = []


def validar_tiempo(inicio, fin, tope, listado, mensaje):
    diferencia = (fin - inicio).total_seconds()
    if diferencia > tope:
        listado.append(mensaje)


def probar_codigo(interactivo=False, saltear_errores=False, resultado_verboso=False):
    # dependencias
    try:
        from simpleai.search.models import SearchNode
    except ImportError:
        problemas.append('No se pudo importar SimpleAI. Se encuentra instalado?')
        return

    # intentar importar la entrega
    print('Importando la entrega...')

    try:
        inicio = datetime.now()
        import entrega1
        fin = datetime.now()
    except ImportError:
        problemas.append('No se pudo encontrar el cÃ³digo python. Probablemente el nombre del '
                         'archivo .py no es correcto, o no estÃ¡ en la raiz del repositorio.')
        return

    validar_tiempo(inicio, fin, 3, problemas,
                   'El import de la entrega demora demasiado tiempo, probablemente estÃ¡n '
                   'haciendo bÃºsqueda en el import. Hagan lo del if __name__ ... que se '
                   'recomienda en la consigna.')

    # intentar extraer y validar la funcion resolver
    print('Extrayendo la funciÃ³n resolver...')

    resolver = getattr(entrega1, 'resolver', None)

    if resolver is None:
        problemas.append('El mÃ³dulo python no define la funciÃ³n resolver.')
        return

    if inspect.getargspec(resolver)[0] != ['metodo_busqueda', 'posiciones_personas']:
        problemas.append('La funciÃ³n resolver no recibe los parÃ¡metros definidos en la entrega.')
        return

    # validar el funcionamiento de la funcion resolver y el planteo del problema en general
    print('Probando la resoluciÃ³n de problemas...')

    # metodo_busqueda, posiciones_personas, limite_largo_camino, limite_tiempo
    pruebas = (

        # simples
        ('breadth_first', ((2, 3),), 10, 10),
        ('depth_first', ((2, 3),), None, 30),
        ('greedy', ((2, 3),), None, 30),
        ('astar', ((2, 3),), 10, 10),

        # completos
        ('breadth_first', ((2, 1), (3, 4), (4, 2)), None, 300),
        ('depth_first', ((2, 1), (3, 4), (4, 2)), None, 300),
        ('greedy', ((2, 1), (3, 4), (4, 2)), None, 60),
        ('astar', ((2, 1), (3, 4), (4, 2)), None, 60),
    )

    for numero_prueba, (metodo_busqueda, posiciones_personas, limite_largo_camino, limite_tiempo) in enumerate(pruebas):
        print('  Prueba', numero_prueba, ':', metodo_busqueda, 'personas en', posiciones_personas)

        if not interactivo or input('ejecutar? (Y/n)').strip() in ('y', ''):
            try:
                inicio = datetime.now()
                resultado = resolver(metodo_busqueda=metodo_busqueda,
                                     posiciones_personas=posiciones_personas)
                fin = datetime.now()

                if isinstance(resultado, SearchNode):
                    print('     largo camino:', len(resultado.path()))
                    print('     estado:', resultado.state)
                    print('     acciones:', [accion for accion, estado in resultado.path()])
                    if resultado_verboso:
                        print('     meta:', repr(resultado.state))
                        print('     camino:', repr(resultado.path()))
                else:
                    print('     resultado:', str(resultado))
                print('    duraciÃ³n:', (fin - inicio).total_seconds())

                if limite_tiempo is not None:
                    validar_tiempo(inicio, fin, limite_tiempo, advertencias,
                                   'La prueba {} demorÃ³ demasiado tiempo (mÃ¡s de {} segundos), '
                                   'probablemente algo no estÃ¡ demasiado bien.'.format(
                                       numero_prueba,
                                       limite_tiempo))

                if resultado is None:
                    problemas.append('El resultado devuelto por la funciÃ³n resolver en la '
                                     'prueba {} fue None, cuando el problema tiene que '
                                     'encontrar soluciÃ³n y se espera que retorne el nodo '
                                     'resultante. Puede que la funciÃ³n resolver no estÃ© '
                                     'devolviendo el nodo resultante, o que el problema no estÃ© '
                                     'encontrando soluciÃ³n como deberÃ­a.'.format(numero_prueba))
                elif isinstance(resultado, SearchNode):
                    if limite_largo_camino and len(resultado.path()) > limite_largo_camino:
                        advertencias.append('El resultado devuelto en la prueba {} excede el '
                                            'largo de camino esperable ({}) para ese problema y '
                                            'mÃ©todo de bÃºsqueda. Es posible que algo no estÃ© '
                                            'bien.'.format(numero_prueba, limite_largo_camino))
                else:
                    problemas.append('El resultado devuelto por la funciÃ³n resolver en la '
                                     'prueba {} no es un nodo de bÃºsqueda.'.format(numero_prueba))

            except Exception as err:
                if saltear_errores:
                    problemas.append('Error al ejecutar {} ({})'.format(metodo_busqueda, str(err)))
                else:
                    raise


def probar_estadisticas():
    # abrir el archivo de estadisticas
    print('Abriendo estadÃ­sticas...')

    nombre_archivo = 'entrega1.txt'
    if not os.path.exists(nombre_archivo):
        problemas.append('No se pudo encontrar el archivo de estadÃ­sticas. Probablemente el '
                         'nombre del archivo no es correcto, o no estÃ¡ en la raiz del '
                         'repositorio.')
        return

    with open(nombre_archivo) as archivo_stats:
        lineas_stats = archivo_stats.readlines()

    # validar contenidos
    casos = list(range(1, 5))
    casos_pendientes = casos[:]

    for linea in lineas_stats:
        linea = linea.strip()
        if linea:
            try:
                caso, valores = linea.split(':')
                caso = int(caso)
                valores = list(map(int, valores.split(',')))
                if len(valores) != 4:
                    raise ValueError()

                if caso not in casos:
                    problemas.append('Caso desconocido en archivo de estadÃ­sticas: {}'.format(caso))
                elif caso not in casos_pendientes:
                    problemas.append('Caso repetido en archivo de estadÃ­sticas: {}'.format(caso))
                else:
                    print('   Encontrado caso', caso)
                    print('    Valores:', valores)
                    casos_pendientes.remove(caso)
            except:
                problemas.append('La siguiente linea de estadÃ­sticas no respeta el formato '
                                 'definido: {}'.format(linea))

    if casos_pendientes:
        problemas.append('No se incluyeron las estadÃ­sticas de los siguientes '
                         'casos: {}'.format(repr(casos_pendientes)))


def imprimir_resultados():
    def listar_cosas(titulo, cosas):
        if cosas:
            print(titulo + ':')
            for cosa in cosas:
                print('*', cosa)

    listar_cosas('Problemas que es necesario corregir', problemas)
    listar_cosas('Advertencias (cosas que pueden ser un problema, aunque no siempre)', advertencias)
    listar_cosas('Recomendaciones', recomendaciones)


if __name__ == '__main__':
    print()
    probar_codigo(interactivo='-i' in sys.argv,
                  saltear_errores='-s' in sys.argv,
                  resultado_verboso='-v' in sys.argv)
    print()
    probar_estadisticas()
    print()
    print('Pruebas automÃ¡ticas terminadas!')
    print()
    imprimir_resultados()