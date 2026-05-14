import math
from collections import Counter
import sys

def calculate_entropy(degrees):
    n = len(degrees)
    if n == 0:
        return 0.0
    counter = Counter(degrees)
    probs = [count / n for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)

def simulate_growth(N_max):
    degrees = [0, 1, 1]  # degrees[0] не используется, вершины 1 и 2
    counter = Counter(degrees)
    n_vertices = 2
    max_deg_history = [1]

    for t in range(3, N_max + 1):
        degrees.append(0)
        n_vertices += 1

        best_u = None
        best_entropy = -float('inf')
        best_u_new_deg = -1

        for u in range(1, t):
            old_deg_u = degrees[u]
            new_deg_u = old_deg_u + 1

            # временно обновляем counter
            counter[old_deg_u] -= 1
            if counter[old_deg_u] == 0:
                del counter[old_deg_u]
            counter[new_deg_u] = counter.get(new_deg_u, 0) + 1
            counter[1] = counter.get(1, 0) + 1

            new_entropy = calculate_entropy([counter[d] for d in sorted(counter.keys()) for _ in range(counter[d])])

            if (new_entropy > best_entropy or
                (abs(new_entropy - best_entropy) < 1e-10 and
                 (best_u is None or
                  (new_deg_u > best_u_new_deg or
                   (new_deg_u == best_u_new_deg and u < best_u))))):
                best_entropy = new_entropy
                best_u = u
                best_u_new_deg = new_deg_u

            # откатываем изменения
            counter[new_deg_u] -= 1
            if counter[new_deg_u] == 0:
                del counter[new_deg_u]
            counter[old_deg_u] = counter.get(old_deg_u, 0) + 1
            counter[1] -= 1
            if counter[1] == 0:
                del counter[1]

        # фиксируем лучшее решение
        old_deg = degrees[best_u]
        degrees[best_u] += 1
        degrees[t] = 1

        counter[old_deg] -= 1
        if counter[old_deg] == 0:
            del counter[old_deg]
        counter[degrees[best_u]] = counter.get(degrees[best_u], 0) + 1
        counter[1] = counter.get(1, 0) + 1

        max_deg_history.append(max(degrees))

        if t % 1000 == 0:
            print(f"Progress: N={t}, max degree={max(degrees)}")

    return max_deg_history, degrees

if __name__ == "__main__":
    N_MAX = 10000
    print(f"Running simulation up to N = {N_MAX}")
    max_deg, final_deg = simulate_growth(N_MAX)
    print(f"\nSimulation finished. Max degree = {max_deg[-1]}")