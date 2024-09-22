# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:53:10 2024

@author: Taline Slim
"""

import json
import re

# STEP 1 : DEFINING THE CLASSES

class Person:
    def __init__(self, name, age, email):
        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        if not self.validate_age(age):
            raise ValueError("Age must be a non-negative integer")

        self.name = name
        self.age = age
        self.__email = email  # private attribute with double underscores
    
    def get_email(self):
        return self.__email
        
    def introduce(self):
        print(f"Hi, my name is {self.name} and I am {self.age} years old.")

    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_age(age):
        return isinstance(age, int) and age >= 0

    # serilization
    def save_to_file(self, filename):
        data = {
            'name': self.name,
            'age': self.age,
            'email': self.__email
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"Data saved to {filename}")

    #load data (read from JSON file)
    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return cls(data['name'], data['age'], data['email'])

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email) # calling the parent class person
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        self.registered_courses.append(course)

    def save_to_file(self, filename):
        data = {
            'name': self.name,
            'age': self.age,
            'email': self._Person__email,  
            'student_id': self.student_id,
            'registered_courses': [course.course_name for course in self.registered_courses]
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"Student data saved to {filename}")

    @classmethod #saving the student data
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            student = cls(data['name'], data['age'], data['email'], data['student_id'])
            return student

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        self.assigned_courses.append(course)
        course.instructor = self 
        print(f"{self.name} has been assigned to the course: {course.course_name}")

    # save instructor data 
    def save_to_file(self, filename):
        data = {
            'name': self.name,
            'age': self.age,
            'email': self._Person__email,
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_name for course in self.assigned_courses]
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"Instructor data saved to {filename}")

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            instructor = cls(data['name'], data['age'], data['email'], data['instructor_id'])
            return instructor
class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name
        self.students = []
        self.assigned_instructor = None

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        self.students = [s for s in self.students if s.name != student.name]

    def assign_instructor(self, instructor):
        self.assigned_instructor = instructor

    def update_student_name(self, old_name, new_name):
        for student in self.students:
            if student.name == old_name:
                student.name = new_name

    def update_instructor_name(self, old_name, new_name):
        if self.assigned_instructor and self.assigned_instructor.name == old_name:
            self.assigned_instructor.name = new_name

    def save_to_file(self, filename):
        data = {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.assigned_instructor.name if self.assigned_instructor else None,
            'students': [student.name for student in self.students]  
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"Course data saved to {filename}")


    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            course = cls(data['course_id'], data['course_name'])
            return course


# Step 2: Implement Data Management

student_taline = Student("Taline", 21, "tws04@aub.edu.com", "202204417")
student_lea = Student("Lea", 22, "lea@aub.edu.com", "202204418")
student_tina = Student("Tina", 21, "tina@aub.edu.com", "202204419")
student_julia = Student("Julia", 23, "julia@aub.edu.com", "202204420")
student_jenny = Student("Jenny", 20, "jenny@aub.edu.com", "202204421")

instructor_imane = Instructor("Dr. Imane", 30, "imane@aub.edu.com", "202212123")
instructor_hassan = Instructor("Dr. Hassan", 35, "hassan@aub.edu.com", "202212124")
instructor_rouba = Instructor("Dr. Rouba", 40, "rouba@aub.edu.com", "202212125")

course_eece340 = Course("EECE340", "Digital Signal Processing")
course_eece435l = Course("EECE435L", "Embedded Systems Lab")
course_eece432 = Course("EECE432", "Advanced Computer Architecture")
course_eece455 = Course("EECE455", "Artificial Intelligence")

course_eece340.add_student(student_taline)
course_eece340.add_student(student_lea)
course_eece435l.add_student(student_tina)
course_eece432.add_student(student_julia)
course_eece455.add_student(student_jenny)

instructor_imane.assign_course(course_eece340)
instructor_hassan.assign_course(course_eece435l)
instructor_rouba.assign_course(course_eece432)
instructor_imane.assign_course(course_eece455)

student_taline.save_to_file("student_taline_data.json")
student_lea.save_to_file("student_lea_data.json")
student_tina.save_to_file("student_tina_data.json")
student_julia.save_to_file("student_julia_data.json")
student_jenny.save_to_file("student_jenny_data.json")

instructor_imane.save_to_file("instructor_imane_data.json")
instructor_hassan.save_to_file("instructor_hassan_data.json")
instructor_rouba.save_to_file("instructor_rouba_data.json")

course_eece340.save_to_file("course_eece340_data.json")
course_eece435l.save_to_file("course_eece435l_data.json")
course_eece432.save_to_file("course_eece432_data.json")
course_eece455.save_to_file("course_eece455_data.json")

loaded_student_taline = Student.load_from_file("student_taline_data.json")
loaded_student_lea = Student.load_from_file("student_lea_data.json")
loaded_student_tina = Student.load_from_file("student_tina_data.json")
loaded_student_julia = Student.load_from_file("student_julia_data.json")
loaded_student_jenny = Student.load_from_file("student_jenny_data.json")

loaded_instructor_imane = Instructor.load_from_file("instructor_imane_data.json")
loaded_instructor_hassan = Instructor.load_from_file("instructor_hassan_data.json")
loaded_instructor_rouba = Instructor.load_from_file("instructor_rouba_data.json")

loaded_course_eece340 = Course.load_from_file("course_eece340_data.json")
loaded_course_eece435l = Course.load_from_file("course_eece435l_data.json")
loaded_course_eece432 = Course.load_from_file("course_eece432_data.json")
loaded_course_eece455 = Course.load_from_file("course_eece455_data.json")

loaded_student_taline.introduce()
loaded_instructor_imane.introduce()
