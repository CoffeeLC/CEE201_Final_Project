import networkx as nx

def node_map(path):
    G = nx.DiGraph()
    with open(path, "r") as f:
        for line in f:
            u, v, w = line.strip().split()
            u, v = int(u), int(v)
            w = float(w)
            G.add_edge(u, v, weight=w)
    return G

def forbidden_nodes(path):
    forbidden = set()
    with open(path, "r") as f:
        for line in f:
            try:
                forbidden.add(int(line.strip()))
            except ValueError:
                print(f"⚠️ Skipping invalid entry: '{line.strip()}'")
    return forbidden
