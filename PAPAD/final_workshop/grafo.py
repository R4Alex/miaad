import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

def get_grafo(model):
    # Crear grafo dirigido
    G = nx.DiGraph()

    # ======================= Build Grafo
    #  Planta → Centro
    for p in model.P:
        for c in model.C:
            for k in model.K:
                val = model.x[p, c, k].value
                if val and val > 0:
                    G.add_edge(f"P:{p}", f"C:{c}", weight=val, label=f"{k}:{val:.0f}")

    #  Centro → Cliente
    for c in model.C:
        for j in model.J:
            for k in model.K:
                val = model.y[c, j, k].value
                if val and val > 0:
                    G.add_edge(f"C:{c}", f"J:{j}", weight=val, label=f"{k}:{val:.0f}")

    # ======================= 
    grados_salida = Counter(dict(G.out_degree()))
    grados_entrada = Counter(dict(G.in_degree()))

    text_list = []

    print("\n\nGrado de salida (nodos con más conexiones salientes):")
    text_list.append("\n\nGrado de salida (nodos con más conexiones salientes):")
    create_image(grados_salida.most_common(10), "image1.png")
    for nodo, grado in grados_salida.most_common(10):
        print(f"{nodo}: {grado}")
        text_list.append(f"{nodo}: {grado}")

    print(" Grado de entrada (nodos con más conexiones entrantes):")
    text_list.append("\n\nGrado de entrada (nodos con más conexiones entrantes):")
    create_image(grados_entrada.most_common(10), "image2.png")
    for nodo, grado in grados_entrada.most_common(10):
        print(f"{nodo}: {grado}")
        text_list.append(f"{nodo}: {grado}")

    # =======================

    print(" Centros con mayor salida (distribuyen a más clientes):")
    text_list.append("\n\nCentros con mayor salida (distribuyen a más clientes):")
    node_list = []
    for nodo, grado in grados_salida.items():
        if nodo.startswith("C:"):
            print(f"{nodo} → {grado} clientes")
            text_list.append(f"{nodo} → {grado} clientes")
            node_list.append((nodo, grado))
    create_image(node_list, "image3.png")


    print(" Centros con mayor entrada (reciben de más plantas):")
    text_list.append("\n\nCentros con mayor entrada (reciben de más plantas):")
    node_list = []
    for nodo, grado in grados_entrada.items():
        if nodo.startswith("C:"):
            print(f"{nodo} ← {grado} plantas")
            text_list.append(f"{nodo} ← {grado} plantas")
            node_list.append((nodo, grado))
    create_image(node_list, "image4.png")
    return text_list


def create_image(data, name):
    frame = pd.DataFrame(data, columns=["Centro", "Cantidad"])
    frame.plot(x='Centro', y='Cantidad', kind='bar')
    plt.title(name)
    plt.subplots_adjust(bottom=0.3)
    plt.savefig(name)
