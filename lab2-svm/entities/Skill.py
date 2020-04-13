class Skill:

    def __init__(self, name, mark) -> None:
        super().__init__()
        self._name = name
        self._mark = mark

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    def delName(self):
        del self._name

    def getMark(self):
        return self._mark

    def setMark(self, value):
        self._mark = value

    def delMark(self):
        del self._mark

    name = property(getName, setName, delName)
    mark = property(getMark, setMark, delMark)


class CountPalletSkill(Skill):

    def __init__(self, mark) -> None:
        super().__init__('Количество поддонов в день', mark)


class NumberPacksDaySkill(Skill):

    def __init__(self, mark) -> None:
        super().__init__('Количество собраных пачек досок за час', mark)
