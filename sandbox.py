from sklearn.cluster import DBSCAN
import numpy as np

X = np.array([[-1, 1], [0, 1], [1, 1], [-1, -1], [0, -1], [1, -1], [0, 0]])

clustering = DBSCAN(eps=1, min_samples=3).fit(X)