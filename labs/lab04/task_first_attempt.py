import logging

logging.basicConfig(filename="school.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Student:
    def __init__(self, number: int, first_name: str, last_name: str):
        self.number = number
        self.first_name = first_name
        self.last_name = last_name
        # self.classes = []

    def __str__(self):
        return f"Number: {self.number}, First name: {self.first_name}, Second name: {self.last_name}"


class AddStudentError(ValueError):
    pass


class Class:
    def __init__(self, class_id: int, student_limit: int = 30):
        self.class_id = class_id
        self.student_limit = student_limit
        self.students = []

    def add_student_dict(self, student_dict):
        if len(self.students) >= self.student_limit:
            raise AddStudentError("Cannot add a new student - the limit for this class has been already reached.")
        else:
            self.students.append(student_dict)

    def remove_student(self, student_number: int):
        pass


class School:
    def __init__(self):
        self.classes = []

    def add_class(self, class_: Class):
        self.classes.append(class_)

    def get_student_total_avg_score(self, student_number: int) -> float:
        score_sum = 0
        classes_num = 0

        for c in self.classes:
            for s_d in c.student_dicts:
                if s_d.student.number == student_number:
                    for score in s_d.scores:
                        score_sum += score
                classes_num += 1

        return score_sum / classes_num

    def get_student_avg_score_in_class(self, student_number: int, class_: Class):
        pass


if __name__ == "__main__":
    s1 = School()
    c1 = Class(1, 15)
    c1.add_student_dict(Student(1, "Anna", "Smith"))
    s1.add_class(c1)

