import numpy as np

from neural_network.ObjectPrototype import ObjectPrototype


class PerceptionAlgorithm:

    def __init__(self, training_sample) -> None:
        """
        :param training_sample: Обучающая выборка, представляет собой двухмерный массив numpy.
                                1-ый столбец - объекты относящиеся к 1-ому классу.
                                2-ой столбец - объекты относящиеся ко 2-ому классу.
        """
        super().__init__()
        self._training_samples = training_sample
        self._weight = None

    def train(self, training_samples=None):
        if training_samples is None:
            training_samples = self._training_samples
        else:
            self._training_samples = training_samples

        sign_count = len(training_samples[0].signs)  # количество признаков у всех должно быть одинаково
        samples_count = len(training_samples)           # количество объектов в обучающей выборке

        # first_class_samples, second_class_samples = training_samples[:, 0], training_samples[:, 1]

        E = 0
        self._weight = np.zeros(shape=(sign_count+1))
        while E < len(training_samples):
            for sample in training_samples:
                scalar_sum = 0
                for i in range(sign_count):
                    scalar_sum += sample.signs[i] * self._weight[i]
                scalar_sum += self._weight[-1]
                if sample.class_type == 1:
                    if scalar_sum > 0:
                        E += 1
                    else:
                        for i in range(sign_count):
                            self._weight[i] += sample.signs[i]
                        self._weight[-1] += 1
                        E = 0
                elif sample.class_type == 2:
                    if scalar_sum < 0:
                        E += 1
                    else:
                        for i in range(sign_count):
                            self._weight[i] -= sample.signs[i]
                        self._weight[-1] -= 1
                        E = 0

    def fit(self, samples):
        for sample in samples:
            print(self._get_distance(sample))

    def _get_distance(self, sample):
        scalar_prod = 0
        for i in range(len(sample.signs)):
            scalar_prod += self._weight[i] * sample.signs[i]
        scalar_prod += self._weight[-1]
        return scalar_prod
