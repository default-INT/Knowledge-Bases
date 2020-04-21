import numpy as np
import cv2

activation_func = lambda x: (1 - np.exp(-2 * x)) / (1 + np.exp(-2 * x))


class ImageUtils:

    def __init__(self, paths=None) -> None:
        super().__init__()
        if paths is None:
            paths = ['img_samples/T1.bmp', 'img_samples/P1.bmp', 'img_samples/O1.bmp']
        self.paths = paths
        self.images = []

    def read_images(self):
        self.images = []
        for path in self.paths:
            self.images.append(cv2.imread(path))
        return self.images

    @staticmethod
    def read_image_on_path(path):
        return ImageUtils.to_binary_matrix(cv2.imread(path))

    def convert_to_binary(self):
        bin_images = []
        for image in self.images:
            bin_images.append(self.to_binary_matrix(image))
        return bin_images

    @staticmethod
    def to_binary_matrix(img):
        bin_img = []
        for iheight in range(img.shape[0]):
            for iwidth in range(img.shape[1]):
                val = np.average(img[iheight][iwidth])
                if val == 0:
                    val = 1
                else:
                    val = -1
                bin_img.append(val)
        return np.array(bin_img)


class HopfieldNetwork:

    def __init__(self, train_samples) -> None:
        super().__init__()
        self.count_neurons = train_samples[0].shape[0]
        self.train_samples = train_samples
        self.weights = np.zeros(shape=(self.count_neurons, self.count_neurons))

    def train(self):
        for sample in self.train_samples:
            self.weights += sample * sample.reshape(len(sample), 1)
        self.weights /= self.count_neurons
        self.weights *= 1 - np.identity(self.count_neurons)

    def fit(self, sample):
        result = activation_func(self.weights.dot(sample.reshape(len(sample), 1)) / 2)  # f(W*X * 1/2)
        return result.flatten()
