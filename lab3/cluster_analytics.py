import numpy as np


def distance_Euclid(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))


def get_rand_index(max_index, prev_index):
    k = np.random.randint(max_index)
    for i in prev_index:
        if i == k:
            return get_rand_index(max_index, prev_index)
    return k


class ClusterAnalytics:

    def __init__(self, samples) -> None:
        """

        :param samples: numpy массив, где строки - объекты, столбцы - признаки объектов
        """
        super().__init__()
        self.samples = samples

    @staticmethod
    def _find_cluster_for_obj(samples, prototypes, cluster_list):
        """
        Распределение объектов по кластерам.
        P.S. Требуется за ранее знать размерность cluster_list, + cluster_list должен быть пустой.
        Можно его создавать в этом методе, но не сегодня.
        :param samples: np.array - список объектов выборки.
        :param prototypes: за ранее найденные прототипы каждого кластера.
        P.S. Кол-во объектов в списке, равно кол-ву кластеров.
        :param cluster_list: Список состоящий из списков хранящие объекты определённого кластера.
        P.S. i-ый элемент 1-го списка, равняется i-му кластеру.
        :return: None
        """
        for sample in samples:
            min_distance = distance_Euclid(sample, prototypes[0])
            cluster_index = 0
            for i in range(len(prototypes)):
                distance = distance_Euclid(sample, prototypes[i])
                if distance < min_distance:
                    cluster_index = i
                    min_distance = distance
            cluster_list[cluster_index].append(sample)

    def average_K_method(self, count_cluster=2):
        """
        Реализация метода K-средних
        :param count_cluster: Кол-во кластреров (классов)
        :return: cluster_list - список состоящий из списков хранящие объекты определённого кластера (класса).
        P.S. i-ый элемент 1-го списка, равняется i-му кластеру.
        """
        prototypes, cluster_list, count_samples, smpl_index = [], [], self.samples.shape[0], []

        i = 0
        # выбираются из множества два случайных объекта в качестве прототипа
        while i < count_cluster:
            rand_index = get_rand_index(count_samples, smpl_index)
            prototypes.append(self.samples[rand_index])
            smpl_index.append(rand_index)
            cluster_list.append([])
            i += 1

        while True:
            # отнесение объектов в определённый кластер
            self._find_cluster_for_obj(self.samples, prototypes, cluster_list)
            new_prototypes = []

            for cluster in cluster_list:
                prototype = np.zeros(shape=cluster[0].shape)
                for sample in cluster:
                    prototype += sample
                new_prototypes.append(prototype / len(cluster))

            if (np.array(prototypes) == np.array(new_prototypes)).all():
                prototypes = new_prototypes
            else:
                return cluster_list

    def maximin_method(self):
        """
        Реализация метода максимина.
        :return: cluster_list - список состоящий из списков хранящие объекты определённого кластера (класса).
        P.S. i-ый элемент 1-го списка, равняется i-му кластеру.
        """
        prototypes, count_samples = [self.samples[0]], len(self.samples)

        max_distance, max_index = 0, None

        # Определения расстояния от 1го прототипа до всех остальных объектов и нахождения наиболее удалённого.
        for i in range(count_samples):
            distance = distance_Euclid(self.samples[i], prototypes[0])
            if max_distance < distance:
                max_distance, max_index = distance, i

        prototypes.append(self.samples[max_index])

        # Опредеоение порогового расстояния
        T = distance_Euclid(prototypes[0], prototypes[1]) / 2

        cluster_list = [[], []]

        while True:
            self._find_cluster_for_obj(self.samples, prototypes, cluster_list)

            check = True
            for i in range(len(prototypes)):
                max_distance, far_sample = 0, None
                for sample in cluster_list[i]:
                    distance = distance_Euclid(sample, prototypes[i])
                    if max_distance < distance:
                        max_distance, far_sample = distance, sample

                if max_distance > T:
                    prototypes.append(far_sample)
                    check = False

            if check:
                return cluster_list
            else:
                distance_sum, cluster_list, count_prototypes = 0, [], len(prototypes)

                for k in range(count_prototypes - 1):
                    cluster_list.append([])
                    for j in range(k, count_prototypes):
                        distance_sum += distance_Euclid(prototypes[k], prototypes[j])
                cluster_list.append([])
                T = distance_sum / (count_prototypes * (count_prototypes - 1))
