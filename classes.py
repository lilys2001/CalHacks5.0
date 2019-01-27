import csv

MAX_SECTION_ENROLLMENT = 0
PERIODS_PER_DAY = 0
COURSE_NAMES = []

class Course:

    def __init__(self, title):
        assert isinstance(title, str) , "title must be a string"
        self.title = title
        self.student_ids = []
        self.sections = []

    # adds a student to the course
    def add_student(self, student_id):
        self.student_ids.append(student_id)

    # makes a new section for this course
    def add_section(self, section):
        assert isinstance(section, Section) , "section must be a Section"
        self.sections.append(section)

    def enroll_student(self, student, section_number=0):
        while section_number < len(self.sections):
            if len(self.sections[section_number].students) < MAX_SECTION_ENROLLMENT and student.schedule[self.sections[section_number].period -1] == -1:
                # enroll!
                self.sections[section_number].enroll_student(student)
                student.schedule[self.sections[section_number].period - 1] = self.sections[section_number].course_title
                break
            else:
                section_number += 1

        if section_number >= len(self.sections):
            raise AtCapacityException

    def __str__(self):
        ln1 = "Course Title: " + self.title
        ln2 = "\tStudent List: " + str(self.student_ids)
        ln3 = "\tSections: " + str([str(section) for section in self.sections])
        return ln1 + "\n" + ln2 + "\n" + ln3 + "\n"


class Section:

    def __init__(self, number, period, course_title):
        self.number = number
        self.period = period
        self.course_title = course_title
        self.students = []

    # enroll students in this section
    def enroll_student(self, student):
        if (len(self.students) < MAX_SECTION_ENROLLMENT):
            self.students.append(student.id)
            student.schedule[self.period - 1] = self.course_title
        else:
            raise AtCapacityException

    # remove students in this section
    def remove_students(self, student_ids):
        assert isinstance(student_ids, list) , "student_ids must be a list of student ids"
        for student in student_ids:
            self.students.remove(student_ids)

    def __str__(self):
        return "Course: " + self.course_title + ". Section: " + str(self.number)

    def str_detailed(self):
        return self.__str__() + " " + "Period: " + str(self.period)  + " " + str(self.students)

class Teacher:
    teacher_lst = []
    num_teachers = -1 # to account for the column header row of data

    def __init__(self, teacher_data):
        self.teacher_data_lst = teacher_data.split(',')
        self.name = self.teacher_data_lst[1]
        Teacher.num_teachers += 1
        self.prep = self.teacher_data_lst[2]
        self.courses = [course.replace('\"', '') for course in self.teacher_data_lst[3:] if course != '']
        temp_courses = []
        for course in self.courses:
            if (course[0] == ' '):
                temp_courses.append(course[1:])
            else:
                temp_courses.append(course)
        self.courses = temp_courses
        Teacher.teacher_lst.append(self)

    # def __init__(self, name, courses, prep):
    #     self.name = name
    #     self.courses = courses
    #     self.prep = int(prep[1])
    #     Teacher.num_teachers += 1
    #     Teacher.teacher_lst.append(self)

    def __str__(self):
        ln1 = "Teacher, " + self.name + ": " + str(self.courses)
        ln2 = "\tPreferred prep period: " + str(self.prep)
        return ln1 + "\n" + ln2

class Student:
    student_lst = []
    num_students = -1 # to account for the column header row of data

# reads input csv file to create instance
    def __init__(self, student_data):
        self.student_data_lst = student_data.split(',')
        self.id = self.student_data_lst[1]
        Student.num_students += 1
        self.course_names = [course.replace("\r\n", "") for course in self.student_data_lst[2:]]
        self.schedule = [-1 for _ in range(len(self.course_names))]
        Student.student_lst.append(self)

    # def __init__(self, id, course_names):
    #     self.id = id
    #     self.course_names = course_names
    #     self.schedule = [-1 for _ in range(len(self.course_names))]
    #     Student.num_students += 1
    #     Student.student_lst.append(self)

    # adds the student to the student's desired course list
    def add_courses(self):
        for course_name in self.course_names:
            courses[course_name].add_student(self.id)

    def get_empty_periods(self):
        result = []
        for i in range(len(self.schedule)):
            if (self.schedule[i] == -1):
                result.append(i + 1)
        return result

    def get_schedule(self):
        string = "Student ID: " + str(self.id) + "\n"
        for i in range(len(self.schedule)):
            string += "Period " + str(i + 1) + ": "
            if self.schedule[i] != -1:
                string += self.schedule[i] + "\n"
            else:
                string += "No class\n"
        return string

    def __str__(self):
        ln1 = "Student ID: " + str(self.id)
        ln2 = "\tWants to take: " + str(self.course_names)
        return ln1 + "\n" + ln2


class AtCapacityException(Exception):
    pass


with open('Student_Course_Request_Form_(Responses)_-_Form_Responses_1.csv', newline = '') as csvfile:
    responses = csv.reader(csvfile, delimiter = ',')
    for row in csvfile:
        Student(row)

