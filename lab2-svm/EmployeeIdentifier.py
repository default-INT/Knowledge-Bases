import numpy as np

from entities.Employee import Employee, BreakerPosition, HandymanPosition
from entities.Skill import Skill, CountPalletSkill, NumberPacksDaySkill
from neural_network.MinimumDistanceSVM import MinimumDistanceSVM
from neural_network.ObjectPrototype import ObjectPrototype
from neural_network.PerceptionAlgorithm import PerceptionAlgorithm


class EmployeeIdentifier:
    """
    Класс занимающийся определением должности для сотрудников.
    """

    def __init__(self, employees=[]) -> None:
        super().__init__()
        self._employees = employees
        self._test_employees = np.array([
            Employee('Трофимов Е.В.', [  # 1 объект класс 1
                CountPalletSkill(100),
                NumberPacksDaySkill(1)
            ], BreakerPosition()),
            Employee('Солодков М.А.', [  # 2 объект класс 2
                CountPalletSkill(20),
                NumberPacksDaySkill(15)
            ], HandymanPosition()),
            Employee('Межейников А.С.', [  # 3 объект класс 2
                CountPalletSkill(20),
                NumberPacksDaySkill(9)
            ], HandymanPosition()),
            Employee('Семёнов Д.С.', [  # 4 объект класс 1
                CountPalletSkill(110),
                NumberPacksDaySkill(4)
            ], BreakerPosition()),
            Employee('Стольный Д.С.', [  # 5 объект класс 2
                CountPalletSkill(20),
                NumberPacksDaySkill(13)
            ], HandymanPosition()),
            Employee('Ропот И.В.', [  # 6 объект класс 1
                CountPalletSkill(120),
                NumberPacksDaySkill(4)
            ], BreakerPosition()),
            Employee('Дворак И.В.', [  # 7 объект класс 1
                CountPalletSkill(145),
                NumberPacksDaySkill(2)
            ], BreakerPosition()),
            Employee('Липский Д.Ю.', [  # 8 объект класс 2
                CountPalletSkill(15),
                NumberPacksDaySkill(10)
            ], HandymanPosition()),
            Employee('Белько Э.В.', [  # 9 объект класс 2
                CountPalletSkill(15),
                NumberPacksDaySkill(5)
            ], HandymanPosition()),
            Employee('Давыдчик А.Е.', [  # 10 объект класс 1
                CountPalletSkill(130),
                NumberPacksDaySkill(2)
            ], BreakerPosition())
        ])
        self._prototypes = EmployeeIdentifier._dimensionless_conversion(self._test_employees)
        self._training_set = EmployeeIdentifier._get_training_set(self._prototypes)
        # self._composite_employees()
        self._minimum_distance_method = MinimumDistanceSVM(self._training_set)
        self._minimum_distance_method.train()

        self._perception_algorithm = PerceptionAlgorithm(self._prototypes)
        self._perception_algorithm.train()

    def add_employee(self, employee):
        self._employees.append(employee)

    def find_jobs(self):
        empl_prototypes = EmployeeIdentifier._dimensionless_conversion(np.concatenate((self._test_employees, np.array(self._employees))))
        self._minimum_distance_method.fit(empl_prototypes[len(self._test_employees):])
        self._perception_algorithm.fit(empl_prototypes[len(self._test_employees):])

    @staticmethod
    def _dimensionless_conversion(employees):
        prototypes = []
        count_signs = len(employees[0].skills)
        count_employees = len(employees)

        for _ in employees:
            prototypes.append(ObjectPrototype(signs=np.zeros(shape=2)))

        for i in range(count_signs):
            max_val = 0
            for employee in employees:
                if employee.skills[i].mark > max_val:
                    max_val = employee.skills[i].mark
            for j in range(count_employees):
                prototypes[j].signs[i] = employees[j].skills[i].mark / max_val
                if isinstance(employees[j].post, BreakerPosition):
                    prototypes[j].class_type = 1
                elif isinstance(employees[j].post, HandymanPosition):
                    prototypes[j].class_type = 2

        return prototypes

    @staticmethod
    def _get_training_set(prototypes):
        training_list_class1, training_list_class2 = [], []
        for prototype in prototypes:
            if prototype.class_type == 1:
                training_list_class1.append(prototype)
            elif prototype.class_type == 2:
                training_list_class2.append(prototype)

        return np.column_stack((training_list_class1, training_list_class2))

    def _composite_employees(self):
        self._prototypes = []
        count_signs = len(self._test_employees[0].skills)
        count_employees = len(self._test_employees)

        for _ in self._test_employees:
            self._prototypes.append(ObjectPrototype(signs=np.zeros(shape=2)))

        for i in range(count_signs):
            max_val = 0
            for employee in self._test_employees:
                if employee.skills[i].mark > max_val:
                    max_val = employee.skills[i].mark
            for j in range(count_employees):
                self._prototypes[j].signs[i] = self._test_employees[j].skills[i].mark / max_val
                if isinstance(self._test_employees[j].post, BreakerPosition):
                    self._prototypes[j].class_type = 1
                elif isinstance(self._test_employees[j].post, HandymanPosition):
                    self._prototypes[j].class_type = 2

        # следовательно должно быть (50 на 50) элементов каждого из классов
        training_list_class1, training_list_class2 = [], []
        for prototype in self._prototypes:
            if prototype.class_type == 1:
                training_list_class1.append(prototype)
            elif prototype.class_type == 2:
                training_list_class2.append(prototype)

        self._training_set = np.column_stack((training_list_class1, training_list_class2))


employee_identifier = EmployeeIdentifier()

employee_identifier.add_employee(Employee('Пискун Е.А.', [
                CountPalletSkill(150),
                NumberPacksDaySkill(3)
            ], BreakerPosition())
)

employee_identifier.find_jobs()
