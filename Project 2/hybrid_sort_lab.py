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


def insertion_sort_part(A, p, r):
    for j in range(p + 1, r + 1):
        key = A[j]
        i = j - 1
        while i >= p and A[i][0] > key[0]:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key


def merge(A, p, q, r):
    L = A[p:q + 1]
    R = A[q + 1:r + 1]
    i = 0
    j = 0
    k = p
    while i < len(L) and j < len(R):
        if L[i][0] <= R[j][0]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1
        k += 1
    while i < len(L):
        A[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        A[k] = R[j]
        j += 1
        k += 1


def hybrid_sort(A, p, r, cutoff):
    if r - p + 1 <= cutoff:
        insertion_sort_part(A, p, r)
        return
    q = (p + r) // 2
    hybrid_sort(A, p, q, cutoff)
    hybrid_sort(A, q + 1, r, cutoff)
    merge(A, p, q, r)


def is_sorted(A):
    for i in range(len(A) - 1):
        if A[i][0] > A[i + 1][0]:
            return False
    return True


def run_time(data, cutoff, runs=15):
    best = None
    for _ in range(runs):
        A = data[:]
        start = time.perf_counter()
        hybrid_sort(A, 0, len(A) - 1, cutoff)
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best:
            best = elapsed
    assert is_sorted(A)
    return best * 1000


if __name__ == "__main__":
    players = load_players()
    sizes = [500, 1000, 2000]
    cutoffs = [1, 2, 4, 8, 16, 32, 64, 128]

    print("n, cutoff, time ms")
    results = {}
    for n in sizes:
        data = players[:]
        random.Random(n).shuffle(data)
        data = data[:n]
        results[n] = []
        for k in cutoffs:
            t = run_time(data, k)
            results[n].append(t)
            print(n, k, round(t, 3))

    print("\nn, best cutoff, hybrid ms, merge sort ms (k=1), insertion sort ms")
    for n in sizes:
        times = results[n]
        best_index = times.index(min(times))
        data = players[:]
        random.Random(n).shuffle(data)
        data = data[:n]
        print(n, cutoffs[best_index], round(times[best_index], 3), round(times[0], 3), round(run_time(data, n, 3), 3))

    for n in sizes:
        plt.plot(cutoffs, results[n], marker="o", label="n = " + str(n))
    plt.xscale("log", base=2)
    plt.title("Hybrid sort: time vs cutoff k")
    plt.xlabel("cutoff k")
    plt.ylabel("time (ms)")
    plt.legend()
    plt.grid(True)
    plt.savefig("result.png", dpi=120)
    plt.show()
