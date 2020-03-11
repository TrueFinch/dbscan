import sys
from typing import List
import dbscan
import matplotlib.pyplot as plt


def main(argv: List[str] = None) -> int:
    points: List[dbscan.Point] = []
    n: int
    d: int
    p: int
    e: float
    with open("input.txt", 'r') as fin, open('output.txt', 'w') as fout:
        params = list(fin.readline().split())
        n = int(params[0])
        d = int(params[1])
        p = int(params[2])
        e = float(params[3])

        for i in range(n):
            points.append(dbscan.Point(list(map(float, fin.readline().split()))))

        scan: dbscan.Scanner = dbscan.Scanner(points, p, e)
        clusters = scan.dbscan()
        print(str(len(clusters)))

        # draw 2d clusters
        plt.figure(dpi=300)
        noise_points = [point for point in points if point.type == dbscan.PointType.NOISE]
        x = [point.coordinates[0] for point in noise_points]
        y = [point.coordinates[1] for point in noise_points]
        plt.scatter(x, y, s=2, label='noise')

        for cluster in clusters:
            x = [point.coordinates[0] for point in cluster.points]
            y = [point.coordinates[1] for point in cluster.points]
            plt.scatter(x, y, s=5, label='cluster {}'.format(cluster.id))

        plt.xlabel("x - axis")
        plt.ylabel("y - axis")
        plt.title("Clusters")
        plt.legend()
        plt.savefig('clusters.svg', dpi=300)
        plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())
