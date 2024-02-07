import calendar
import io

from typing import Any#, List, Optional
from flask_appbuilder import ModelView
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import g, flash, abort, redirect, send_file, url_for, request # current user
from flask_appbuilder.actions import action

from . import appbuilder, db
from .models import Students, Teachers, Categories, Courses, Cycles, CoursesPerCycle, Enrollments, Classes, TeachersPerCourse
from wtforms.fields import StringField


db.create_all()


def all_fields(class_name):
    col_list = []
    for k, v in class_name.__dict__.items():
        if not k.startswith('_'):
            col_list.append(k)
    return col_list

class StudentsModelView(ModelView):
    datamodel = SQLAInterface(Students)
    col_list = all_fields(Students)
    # add_columns = ['student_id', 'student_name', 'email', 'birth_date', 'phone', ]
    
    add_columns = col_list.copy()
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()


class TeachersModelView(ModelView):
    datamodel = SQLAInterface(Teachers)
    col_list = all_fields(Teachers)

    add_columns = col_list.copy()
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()


class CategoriesModelView(ModelView):
    datamodel = SQLAInterface(Categories)

    col_list = all_fields(Categories)

    add_columns = col_list.copy()
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()
    

class CoursesModelView(ModelView):
    datamodel = SQLAInterface(Courses)
    # hide category_id not null field from entry and then feed it in from pre/...
    col_list = ['course_id', 'categories', 'course_description', 'abstract', 'bibliography']
    # print (col_list)
    add_columns = col_list.copy()
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()

    def pre_add(self, rec: Any) -> None:
        rec.category_id = rec.categories.category_id

    def pre_edit(self, rec: Any) -> None:
        rec.category_id = rec.categories.category_id

class CyclesModelView(ModelView):
    datamodel = SQLAInterface(Cycles)

    col_list = all_fields(Cycles)
    add_columns = col_list.copy()
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()


class CoursesPerCycleModelView(ModelView):
    datamodel = SQLAInterface(CoursesPerCycle)

    col_list = all_fields(CoursesPerCycle)
    print (col_list)
    # hide mandatory/foreign keys not null field from entry and then feed it in from pre/...
    col_list = ['cycles','courses',  'course_start_date', 'course_end_date']
    add_columns = col_list.copy()
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()

    def pre_add(self, rec: Any) -> None:
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id

    def pre_edit(self, rec: Any) -> None:
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id


class EnrollmentsModelView(ModelView):
    datamodel = SQLAInterface(Enrollments)

    # col_list = all_fields(Enrollments)
    # print (col_list)
    # hide mandatory/foreign keys not null field from entry and then feed it in from pre/...
    add_columns = ['students', 'cycles', 'courses']
    list_columns = ['students', 'cycles', 'courses', 'cancelled']
    edit_columns =  ['students', 'cycles', 'courses', 'cancelled', 'cancellation_reason']
    show_columns = edit_columns.copy()

    def pre_add(self, rec: Any) -> None:
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id
        rec.student_id = rec.students.student_id

    def pre_edit(self, rec: Any) -> None:
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id
        rec.student_id = rec.students.student_id

    # TODO: disable primary key fiedlds during Edit
        

class ClassesModelView(ModelView):
    datamodel = SQLAInterface(Classes)

    # col_list = all_fields(Classes)
    # print (col_list)
    col_list = ['cycles', 'courses', 'class_no', 'class_title', 'teachers',  'start_date', 'end_date']
    # hide mandatory/foreign keys not null field from entry and then feed it in from pre/...
    add_columns = col_list.copy()
    list_columns = col_list.copy()
    edit_columns =  col_list.copy()
    show_columns = col_list.copy()

    def pre_add(self, rec: Any) -> None:
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id
        rec.teacher_id = rec.teachers.teacher_id

    def pre_edit(self, rec: Any) -> None:
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id
        rec.teacher_id = rec.teachers.teacher_id

    # TODO: disable primary key fiedlds during Edit
        

class TeachersPerCourseModelView(ModelView):
    datamodel = SQLAInterface(TeachersPerCourse)

    col_list = all_fields(TeachersPerCourse)
    print (col_list)
    # col_list = ['cycles', 'courses', 'class_no', 'class_title', 'teachers',  'start_date', 'end_date']
    # # hide mandatory/foreign keys not null field from entry and then feed it in from pre/...
    # add_columns = col_list.copy()
    # list_columns = col_list.copy()
    # edit_columns =  col_list.copy()
    # show_columns = col_list.copy()

    # def pre_add(self, rec: Any) -> None:
    #     rec.course_id = rec.courses.course_id
    #     rec.cycle_id = rec.cycles.cycle_id
    #     rec.teacher_id = rec.teachers.teacher_id

    # def pre_edit(self, rec: Any) -> None:
    #     rec.course_id = rec.courses.course_id
    #     rec.cycle_id = rec.cycles.cycle_id
    #     rec.teacher_id = rec.teachers.teacher_id

    # # TODO: disable primary key fiedlds during Edit
        

        
appbuilder.add_view(StudentsModelView, "Students", icon="fa-folder-open-o", category="LMS", category_icon="fa-envelope")
appbuilder.add_view(EnrollmentsModelView, "Enrollments", icon="fa-envelope", category="LMS")
appbuilder.add_separator("LMS")
appbuilder.add_view(TeachersModelView, "Teachers", icon="fa-envelope", category="LMS")
appbuilder.add_view(CategoriesModelView, "Course Categories", icon="fa-envelope", category="LMS")
appbuilder.add_view(CyclesModelView, "Cycles", icon="fa-envelope", category="LMS")
appbuilder.add_view(CoursesModelView, "Courses", icon="fa-envelope", category="LMS")
appbuilder.add_view(CoursesPerCycleModelView, "Courses per Cycle", icon="fa-envelope", category="LMS")
appbuilder.add_view(ClassesModelView, "Classes", icon="fa-envelope", category="LMS")
appbuilder.add_view(TeachersPerCourseModelView, "Teachers Per Course", icon="fa-envelope", category="LMS")

