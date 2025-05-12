from pulp import *

def solve_shortest_path(G, source, target, forbidden=None, budget=None):
    model = LpProblem("Shortest_Path", LpMinimize)
    edge_vars = LpVariable.dicts("Edge", G.edges(), cat="Binary")

    # Objective: Minimize travel cost
    model += lpSum(G[u][v]['weight'] * edge_vars[(u, v)] for u, v in G.edges())

    # Flow constraints
    for node in G.nodes():
        inflow = lpSum(edge_vars[(u, v)] for u, v in G.in_edges(node))
        outflow = lpSum(edge_vars[(u, v)] for u, v in G.out_edges(node))

        if node == source:
            model += (outflow - inflow == 1)
        elif node == target:
            model += (inflow - outflow == 1)
        else:
            model += (inflow == outflow)

    # Block red zones if given
    if forbidden and budget is not None:
        y_vars = LpVariable.dicts("Y", forbidden, cat="Binary")
        for n in forbidden:
            for u, v in G.in_edges(n):
                if (u, v) in edge_vars:
                    model += edge_vars[(u, v)] <= y_vars[n]
            for u, v in G.out_edges(n):
                if (u, v) in edge_vars:
                    model += edge_vars[(u, v)] <= y_vars[n]
        model += lpSum(y_vars[n] for n in forbidden) <= budget
    elif forbidden:
        for n in forbidden:
            for u, v in list(G.in_edges(n)) + list(G.out_edges(n)):
                if (u, v) in edge_vars:
                    model += edge_vars[(u, v)] == 0

    status = model.solve(PULP_CBC_CMD(msg=False))
    path = [(u, v) for u, v in G.edges() if value(edge_vars[(u, v)]) == 1]
    cost = sum(G[u][v]['weight'] for u, v in path)
    return path, cost, status
