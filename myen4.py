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
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def _avg_grade(self):
        grades = [g for course in self.grades.values() for g in course]
        return round(sum(grades) / len(grades), 1) if grades else 0

    def __str__(self):
        avg = self._avg_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) or 'Нет'
        finished_courses = ', '.join(self.finished_courses) or 'Нет'
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за ДЗ: {avg}\n"
                f"Курсы в процессе: {courses_in_progress}\n"
                f"Завершённые курсы: {finished_courses}")

    def __lt__(self, other):
        if not isinstance(other, Student):
            raise TypeError("Нельзя сравнить студента с другим типом")
        return self._avg_grade() < other._avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._avg_grade() == other._avg_grade()


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

    def _avg_grade(self):
        grades = [g for course in self.grades.values() for g in course]
        return round(sum(grades) / len(grades), 1) if grades else 0

    def __str__(self):
        avg = self._avg_grade()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg}"

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            raise TypeError("Нельзя сравнить лектора с другим типом")
        return self._avg_grade() < other._avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._avg_grade() == other._avg_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'


# === Функции для средней оценки по курсу ===
def avg_student_grade(students, course):
    all_grades = [g for s in students for g in s.grades.get(course, [])]
    return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0

def avg_lecturer_grade(lecturers, course):
    all_grades = [g for l in lecturers for g in l.grades.get(course, [])]
    return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0


# === Создание экземпляров ===
s1 = Student('Анна', 'Петрова', 'female')
s2 = Student('Иван', 'Смирнов', 'male')
s1.courses_in_progress += ['Python', 'Git']
s1.finished_courses += ['Введение в программирование']
s2.courses_in_progress += ['Python']
s2.finished_courses += ['Английский']
s1.grades = {'Python': [9, 8, 10], 'Git': [7, 9]}
s2.grades = {'Python': [10, 10, 9]}

l1 = Lecturer('Олег', 'Булыгин')
l2 = Lecturer('Елена', 'Никитина')
l1.courses_attached = l2.courses_attached = ['Python']
l1.grades = {'Python': [9, 10, 8]}
l2.grades = {'Python': [7, 8, 9]}

r1 = Reviewer('Сергей', 'Грин')
r2 = Reviewer('Мария', 'Лопес')
r1.courses_attached = r2.courses_attached = ['Python']

# === Вызов методов ===
s1.rate_lecture(l1, 'Python', 10)
s2.rate_lecture(l2, 'Python', 8)
r1.rate_hw(s1, 'Python', 9)
r2.rate_hw(s1, 'Git', 8)

# === Вывод ===
print("=== Студенты ===\n", s1, '\n\n', s2, sep='')
print("\n=== Лекторы ===\n", l1, '\n\n', l2, sep='')
print("\n=== Проверяющие ===\n", r1, '\n\n', r2, sep='')
print("\n=== Сравнения ===")
print("student1 < student2:", s1 < s2)
print("lecturer1 > lecturer2:", l1 > l2)
print("\n=== Средние оценки по курсу ===")
print("Средняя оценка студентов (Python):", avg_student_grade([s1, s2], 'Python'))
print("Средняя оценка лекторов (Python):", avg_lecturer_grade([l1, l2], 'Python'))