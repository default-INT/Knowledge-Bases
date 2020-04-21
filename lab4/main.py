from neural_network import ImageUtils, HopfieldNetwork


def str_array_img(array_img):
    _str = ''
    for i in range(array_img.shape[0]):
        if array_img[i] <= 0:
            _str += ' '
        else:
            _str += '█'
        if (i + 1) % 10 == 0:
            _str += '\n'
    return _str


if __name__ == '__main__':
    iu = ImageUtils()
    iu.read_images()
    training_samples = iu.convert_to_binary()

    print("Изображение для обучения")
    for img in training_samples:
        print(str_array_img(img))

    hn = HopfieldNetwork(training_samples)
    hn.train()

    print("Тестовое изображение")
    test_img = ImageUtils.read_image_on_path('img_samples/T_20.bmp')
    print(str_array_img(test_img))

    result = hn.fit(test_img)
    print("Изображение после преобразования сетью Хопфилда.")
    print(str_array_img(result))