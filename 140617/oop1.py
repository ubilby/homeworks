"""
 Попробуйте перенести в ОО-код следующий пример из реального мира:
- есть курсы, учителя и ученики
- у каждого курса есть свой учитель
- у каждого учителя есть своя группа учеников

Определите какие объекты есть в этом примере, какие у них свойства и какие
методы, как эти объекты будут между собой взаимодействовать, например,
к курсу можно добавить учителя.

Создайте все необходимые классы и приведите пример их использования.

"""

class Courses(object):
    """класс курсы, может добавлять себе учителей, если требуется"""
    def __init__(self, title, teacher = None):
        self.title = title
        self.teachers = []

        if teacher is not None:
            self.add_teacher(teacher)


    def add_teacher(self, teacher):
        if not isinstance(teacher, Teacher):
            raise OrderException("Это не учитель")

        self.teachers.append(teacher)

        
class Teacher(object):
    """собсна класс учитель: инициализируется сразу с группой, иначе зачем его держать?)
    группу учителя можно расширить только студентами"""
    def __init__(self, name, *students):
        self.name = name
        self.students = [i for i in students]

    def add_students(*students):
        for i in students:
            if not isinstance(i, Student):
                raise OrderException("Это не ученик")

            self.students.append(i)
    
class Student(object):
    """студенты. могут пока только учиться)"""
    def __init__(self, name):
        self.name = name


student1 = Student("Ваня")
student2 = Student("Коля")
student3 = Student("Петя")
student4 = Student("Кирилл")

teacher1 = Teacher("Семен Семеныч", student1, student2, student3, student4)

courses1 = Courses("Python Разработчик", teacher1)

