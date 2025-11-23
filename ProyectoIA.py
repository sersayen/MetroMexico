#!pip3 install networkx
import networkx as nx
import matplotlib.pyplot as plt

#Pesos: Tiempo en minutos entre las estaciones
Graph = nx.Graph()
#Linea 1
Graph.add_edge("Observatorio", "Tacubaya", weight = 2)
Graph.add_edge("Tacubaya", "Juanacatlan", weight = 2)
Graph.add_edge("Juanacatlan", "Chapultepec", weight = 2)
Graph.add_edge("Chapultepec", "Sevilla", weight = 1)
Graph.add_edge("Sevilla", "Insurgentes", weight = 2)
Graph.add_edge("Insurgentes", "Cuauhtemoc", weight = 2)
Graph.add_edge("Cuauhtemoc", "Balderas", weight = 1)

#Linea 3
Graph.add_edge("Balderas", "Juarez", weight = 1)
Graph.add_edge("Balderas", "Niños Heroes", weight = 1)
Graph.add_edge("Niños Heroes", "Hospital General", weight = 2)
Graph.add_edge("Hospital General", "Centro Medico", weight = 1)
Graph.add_edge("Centro Medico", "Etiopia", weight = 3)
Graph.add_edge("Etiopia", "Eugenia", weight = 2)
Graph.add_edge("Eugenia", "Division del Norte", weight = 1)
Graph.add_edge("Division del Norte", "Zapata", weight = 2)
Graph.add_edge("Zapata", "Coyoacan", weight = 2)
Graph.add_edge("Viveros", "Coyoacan", weight = 2)
Graph.add_edge("Viveros", "M.A De Quevedo", weight = 2)
Graph.add_edge("M.A De Quevedo", "Copilco", weight = 3)
Graph.add_edge("Universidad", "Copilco", weight = 2)

#Linea 7
Graph.add_edge("Mixcoac", "Barranca del Muerto", weight = 2)
Graph.add_edge("Mixcoac", "San Antonio", weight = 2)
Graph.add_edge("San Antonio", "San Pedro de los Pinos", weight = 1)
Graph.add_edge("Tacubaya", "San Pedro de los Pinos", weight = 2)
Graph.add_edge("Tacubaya", "Constituyentes", weight = 2)
Graph.add_edge("Constituyentes", "Auditorio", weight = 2)
Graph.add_edge("Auditorio", "Polanco", weight = 2)

#Linea 9
Graph.add_edge("Tacubaya", "Patriotismo", weight = 3)
Graph.add_edge("Patriotismo", "Chilpacingo", weight = 2)
Graph.add_edge("Centro Medico", "Chilpacingo", weight = 2)
Graph.add_edge("Centro Medico", "Lazaro Cardenas", weight = 2)

#Linea 12
Graph.add_edge("Insurgentes Sur", "Mixcoac", weight = 2)
Graph.add_edge("Hospital 20 de Noviembre", "Insurgentes Sur", weight = 1)
Graph.add_edge("Zapata", "Hospital 20 de Noviembre", weight = 2)
Graph.add_edge("Zapata", "Parque de los Venados", weight = 1)
Graph.add_edge("Eje Central", "Parque de los Venados", weight = 4)

