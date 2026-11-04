import random
import unittest
from running_median_lab import running_median_heaps, running_median_sorting


class TestRunningMedian(unittest.TestCase):
    def test_slide_example(self):
        self.assertEqual(running_median_heaps([5, 15, 1, 3]), [5, 10, 5, 4])

    def test_empty(self):
        self.assertEqual(running_median_heaps([]), [])

    def test_one_element(self):
        self.assertEqual(running_median_heaps([7]), [7])

    def test_duplicates(self):
        self.assertEqual(running_median_heaps([2, 2, 2, 2]), [2, 2, 2, 2])

    def test_sorted_and_reversed(self):
        self.assertEqual(running_median_heaps([1, 2, 3, 4, 5]), [1, 1.5, 2, 2.5, 3])
        self.assertEqual(running_median_heaps([5, 4, 3, 2, 1]), [5, 4.5, 4, 3.5, 3])

    def test_random_against_sorting(self):
        rng = random.Random(5)
        for _ in range(100):
            stream = [rng.randint(0, 30) for _ in range(rng.randint(0, 60))]
            self.assertEqual(running_median_heaps(stream), running_median_sorting(stream))


if __name__ == "__main__":
    unittest.main()
