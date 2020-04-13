class ObjectPrototype:
    """
    Сужающий класс, который хранит признаки объектов.
    """

    def __init__(self, class_type=0, signs=[]) -> None:
        super().__init__()
        self.class_type = class_type
        self.signs = signs
