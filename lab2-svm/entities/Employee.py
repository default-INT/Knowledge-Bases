class Employee:

    def __init__(self, fullName, skills, post=None) -> None:
        super().__init__()
        self._fullName = fullName
        self._skills = skills
        self.post = post

    def getFullName(self):
        return self._fullName

    def setFullName(self, value):
        self._fullName = value

    def delFullName(self):
        del self._fullName

    def getSkills(self):
        return self._skills

    def setSkills(self, value):
        self._skills = value

    def delSkills(self):
        del self._skills

    fullName = property(getFullName, setFullName, delFullName)
    skills = property(getSkills, setSkills, delSkills)


class Position:

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)


class BreakerPosition(Position):

    def __init__(self) -> None:
        super().__init__('Сбойщик')


class HandymanPosition(Position):

    def __init__(self) -> None:
        super().__init__('Разнорабочий')
