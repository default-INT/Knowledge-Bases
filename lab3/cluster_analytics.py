import numpy as np


def distance_Euclid(point1, point2):
    return np.sum((point1 - point2) ** 2)


class ClusterAnalytics:

    def __init__(self, samples) -> None:
        """

        :param samples: numpy массив, где строки - объекты, столбцы - признаки объектов
        """
        super().__init__()
        self.samples = samples

    def average_K_method(self, count_cluster=2):
        s = 0
        prototypes = []
        cluster_list = []
        count_samples = self.samples.shape[0]
        max_distance = 0

        i = 0
        while i < count_cluster:
            prototypes.append(self.samples[i])
            cluster_list.append([])
            i += 1

        while True:
            for sample in self.samples:
                min_distance = 0
                cluster_index = 0
                for i in range(len(prototypes)):
                    distance = distance_Euclid(sample, prototypes[i])
                    if distance < min_distance:
                        cluster_index = i
                        min_distance = distance
                cluster_list[cluster_index].append(sample)
            new_prototypes = []

            for cluster in cluster_list:
                prototype = np.zeros(shape=cluster[0].shape)
                for sample in cluster:
                    prototype += sample
                new_prototypes.append(prototype / len(cluster))

            if prototype != new_prototypes:
                prototype = new_prototypes
            else:
                return cluster_list
