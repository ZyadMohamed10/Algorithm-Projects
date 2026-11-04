import csv
import heapq
import random
import time
import matplotlib.pyplot as plt


def load_players():
    players = []
    with open("players.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            players.append((int(row["Value_EUR"]), row["Name"]))
    return players


def running_median_heaps(stream):
    low = []
    high = []
    medians = []
    for x in stream:
        if len(low) == 0 or x <= -low[0]:
            heapq.heappush(low, -x)
        else:
            heapq.heappush(high, x)

        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))

        if len(low) > len(high):
            medians.append(-low[0])
        else:
            medians.append((-low[0] + high[0]) / 2)
    return medians


def running_median_sorting(stream):
    medians = []
    for i in range(len(stream)):
        prefix = sorted(stream[:i + 1])
        m = len(prefix)
        if m % 2 == 1:
            medians.append(prefix[m // 2])
        else:
            medians.append((prefix[m // 2 - 1] + prefix[m // 2]) / 2)
    return medians


def best_time(func, stream, runs=3):
    best = None
    for _ in range(runs):
        start = time.perf_counter()
        func(stream)
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best:
            best = elapsed
    return best * 1000


if __name__ == "__main__":
    print("slide example [5, 15, 1, 3]:", running_median_heaps([5, 15, 1, 3]))

    players = load_players()
    random.Random(1).shuffle(players)

    print("\nscouting stream: median market value so far")
    values = [p[0] for p in players]
    medians = running_median_heaps(values)
    for i in range(8):
        print(players[i][1], "| value", players[i][0], "| median so far", medians[i])
    print("median of all", len(values), "players:", medians[-1])

    assert medians == running_median_sorting(values)

    sizes = [250, 500, 1000, 2000]
    heap_times = []
    sort_times = []
    print("\nn, heaps ms, sort every time ms")
    for n in sizes:
        stream = values[:n]
        heap_times.append(best_time(running_median_heaps, stream))
        sort_times.append(best_time(running_median_sorting, stream))
        print(n, round(heap_times[-1], 3), round(sort_times[-1], 3))

    plt.plot(sizes, heap_times, marker="o", label="two heaps")
    plt.plot(sizes, sort_times, marker="s", label="sort the prefix every time")
    plt.title("Running median of market value")
    plt.xlabel("n (number of players in the stream)")
    plt.ylabel("time (ms)")
    plt.legend()
    plt.grid(True)
    plt.savefig("result.png", dpi=120)
    plt.show()