with open('Instructor_Class_Selection_Form_(Responses)_-_Form_Responses_1.csv') as csvfile:
    responses = csv.reader(csvfile, delimiter = ',')
    for row in csvfile:
        Teacher(row)

with open('Parsed_Counselor_Response_-_Sheet1.csv') as csvfile:
    responses = csv.reader(csvfile, delimiter = ',')
    print(responses)
    for row in csvfile:
        row_splice = row.split(',')
        if row_splice[0] == 'Maximum Section Enrollment':
            MAX_SECTION_ENROLLMENT = int(row_splice[1])
        elif row_splice[0] == 'Periods Per Day':
            PERIODS_PER_DAY = int(row_splice[1])
        else:
            COURSE_NAMES.append(row_splice[0])
    COURSE_NAMES.pop(0)
    C_N_copy = COURSE_NAMES[:]
    for i in range(len(C_N_copy)):
        if not C_N_copy[i]:
            COURSE_NAMES.remove('')
            COURSE_NAMES.remove(C_N_copy[i+1])

Student.student_lst.pop(0)
Teacher.teacher_lst.pop(0)
# ******************************* TEST DATA SET 1 **************************** #
# s1 = Student(1, ["C1", "C2", "C3"])
# s2 = Student(2, ["C1", "C2", "C4"])
# s3 = Student(3, ["C1", "C2", "C5"])
# s4 = Student(4, ["C2", "C3", "C4"])
# s5 = Student(5, ["C2", "C3", "C5"])
# s6 = Student(6, ["C1", "C3", "C4"])
# s7 = Student(7, ["C1", "C2", "C3"])
# s8 = Student(8, ["C2", "C3", "C5"])
# s9 = Student(9, ["C1", "C3", "C5"])
# s10 = Student(10, ["C2", "C4", "C5"])

# t1 = Teacher("W", ["C1"], "P2")
# t2 = Teacher("X", ["C2"], "P3")
# t3 = Teacher("Y", ["C3"], "P1")
# t4 = Teacher("Z", ["C4", "C5"], "P2")
# ************************************************************************** #

# ********************************* TEST DATA SET 2 ************************ #
# s1 = Student(1, ["Math 1", "Eng 1", "Hist 1", "Bio 1"])
# s2 = Student(2, ["Math 1", "Eng 1", "Hist 2", "Chem 1"])
# s3 = Student(3, ["Math 2", "Eng 1", "Hist 1", "Bio 1"])
# s4 = Student(4, ["Math 2", "Eng 2", "Hist 2", "Chem 1"])
# s5 = Student(5, ["Math 1", "Eng 2", "Hist 2", "Bio 1"])
# s6 = Student(6, ["Math 2", "Eng 2", "Hist 1", "Bio 1"])
# s7 = Student(7, ["Math 2", "Eng 2", "Hist 2", "Chem 1"])
# s8 = Student(8, ["Math 1", "Math 2", "Bio 1", "Chem 1"])
# s9 = Student(9, ["Eng 1", "Eng 2", "Bio 1", "Chem 1"])
# s10 = Student(10, ["Eng 1", "Eng 2", "Hist 1", "Hist 2"])
# s11 = Student(11, ["Hist 1", "Hist 2", "Eng 1", "Eng 2"])
# s12 = Student(12, ["Math 1", "Chem 1", "Eng 1", "Hist 2"])
# s13 = Student(13, ["Bio 1", "Chem 1", "Hist 1", "Hist 2"])
# s14 = Student(14, ["Eng 1", "Hist 2", "Eng 2", "Bio 1"])
# s15 = Student(15, ["Chem 1", "Math 2", "Math 1", "Eng 1"])
#
# t1 = Teacher("Ms. Homer", ["Eng 1", "Eng 2"], "P3")
# t2 = Teacher("Mr. Churchill", ["Hist 1", "Hist 2"], "P4")
# t3 = Teacher("Mr. Pi", ["Math 1", "Math 2"], "P1")
# t4 = Teacher("Ms. Einstein", ["Bio 1", "Chem 1"], "P2")
# ************************************************************************* #



[print(student) for student in Student.student_lst] # print the students
print("\n")
[print(teacher) for teacher in Teacher.teacher_lst] # print the teachers
print("\n")
print(COURSE_NAMES, MAX_SECTION_ENROLLMENT, PERIODS_PER_DAY)

# course_names = ["Math 1", "Math 2", "Hist 1", "Hist 2", "Eng 1", "Eng 2", "Bio 1", "Chem 1"] # get all the courses

courses = {}
for course_name in COURSE_NAMES: # builds a dictionary which links course name with corresponding Course instance
    courses[course_name] = Course(course_name)

for student in Student.student_lst[1:]: # add the students to the courses
    student.add_courses()

for course_name in COURSE_NAMES: # print the courses
    print(courses[course_name])

COURSE_NAMES.sort(key=lambda x: len(courses[x].student_ids)) # sorts based on num students interested in course
