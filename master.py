# Ben Liao, Christine Lu, Lily Sai

from classes import *
from math import ceil

class Master:

    def __init__(self, periods):
        self.master = []
        for i in range(len(Teacher.teacher_lst)):
            lst = []
            for j in range(periods):
                lst.append(None)
            self.master.append(lst)

    def add_section(self, teacher, period, section):
        self.master[teacher][period - 1] = section

    def add_prep(self, teacher, period):
        self.master[teacher][period - 1] = "PREP"

    def init_sections(self):
        # find teacher to teach course
        for course in COURSE_NAMES:
            course_teacher = ""
            for teacher in Teacher.teacher_lst:
                if course in teacher.courses:
                    course_teacher = teacher
                    break

            num_sections = ceil(len(courses[course].student_ids) / MAX_SECTION_ENROLLMENT) # find number of sections to fil
            teacher_index = Teacher.teacher_lst.index(course_teacher) # get index of row that represents teacher's schedule so far

            count = num_sections
            while count > 0 and (None in self.master[teacher_index]): # while we still have sections to create
                for period in range(1, len(self.master[teacher_index]) + 1): # find the next open period, create a new section, then add it
                    if (self.master[teacher_index][period - 1] == None): # if nothing there right now, add the section
                        section = Section(num_sections - count, period, course)
                        self.add_section(teacher_index, period, section)
                        courses[course].add_section(section)
                        count -= 1
                        break

    def fill_sections(self):
        classless = []
        for student in Student.student_lst:
            for course_name in student.course_names:
                try:
                    course = courses[course_name]
                    course.enroll_student(student)
                except AtCapacityException:
                    classless.append([student, course_name])

        for student in Student.student_lst:
            print(student.schedule)

        # try to enroll students in other classes in the same period
        cases, resolved = len(classless), 0
        for elem in classless:
            empty_periods = elem[0].get_empty_periods()

            i, flag = 0, True
            while i < len(empty_periods) and flag:
                empty_period = empty_periods[i]
                for row in self.master:
                    if isinstance(row[empty_period - 1], Section):
                        try:
                            row[empty_period - 1].enroll_student(elem[0])
                            flag = False
                            resolved += 1
                            break
                        except AtCapacityException:
                            pass
                i += 1
        print("\nRESOLVED " + str(resolved) + " CASES\n\n")


    def __str__(self):
        string = ""
        for teacher in self.master:
            string += "["
            for period in teacher:
                string += str(period) + ", "
            string += "]\n"
        return string

def get_schedule(student_id):
    i = 0
    while i < len(Student.student_lst):
        student = Student.student_lst[i]
        if (student.id == student_id):
            return print(student.get_schedule())
        i += 1
    print("Student not found!")

# *******************************************************************************

master = Master(PERIODS_PER_DAY)

for teacher in Teacher.teacher_lst:
    master.add_prep(Teacher.teacher_lst.index(teacher), teacher.prep)

master.init_sections()

print(master)
for course_name in COURSE_NAMES: # print the courses
    print(courses[course_name])

master.fill_sections()
for row in range(len(master.master)):
    for col in range(len(master.master[0])):
        if isinstance(master.master[row][col], Section):
            print(master.master[row][col].str_detailed() + "\n")

for student in Student.student_lst: # print out the schedules!
    print(student.get_schedule())
