import numpy as np

from neural_network.ObjectPrototype import ObjectPrototype


class MinimumDistanceSVM:

    def __init__(self, training_sample) -> None:
        """
        :param training_sample: Обучающая выборка, представляет собой двухмерный массив numpy.
                                1-ый столбец - объекты относящиеся к 1-ому классу.
                                2-ой столбец - объекты относящиеся ко 2-ому классу.
        """
        super().__init__()
        self._training_samples = training_sample
        self._prototype1 = None
        self._prototype2 = None

    def train(self, training_samples=None):
        if training_samples is None:
            training_samples = self._training_samples
        else:
            self._training_samples = training_samples

        sign_count = len(training_samples[0][0].signs)  # количество признаков у всех должно быть одинаково
        samples_count = len(training_samples)  # количество объектов в обучающей выборке

        self._prototype1 = ObjectPrototype(class_type=1, signs=np.zeros(shape=sign_count))
        self._prototype2 = ObjectPrototype(class_type=2, signs=np.zeros(shape=sign_count))

        first_class_samples, second_class_samples = training_samples[:, 0], training_samples[:, 1]

        for sign_i in range(sign_count):
            avg_x1, avg_x2 = 0, 0

            for samples in training_samples:
                avg_x1, avg_x2 = samples[0].signs[sign_i], samples[1].signs[sign_i]
            avg_x1, avg_x2 = avg_x1 / samples_count, avg_x2 / samples_count

            self._prototype1.signs[sign_i] = avg_x1
            self._prototype2.signs[sign_i] = avg_x2
        pass

    def fit(self, samples):
        for sample in samples:
            print(self._get_distance(sample))

    def _get_distance(self, sample):
        scalar_prod1_class1, scalar_prod2_class1 = 0, 0
        scalar_prod1_class2, scalar_prod2_class2 = 0, 0
        for i in range(len(self._prototype1.signs)):
            scalar_prod1_class1 += self._prototype1.signs[i] * sample.signs[i]
            scalar_prod2_class1 += self._prototype1.signs[i] ** 2

            scalar_prod1_class2 += self._prototype2.signs[i] * sample.signs[i]
            scalar_prod2_class2 += self._prototype2.signs[i] ** 2
        return (scalar_prod1_class1 * 2 - scalar_prod2_class1), (scalar_prod1_class2 * 2 - scalar_prod2_class2)
