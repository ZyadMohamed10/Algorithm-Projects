import csv
import random
import time
import matplotlib.pyplot as plt


def load_players():
    players = []
    with open("players.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            players.append((int(row["Overall"]), row["Name"]))
    return players


def insertion_sort(arr):
    comps = 0
    shifts = 0
    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1
        while i >= 0:
            comps += 1
            if arr[i][0] > key[0]:
                arr[i + 1] = arr[i]
                shifts += 1
                i -= 1
            else:
                break
        arr[i + 1] = key
    return comps, shifts


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i][0] <= right[j][0]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i][0] > arr[i + 1][0]:
            return False
    return True


def make_data(players, case, n):
    if case == "Sorted":
        return sorted(players[:n], key=lambda p: p[0])
    if case == "Reverse":
        return sorted(players[:n], key=lambda p: p[0], reverse=True)
    sample = players[:]
    random.Random(n).shuffle(sample)
    return sample[:n]


def best_time(func, data, runs=7):
    best = None
    for _ in range(runs):
        copy = data[:]
        start = time.perf_counter()
        func(copy)
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best:
            best = elapsed
    return best * 1000


players = load_players()
sizes = [100, 250, 500, 1000, 2000]
cases = ["Sorted", "Reverse", "Random"]
times = {}
merge_times = []

print("case, n, comparisons, shifts, insertion ms")
for case in cases:
    times[case] = []
    for n in sizes:
        data = make_data(players, case, n)

        test = data[:]
        comps, shifts = insertion_sort(test)
        assert is_sorted(test)

        t = best_time(insertion_sort, data)
        times[case].append(t)
        print(case, n, comps, shifts, round(t, 3))

        if case == "Random":
            assert is_sorted(merge_sort(data))
            merge_times.append(best_time(merge_sort, data))

print("\nn, worst case comparisons, n(n-1)/2, best case comparisons, n-1")
for n in sizes:
    worst, _ = insertion_sort(make_data(players, "Reverse", n))
    best, _ = insertion_sort(make_data(players, "Sorted", n))
    print(n, worst, n * (n - 1) // 2, best, n - 1)

print("\nn, insertion ms (random), merge ms (random)")
for i in range(len(sizes)):
    print(sizes[i], round(times["Random"][i], 3), round(merge_times[i], 3))

for case in cases:
    plt.plot(sizes, times[case], marker="o", label="Insertion - " + case)
plt.plot(sizes, merge_times, marker="s", linestyle="--", label="Merge - Random")
plt.title("Insertion Sort on FIFA 19 players")
plt.xlabel("n (number of players)")
plt.ylabel("time (ms)")
plt.legend()
plt.grid(True)
plt.savefig("result.png", dpi=120)
plt.show()
