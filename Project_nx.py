from pulp import *
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------
# STEP 1: Load Graph from File
# ----------------------------
G = nx.DiGraph()
with open("data/small_test.txt", "r") as f:
    for line in f:
        u, v, w = map(int, line.strip().split())
        G.add_edge(u, v, weight=w)

# ----------------------------
# STEP 2: Shortest Path Solver
# ----------------------------
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
        #Budget tolerance
        y_vars = LpVariable.dicts("Y",forbidden,cat="Binary")
        for n in forbidden:
            red_edges = list(G.in_edges(n)) + list(G.out_edges(n))
            edge_sum = lpSum(edge_vars[(u,v)] for u,v in red_edges if (u,v) in edge_vars)
            model += edge_sum <=100*y_vars[n]
        model += lpSum(y_vars[n] for node in forbidden) <= budget
    elif forbidden:
        for n in forbidden:
            for u, v in list(G.in_edges(n)) + list(G.out_edges(n)):
                if (u, v) in edge_vars:
                    model += edge_vars[(u, v)] == 0

    status = model.solve(PULP_CBC_CMD(msg=False))
    path = [(u, v) for u, v in G.edges() if value(edge_vars[(u, v)]) == 1]
    cost = sum(G[u][v]['weight'] for u, v in path)
    return path, cost, status

# ----------------------------
# STEP 3: Output Formatter
# ----------------------------
def print_solution(label, path, cost, status):
    print(f"--- {label} ---")
    if status == 1:
        print("✅ Optimal solution found")
        print(f"Path: {path}")
        print(f"Total cost: {cost}")
    else:
        print("❌ No optimal solution found")
    print()

# ----------------------------
# STEP 4: Run Question 1 & 2
# ----------------------------
source = 0
target = max(G.nodes())
red_zones = {3, 7}
beta = 0

# Unrestricted
path_unrestricted, cost_unrestricted, status_unrestricted = solve_shortest_path(G, source, target)
print_solution("Unrestricted Path", path_unrestricted, cost_unrestricted, status_unrestricted)

# Restricted (Avoid red zones)
path_restricted, cost_restricted, status_restricted = solve_shortest_path(G, source, target, forbidden=red_zones)
print_solution("Restricted Path (Avoid Red Zones)", path_restricted, cost_restricted, status_restricted)

# Price of Unjustness
if status_unrestricted == 1 and status_restricted == 1:
    print(f"🧮 Price of Unjustness: {cost_restricted - cost_unrestricted}")

# Question 3: Budgeted tolerance
budget = 1
path_budgeted, cost_budgeted, status_budgeted = solve_shortest_path(
    G, source, target, forbidden=red_zones, budget=budget
)
print_solution(f"Budgeted Path (B = {budget})", path_budgeted, cost_budgeted, status_budgeted)
