import unittest
from pass_network_lab import build_graph, bfs, path_to, dfs_path, load_passes, team_graph, goalkeeper


class TestPassNetwork(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": {"B", "C"},
            "B": {"D"},
            "C": {"D"},
            "D": {"E"},
            "E": set(),
            "F": set(),
        }

    def test_bfs_distances(self):
        dist, parent = bfs(self.graph, "A")
        self.assertEqual(dist, {"A": 0, "B": 1, "C": 1, "D": 2, "E": 3})

    def test_unreachable_vertex(self):
        dist, parent = bfs(self.graph, "A")
        self.assertNotIn("F", dist)

    def test_path_rebuild(self):
        dist, parent = bfs(self.graph, "A")
        path = path_to(parent, "E")
        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "E")

    def test_start_alone(self):
        dist, parent = bfs({"X": set()}, "X")
        self.assertEqual(dist, {"X": 0})

    def test_dfs_path_is_valid(self):
        path = dfs_path(self.graph, "A", "E")
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "E")
        for i in range(len(path) - 1):
            self.assertIn(path[i + 1], self.graph[path[i]])

    def test_build_graph(self):
        rows = [{"passer": "P1", "recipient": "P2"}, {"passer": "P2", "recipient": "P3"}]
        graph = build_graph(rows)
        self.assertEqual(graph, {"P1": {"P2"}, "P2": {"P3"}, "P3": set()})

    def test_real_final(self):
        rows = load_passes()
        graph = team_graph(rows, "8658", "France")
        gk = goalkeeper(rows, "8658", "France")
        dist, parent = bfs(graph, gk)
        self.assertEqual(gk, "Hugo Lloris")
        self.assertGreaterEqual(len(dist), 10)
        for player in dist:
            self.assertLessEqual(dist[player], len(dfs_path(graph, gk, player)) - 1)


if __name__ == "__main__":
    unittest.main()
