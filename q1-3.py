from src.graph_loader import node_map, forbidden_nodes
from src.shortest_path_solver import solve_shortest_path
from src.utils import print_solution, count_red_zones_in_path
from src.compare_beta import compare_price_difference, compare_best_case

def budget_analysis():
    G = node_map("data/small_test.txt")
    cameras = forbidden_nodes("data/small_cameras.txt")

    nodes = list(G.nodes)
    source = 0
    target = 9

    path_best, cost_best, status_best = solve_shortest_path(G,source,target)
    
    cost_with_budget = {}
    for B in [0,1,2]:
        path, cost, status = solve_shortest_path(G, source, target, forbidden=cameras, budget=B)
        print_solution(f"Chicago: Budgeted Camera Use (B = {B})", path, cost, status)
        if status == 1:
            used = count_red_zones_in_path(path, cameras)
            print(f"🔍 Camera streets actually used: {used} \n")
            cost_with_budget[B] = cost
    if cost_with_budget:
        compare_price_difference(cost_with_budget)
        compare_best_case(cost_best,cost_with_budget)
 

if __name__ == "__main__":
    budget_analysis()
