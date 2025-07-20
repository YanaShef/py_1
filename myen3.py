class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress and 0 <= grade <= 10:
            self.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def _get_average(self):
        grades = [g for subj in self.grades.values() for g in subj]
        return round(sum(grades) / len(grades), 1) if grades else 0

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self._get_average()}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress) or 'Нет'}\n"
                f"Завершённые курсы: {', '.join(self.finished_courses) or 'Нет'}")

    def __lt__(self, other):
        if not isinstance(other, Student): raise TypeError("Сравнение возможно только между студентами")
        return self._get_average() < other._get_average()

    def __eq__(self, other):
        if not isinstance(other, Student): return NotImplemented
        return self._get_average() == other._get_average()

    def __le__(self, other): return self < other or self == other
    def __gt__(self, other): return not self <= other
    def __ge__(self, other): return not self < other
    def __ne__(self, other): return not self == other


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _get_average(self):
        grades = [g for subj in self.grades.values() for g in subj]
        return round(sum(grades) / len(grades), 1) if grades else 0

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self._get_average()}"

    def __lt__(self, other):
        if not isinstance(other, Lecturer): raise TypeError("Сравнение возможно только между лекторами")
        return self._get_average() < other._get_average()

    def __eq__(self, other):
        if not isinstance(other, Lecturer): return NotImplemented
        return self._get_average() == other._get_average()

    def __le__(self, other): return self < other or self == other
    def __gt__(self, other): return not self <= other
    def __ge__(self, other): return not self < other
    def __ne__(self, other): return not self == other


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'


# Примеры
student1 = Student('Ruoy', 'Eman', 'your_gender')
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']
student1.grades['Python'] = [9, 8, 10]
student1.grades['Git'] = [7, 9]

student2 = Student('Alice', 'Smith', 'female')
student2.courses_in_progress += ['Python']
student2.grades['Python'] = [10, 10, 9]

lecturer1 = Lecturer('Иван', 'Иванов')
lecturer1.grades['Python'] = [9, 10, 8]

lecturer2 = Lecturer('Петр', 'Петров')
lecturer2.grades['Python'] = [7, 8, 9]

reviewer = Reviewer('Пётр', 'Сидоров')

# Вывод
print('--- Студенты ---')
print(student1)
print('\n')
print(student2)

print('\n--- Лекторы ---')
print(lecturer1)
print('\n')
print(lecturer2)

print('\n--- Проверяющий ---')
print(reviewer)

# Сравнение
print("\nСравнение студентов:")
print("student1 < student2:", student1 < student2)
print("student1 > student2:", student1 > student2)

print("\nСравнение лекторов:")
print("lecturer1 < lecturer2:", lecturer1 < lecturer2)
print("lecturer1 > lecturer2:", lecturer1 > lecturer2)