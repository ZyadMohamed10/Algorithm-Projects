import csv
import time
from collections import deque
import matplotlib.pyplot as plt


def load_passes():
    with open("passes.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_graph(rows):
    graph = {}
    for r in rows:
        graph.setdefault(r["passer"], set()).add(r["recipient"])
        graph.setdefault(r["recipient"], set())
    return graph


def bfs(graph, start):
    dist = {start: 0}
    parent = {start: None}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in sorted(graph[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)
    return dist, parent


def path_to(parent, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]


def dfs_path(graph, start, target):
    visited = set()
    path = []

    def visit(u):
        visited.add(u)
        path.append(u)
        if u == target:
            return True
        for v in sorted(graph[u]):
            if v not in visited and visit(v):
                return True
        path.pop()
        return False

    visit(start)
    return path


def team_graph(rows, match_id, team):
    return build_graph([r for r in rows if r["match_id"] == match_id and r["team"] == team])


def goalkeeper(rows, match_id, team):
    for r in rows:
        if r["match_id"] == match_id and r["team"] == team and r["passer_position"] == "Goalkeeper":
            return r["passer"]


def best_time(func, runs=3):
    best = None
    for _ in range(runs):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best:
            best = elapsed
    return best * 1000


def full_traversal(graph):
    seen = set()
    for node in graph:
        if node not in seen:
            dist, parent = bfs(graph, node)
            seen.update(dist)
    return len(seen)


if __name__ == "__main__":
    rows = load_passes()
    final = "8658"

    for team in ["France", "Croatia"]:
        graph = team_graph(rows, final, team)
        gk = goalkeeper(rows, final, team)
        dist, parent = bfs(graph, gk)
        edges = sum(len(v) for v in graph.values())
        print("\n" + team + ": " + str(len(graph)) + " players, " + str(edges) + " pass links")
        print("goalkeeper:", gk)
        for player in sorted(dist, key=dist.get):
            print("  ", dist[player], "passes:", " -> ".join(path_to(parent, player)))
        print("average passes from the goalkeeper:", round(sum(dist.values()) / (len(dist) - 1), 2))

        far = max(dist, key=dist.get)
        shortest = path_to(parent, far)
        any_path = dfs_path(graph, gk, far)
        print("to", far, "- BFS:", len(shortest) - 1, "passes, DFS:", len(any_path) - 1, "passes")

    match_ids = []
    for r in rows:
        if r["match_id"] not in match_ids:
            match_ids.append(r["match_id"])

    print("\nmatches, V, E, V+E, traversal time (microseconds), microseconds per (V+E)")
    xs = []
    ys = []
    for m in range(1, len(match_ids) + 1):
        subset = [r for r in rows if r["match_id"] in match_ids[:m]]
        graph = build_graph(subset)
        v = len(graph)
        e = sum(len(x) for x in graph.values())
        t = best_time(lambda: [full_traversal(graph) for _ in range(200)]) / 200 * 1000
        xs.append(v + e)
        ys.append(t)
        print(m, v, e, v + e, round(t, 1), round(t / (v + e), 3))

    plt.plot(xs, ys, marker="o")
    plt.title("BFS over the whole pass graph: time vs V + E")
    plt.xlabel("V + E")
    plt.ylabel("time (microseconds)")
    plt.grid(True)
    plt.savefig("result.png", dpi=120)
    plt.show()
