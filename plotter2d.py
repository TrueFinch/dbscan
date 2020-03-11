import sys
from typing import List
import dbscan
import random


def main(argv: List[str] = None) -> int:
    with open("input.txt", 'r') as fin:
        params = list(fin.readline().split())
        n = int(params[0])

        db: List[dbscan.Point] = []
        for i in range(n):
            db.append(dbscan.Point(list(map(float, fin.readline().split()))))

    if db[0].get_dimension() != 2:
        return 0



    return 0


if __name__ == "__main__":
    sys.exit(main())
