class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: можно оценивать только лекторов'
        if course not in lecturer.courses_attached:
            return 'Ошибка: лектор не прикреплён к данному курсу'
        if course not in self.courses_in_progress:
            return 'Ошибка: вы не изучаете данный курс'
        if grade not in range(0, 11):
            return 'Ошибка: оценка вне диапазона (0-10)'

        lecturer.grades.setdefault(course, []).append(grade)
        return 'Оценка учтена'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            return 'Ошибка: можно оценивать только студентов'
        if course not in self.courses_attached:
            return 'Ошибка: вы не прикреплены к данному курсу'
        if course not in student.courses_in_progress:
            return 'Ошибка: студент не изучает данный курс'
        if grade not in range(0, 11):
            return 'Ошибка: оценка вне диапазона (0-10)'

        student.grades.setdefault(course, []).append(grade)
        return 'Оценка учтена'


# Проверка:
lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Ольга', 'Алёхина', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

# Тестируем метод rate_lecture()
print(student.rate_lecture(lecturer, 'Python', 7))  # Оценка учтена
print(student.rate_lecture(lecturer, 'Java', 8))  # Ошибка: лектор не прикреплён к данному курсу
print(student.rate_lecture(lecturer, 'C++', 8))  # Ошибка: вы не изучаете данный курс
print(student.rate_lecture(reviewer, 'Python', 6))  # Ошибка: можно оценивать только лекторов

print(lecturer.grades)  # {'Python': [7]}

# Тестируем метод rate_hw()
print(reviewer.rate_hw(student, 'Python', 9))  # Оценка учтена
print(reviewer.rate_hw(student, 'C++', 5))  # Ошибка: студент не изучает данный курс

print(student.grades)  # {'Python': [9]}