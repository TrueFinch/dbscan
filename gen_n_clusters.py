import sys
from typing import List, Tuple, Dict
import dbscan
import random
import numpy as np
from queue import Queue


def gen_cluster(dim: int, eps: float, center: Tuple[float, float], cluster_points_number: int) -> dbscan.Cluster:
    result: dbscan.Cluster = dbscan.Cluster.cluster_of([])
    circle_center = list(center)
    if dim > 2:
        for i  in range(dim - 2):

    for i in range(0, cluster_points_number):

    return result


def gen_clusters(dim: int, eps: float, cluster_points_number: List[int]) -> List[dbscan.Cluster]:
    clusters: Dict[Tuple[int, int], dbscan.Cluster] = {}
    queue: Queue[Tuple[int, int]] = Queue()
    queue.put((0, 0))
    for points_number in cluster_points_number:
        center: Tuple[int, int] = queue.get()
        clusters[center] = gen_cluster(dim, eps, (center[0] * eps + center[0], center[1] * eps + center[1]),
                                       points_number)
        neighbors = [(center[0] + 1, center[1]), (center[0] - 1, center[1]),
                     (center[0], center[1] + 1), (center[0], center[1] - 1)]
        for p in neighbors:
            if p not in clusters:
                queue.put(p)

    return list(clusters.values())


# n - common clusters number
# Returns min_ptr and clusters points number in tuple
def get_clusters_points_number(n: int) -> Tuple[int, List[int]]:
    min_p_variants: List[int] = list(range(1, 21))
    min_p: int = 0
    while len(min_p_variants) > 0:
        min_p = random.choice(min_p_variants)
        if min_p * n > 500:
            min_p = 0
            min_p_variants.remove(min_p)
            continue
        break

    assert min_p > 0, "Error while cluster generation, try to generate less clusters"

    clusters_points_number: List[int] = [min_p] * n
    points_count = random.randint(min_p * n, 500)

    i = 0
    while points_count < min_p:
        new_points = random.randint(0, min_p if min_p < points_count else points_count)
        clusters_points_number[i % n] += new_points
        points_count -= new_points
        i += 1

    return min_p, clusters_points_number


def main(argv: List[str] = None) -> int:
    if len(argv) < 2:
        return 1
    # clusters number
    n: int = int(argv[0])
    # count of dimensions
    d: int = int(argv[1])
    assert d <= 10, "Wrong number of dimensions"

    e = random.uniform(1, 2)

    min_p, points_number = get_clusters_points_number(n)

    clusters: List[dbscan.Cluster] = gen_clusters(d, e, points_number)

    with open("input.txt", "w") as fout:
        fout.write('{} {} {} {:.2f}\n'.format(n, d, min_p, e))
        cluster: dbscan.Cluster
        for cluster in clusters:
            point: dbscan.Point
            for point in cluster.points:
                fout.write(point.to_string() + '\n')
    fout.close()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
