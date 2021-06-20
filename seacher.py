import numpy as np
import csv


def euclid_distance(histA, histB):
    n = len(histA) // 4
    results = []
    for i in range(4):
        x, y = i * n, i * n + n
        d = np.sum([(a - b) ** 2 for (a, b) in zip(histA[x:y], histB[x:y])]) ** 0.5
        results.append(d)
    return results


class Searcher:
    def __init__(self, _indexPath):
        self.indexPath = _indexPath

    def search(self, queryFeatures):
        queryFeatures = np.array(queryFeatures)
        results = {}

        with open(self.indexPath) as f:
            reader = csv.reader(f)
            for row in reader:
                features = [float(x) for x in row[1:]]
                features = np.array(features)
                d = euclid_distance(features, queryFeatures)
                results[row[0]] = max(d)
                print("{}: {} --> Max: {}".format(row[0], d, results[row[0]]))

            f.close()
        results = sorted([(v, k) for (k, v) in results.items()])
        return results


