def count_red_zones_in_path(path, red_zones):
    return len(set(u for u, v in path).union(v for u, v in path) & red_zones)

def print_solution(label, path, cost, status):
    print(f"--- {label} ---")
    if status == 1:
        print("✅ Optimal solution found")
        #print(f"Path: {path}")
        print(f"Total cost: {cost}")
    else:
        print("❌ No optimal solution found")
    print()
