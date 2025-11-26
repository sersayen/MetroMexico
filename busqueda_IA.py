import networkx as nx # A*
import re # Regular Expresions 

# CREACION DE GRAFO

#Pesos: Tiempo en minutos entre las estaciones
Graph = nx.Graph()
#Linea 1
Graph.add_edge("Observatorio", "L1Tacubaya", weight = 2)
Graph.add_edge("L1Tacubaya", "Juanacatlan", weight = 2)
Graph.add_edge("Juanacatlan", "Chapultepec", weight = 2)
Graph.add_edge("Chapultepec", "Sevilla", weight = 1)
Graph.add_edge("Sevilla", "Insurgentes", weight = 2)
Graph.add_edge("Insurgentes", "Cuauhtemoc", weight = 2)
Graph.add_edge("Cuauhtemoc", "L1Balderas", weight = 1)

#Linea 3
Graph.add_edge("L3Balderas", "Juarez", weight = 1)
Graph.add_edge("Balderas", "Niños Heroes", weight = 1)
Graph.add_edge("Niños Heroes", "Hospital General", weight = 2)
Graph.add_edge("Hospital General", "L3Centro Medico", weight = 1)
Graph.add_edge("L3Centro Medico", "Etiopia", weight = 3)
Graph.add_edge("Etiopia", "Eugenia", weight = 2)
Graph.add_edge("Eugenia", "Division del Norte", weight = 1)
Graph.add_edge("Division del Norte", "L3Zapata", weight = 2)
Graph.add_edge("L3Zapata", "Coyoacan", weight = 2)
Graph.add_edge("Viveros", "Coyoacan", weight = 2)
Graph.add_edge("Viveros", "M.A De Quevedo", weight = 2)
Graph.add_edge("M.A De Quevedo", "Copilco", weight = 3)
Graph.add_edge("Universidad", "Copilco", weight = 2)

#Linea 7
Graph.add_edge("L7Mixcoac", "Barranca del Muerto", weight = 2)
Graph.add_edge("L7Mixcoac", "San Antonio", weight = 2)
Graph.add_edge("San Antonio", "San Pedro de los Pinos", weight = 1)
Graph.add_edge("L7Tacubaya", "San Pedro de los Pinos", weight = 2)
Graph.add_edge("L7Tacubaya", "Constituyentes", weight = 2)
Graph.add_edge("Constituyentes", "Auditorio", weight = 2)
Graph.add_edge("Auditorio", "Polanco", weight = 2)

#Linea 9
Graph.add_edge("L9Tacubaya", "Patriotismo", weight = 3)
Graph.add_edge("Patriotismo", "Chilpacingo", weight = 2)
Graph.add_edge("L9Centro Medico", "Chilpacingo", weight = 2)
Graph.add_edge("L9Centro Medico", "Lazaro Cardenas", weight = 2)

#Linea 12
Graph.add_edge("Insurgentes Sur", "L12Mixcoac", weight = 2)
Graph.add_edge("Hospital 20 de Noviembre", "Insurgentes Sur", weight = 1)
Graph.add_edge("L12Zapata", "Hospital 20 de Noviembre", weight = 2)
Graph.add_edge("L12Zapata", "Parque de los Venados", weight = 1)
Graph.add_edge("Eje Central", "Parque de los Venados", weight = 4)

#Trasbordos
Graph.add_edge("L12Mixcoac", "Mixcoac", weight = 2.5)
Graph.add_edge("L7Mixcoac", "Mixcoac", weight = 2.5)
Graph.add_edge("L12Zapata", "Zapata", weight = 2.5)
Graph.add_edge("L3Zapata", "Zapata", weight = 2.5)
Graph.add_edge("L9Centro Medico", "Centro Medico", weight = 2.5)
Graph.add_edge("L3Centro Medico", "Centro Medico", weight = 2.5)
Graph.add_edge("L3Balderas", "Balderas", weight = 2.5)
Graph.add_edge("L1Balderas", "Balderas", weight = 2.5)
Graph.add_edge("L9Tacubaya", "Tacubaya", weight = 2.5)
Graph.add_edge("L7Tacubaya", "Tacubaya", weight = 2.5)
Graph.add_edge("L1Tacubaya", "Tacubaya", weight = 2.5)


# DEFINICION DE CONSTANTES

DIFICIL_ACCESO = {
    "Chapultepec", "Insurgentes", "Etiopia", "Eugenia", "Division del Norte",
    "Coyoacan", "Lazaro Cardenas", "Mixcoac"
}
TRASBORDOS = {
    "Mixcoac", "Zapata", "Centro Medico", "Balderas", "Tacubaya"
}

FRANJAS_HORARIAS = [
    (7, 0, 9, 0),
    (18, 0, 20, 0)
]

FACTOR_HORA_PUNTA = 1.2
PENALIZACION_DISCAPACIDAD = 900

# INICIALIZACION DE VARIABLES
es_discapacitado = False
es_hora_punta = False


# DEFINICION DE METODOS:

def limpiar_nombre(estacion):
    return re.sub(r"^L\d+", "", estacion)

def limpiar_lista(nodos):
    lista_limpia = []
    for nodo in nodos:
        nodo =limpiar_nombre(nodo)
        if nodo not in lista_limpia:
            lista_limpia.append(nodo)
    return lista_limpia


def lista_nodos_grafo():
    return limpiar_lista(list(Graph.nodes))

def get_heuristica(start_node):
    def heuristica_final(actual, destino):
        try:
            saltos = nx.shortest_path_length(Graph, actual, destino)
        except nx.NetworkXNoPath:
            return float('inf')
        
        return saltos
    
    return heuristica_final


def calcular_ruta(salida, destino):
    G_temporal = Graph.copy()
    
    for u, v, data in G_temporal.edges(data=True):
        if es_hora_punta:
            data['weight'] = data['weight'] * FACTOR_HORA_PUNTA
        u_limpia = limpiar_nombre(u)
        v_limpia = limpiar_nombre(v)
        es_trasbordo = u_limpia == v_limpia
        if es_trasbordo and es_discapacitado and u_limpia in DIFICIL_ACCESO:
            data["weight"] = data["weight"] + PENALIZACION_DISCAPACIDAD/2
        if (u == salida or u == destino) or (v == salida or v == destino):
            data["weight"] = 0
    
    heuristica = get_heuristica(salida)
    camino = nx.astar_path(G_temporal, salida, destino, heuristic=heuristica, weight="weight")
    tiempo_total = nx.astar_path_length(G_temporal, salida, destino, heuristic=heuristica, weight="weight")
    
    camino = limpiar_lista(camino)
    for nodo in camino:
        print(nodo)
    
    if es_discapacitado:
        for estacion in camino:
            if estacion != salida and estacion != destino and estacion in DIFICIL_ACCESO and estacion in TRASBORDOS:
                tiempo_total = tiempo_total - PENALIZACION_DISCAPACIDAD
     

    return camino, tiempo_total
