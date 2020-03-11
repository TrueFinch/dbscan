import sys
from typing import List
import dbscan
import random
import numpy as np


def main(argv: List[str] = None) -> int:
    if len(argv) < 6:
        return 1
    n: int = int(argv[0])
    d: int = int(argv[1])
    p: int = int(argv[2])
    e: float = int(argv[3])
    min_coord: int = int(argv[4])
    max_coord: int = int(argv[5])

    points: List[dbscan.Point] = []

    i: int = 0
    while i < n:
        new_point: dbscan.Point = dbscan.Point([random.uniform(min_coord, max_coord) for j in range(0, d)])
        if new_point not in points:
            points.append(new_point)
            i += 1

    with open("input.txt", "w") as fout:
        fout.write('{} {} {} {:.2f}\n'.format(n, d, p, e))
        point: dbscan.Point
        for point in points:
            fout.write(point.to_string() + '\n')
    fout.close()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
