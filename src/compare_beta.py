import networkx as nx

def compare_price_difference(cost_beta):
    keys = sorted(cost_beta.keys())
    base_B = keys[0]
    base_cost = cost_beta[base_B]
    print(f"\n📊 Price difference compared to B = {base_B}:")
    for B in keys[1:]:
        diff = base_cost - cost_beta[B]
        print(f"B = {B}: Difference = {diff:.2f}")

def compare_best_case(cost_best, cost_beta):
    print("\n📊 Cost difference vs. unrestricted path:")
    for B, cost in sorted(cost_beta.items()):
        diff = cost - cost_best
        print(f"B = {B}: Difference = {diff:.2f}")
