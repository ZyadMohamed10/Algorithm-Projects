import random
import unittest
from hybrid_sort_lab import hybrid_sort, load_players


def sort_with(values, cutoff):
    A = [(v, "x") for v in values]
    hybrid_sort(A, 0, len(A) - 1, cutoff)
    return [a[0] for a in A]


class TestHybridSort(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(sort_with([], 4), [])

    def test_one_element(self):
        self.assertEqual(sort_with([5], 4), [5])

    def test_duplicates(self):
        self.assertEqual(sort_with([3, 1, 3, 1, 3], 2), [1, 1, 3, 3, 3])

    def test_sorted(self):
        self.assertEqual(sort_with([1, 2, 3, 4, 5, 6], 2), [1, 2, 3, 4, 5, 6])

    def test_reversed(self):
        self.assertEqual(sort_with([6, 5, 4, 3, 2, 1], 2), [1, 2, 3, 4, 5, 6])

    def test_random(self):
        for k in [1, 4, 16]:
            values = [random.randint(0, 50) for _ in range(100)]
            self.assertEqual(sort_with(values, k), sorted(values))

    def test_real_players(self):
        players = load_players()
        data = players[:]
        hybrid_sort(data, 0, len(data) - 1, 16)
        self.assertEqual(data, sorted(players, key=lambda p: p[0]))


if __name__ == "__main__":
    unittest.main()