lineas = {
    frozenset({"Observatorio", "Tacubaya"}) : "L1", frozenset({"Tacubaya", "Juanacatlan"}) : "L1",
    frozenset({"Juanacatlan", "Chapultepec"}) : "L1", frozenset({"Chapultepec", "Sevilla"}) : "L1",
    frozenset({"Sevilla", "Insurgentes"}) : "L1", frozenset({"Insurgentes", "Cuauhtemoc"}) : "L1",
    frozenset({"Cuauhtemoc", "Balderas"}) : "L1", frozenset({"Balderas", "Juarez"}) : "L3",
    frozenset({"Balderas", "Niños Heroes"}) : "L3", frozenset({"Niños Heroes", "Hospital General"}) : "L3",
    frozenset({"Hospital General", "Centro Medico"}) : "L3", frozenset({"Centro Medico", "Etiopia"}) : "L3",
    frozenset({"Etiopia", "Eugenia"}) : "L3", frozenset({"Eugenia", "Division del Norte"}) : "L3",
    frozenset({"Division del Norte", "Zapata"}) : "L3", frozenset({"Zapata", "Coyoacan"}) : "L3",
    frozenset({"Viveros", "Coyoacan"}) : "L3", frozenset({"Viveros", "M.A De Quevedo"}) : "L3",
    frozenset({"M.A De Quevedo", "Copilco"}) : "L3", frozenset({"Universidad", "Copilco"}) : "L3",
    frozenset({"Mixcoac", "Barranca del Muerto"}) : "L7", frozenset({"Mixcoac", "San Antonio"}) : "L7",
    frozenset({"San Antonio", "San Pedro de los Pinos"}) : "L7", frozenset({"Tacubaya", "San Pedro de los Pinos"}) : "L7",
    frozenset({"Tacubaya", "Constituyentes"}) : "L7", frozenset({"Constituyentes", "Auditorio"}) : "L7",
    frozenset({"Auditorio", "Polanco"}) : "L7", frozenset({"Tacubaya", "Patriotismo"}) : "L9",
    frozenset({"Patriotismo", "Chilpacingo"}) : "L9", frozenset({"Centro Medico", "Chilpacingo"}) : "L9",
    frozenset({"Centro Medico", "Lazaro Cardenas"}) : "L9", frozenset({"Insurgentes Sur", "Mixcoac"}) : "L12",
    frozenset({"Hospital 20 de Noviembre", "Insurgentes Sur"}) : "L12", frozenset({"Zapata", "Hospital 20 de Noviembre"}) : "L12",
    frozenset({"Zapata", "Parque de los Venados"}) : "L12", frozenset({"Eje Central", "Parque de los Venados"}) : "L12",

}
def get_linea(u, v):
    return lineas.get(frozenset({u, v}))

penalizaciones_transbordo = {
    "Tacubaya": 5,
    "Centro Medico":4,
    "Zapata": 3,
    "Mixcoac":3,
    "Balderas":3,
}

dificil_acceso = {
    "Chapultepec", "Insurgentes", "Etiopia", "Eugenia", "Division del Norte",
    "Coyoacan", "Lazaro Cardenas",
}

estado = "hora_punta"
factor_hora = 1.2 if estado == "hora_punta" else 1.0


def get_heuristica(start_node):
    def heuristica_final(actual, destino):
        try:
            saltos = nx.shortest_path_length(Graph, actual, destino)
        except nx.NetworkXNoPath:
            return float('inf')
        h = saltos * factor_hora
    
        penalizacion_transbordos = 0
        penalizacion_accesibilidad = 0
        if actual in penalizaciones_transbordo:
            penalizacion_transbordos += penalizaciones_transbordo[actual]
        if actual in dificil_acceso:
            penalizacion_accesibilidad += 3
        return h + penalizacion_transbordos + penalizacion_accesibilidad
    return heuristica_final

def penalizacion_total(path, salida):
    total = 0
    path_len = len(path)
    if salida in dificil_acceso:
        total += 3
    for i in range(1, path_len - 1):
        actual = path[i]
        prev = path[i - 1]
        sig = path[i + 1]
        if actual in penalizaciones_transbordo:
            linea_salida = get_linea(prev, actual)
            linea_llegada = get_linea(actual, sig)
            if linea_salida != linea_llegada:
                total += penalizaciones_transbordo[actual]
    return total


def calcular_ruta(salida, destino):
    heuristica = get_heuristica(salida)
    camino = nx.astar_path(Graph, salida, destino, heuristic=heuristica, weight="weight")
    dist = nx.astar_path_length(Graph, salida, destino, heuristic=heuristica, weight="weight")
    penalizacion = penalizacion_total(camino, salida)
    tiempo_total = dist + penalizacion
    return camino, tiempo_total


#print(nx.astar_path(Graph, "Polanco", "Universidad", heuristic = heuristica_final, weight="weight"))
#print(nx.astar_path_length (Graph, "Polanco", "Universidad", heuristic = heuristica_final, weight="weight"))

