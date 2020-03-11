from __future__ import annotations

from enum import Enum

from typing import List, Optional
from numpy import linalg
import numpy


class PointType(Enum):
    NONE = 0
    NOISE = 1
    CORE = 2
    EDGE = 3


class Point:
    __id__ = 0

    def __init__(self, a_coords: Optional[List[float]] = None):
        self.coordinates: List[float] = [] if a_coords is None else a_coords
        self.id: int = Point.__id__
        Point.__id__ += 1
        self.type: PointType = PointType.NONE
        self.color: int = -1

    def getDistance(self, p: Point) -> float:
        return linalg.norm(numpy.array(self.coordinates) - numpy.array(p.coordinates))

    def to_string(self) -> str:
        return " ".join(["{:.2f}".format(coord) for coord in self.coordinates])

    def get_dimension(self) -> int:
        return len(self.coordinates)


class Cluster:
    __id__ = 0
    __ids__ = []

    @staticmethod
    def cluster_of(a_points: List[Point], color: int = None) -> Cluster:
        return Cluster(a_points, color)

    def __init__(self, a_points: Optional[List[Point]] = None, color: int = None):
        self.points: List[Point] = []
        if a_points is not None:
            self.points = a_points
        if color not in Cluster.__ids__:
            self.id = color
        else:
            while Cluster.__id__ in Cluster.__ids__:
                Cluster.__id__ += 1
            self.id = Cluster.__id__
            Cluster.__id__ += 1

        Cluster.__ids__.append(self.id)


class Scanner:
    def __init__(self, database: List[Point], min_ptr: int, epsilon: float):
        self.points: List[Point] = database
        self.min_ptr: int = min_ptr
        self.eps: float = epsilon
        self.clusters: List[Cluster] = []
        # self.point_id = []
        # self.all_dist = self.__calculate_all_distances__()

    # def __calculate_all_distances__(self) -> List[List[float]]:
    #     result = [[] * len(self.db)] * len(self.db)
    #     for point in self.db:
    #         result
    #     return result

    def get_neighbours(self, point: Point) -> List[Point]:
        result: List[Point] = []
        for p in self.points:
            if point.id != p.id and point.getDistance(p) <= self.eps:
                result.append(p)
        return result

    def dbscan(self) -> List[Cluster]:
        for point in self.points:
            if point.type != PointType.NONE:
                continue
            neighbours = self.get_neighbours(point)
            if (len(neighbours) + 1) < self.min_ptr:
                point.type = PointType.NOISE
                continue
            self.clusters.append(Cluster.cluster_of([point]))
            point.type = PointType.CORE
            point.color = self.clusters[len(self.clusters) - 1].id
            self.__grow_cluster__(neighbours, point.color)
        return self.clusters

    def __grow_cluster__(self, neighbours: List[Point], cluster_id: int):
        for point in neighbours:
            if point.type == PointType.NOISE:
                point.type = PointType.EDGE
                self.clusters[cluster_id].points.append(point)
            if point.type != PointType.NONE:
                continue
            point.color = cluster_id
            point.type = PointType.EDGE
            self.clusters[cluster_id].points.append(point)
            new_neighbours: List[Point] = [p for p in self.get_neighbours(point)]
            if (len(new_neighbours) + 1) > self.min_ptr:
                point.type = PointType.CORE
                neighbours.extend([p for p in new_neighbours if p.type == PointType.NOISE or p.type == PointType.NONE])
