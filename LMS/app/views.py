import calendar
import io

from typing import Any#, List, Optional
from flask_appbuilder import ModelView 
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget, Select2AJAXWidget, Select2SlaveAJAXWidget
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import g, flash, abort, redirect, send_file, url_for, request # current user
from flask_appbuilder.actions import action

from . import appbuilder, db
from .models import Students, Teachers, Categories, Courses, Cycles, CoursesPerCycle, Enrollments, Classes, TeachersPerCourse
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .formVal import check_date_range, check_course_cycle_dates, check_unique_course_cycle, check_unique_compund_pk
from .api import TestModelApi, ExampleApi

db.create_all()


def all_fields(class_name):
    col_list = []
    for k, _ in class_name.__dict__.items():
        if not k.startswith('_'):
            col_list.append(k)
    return col_list

class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)
    

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
    # extra fieled validations
    validators_columns = {
        'cycle_end_date':[check_date_range('cycle_start_date', message=None)],
        'vacation_end_date':[check_date_range('vacation_start_date')],
        # 'vacation_end_date':[validate_by_endpoint('/example_api')],
    }

    col_list = all_fields(Cycles)
    add_columns = col_list.copy()
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()


class CoursesPerCycleModelView(ModelView):
    datamodel = SQLAInterface(CoursesPerCycle)

    #TODO: to be fixed once a reply is recieved for fixing AJAX error
    # add_form_extra_fields = {
    #     'cycles': AJAXSelectField('cycles',
    #     description='This will be populated with AJAX',
    #     datamodel=datamodel,
    #     col_name='cycle_id',
    #     widget=Select2AJAXWidget(endpoint='/coursespercyclemodelview/api/column/add/cycles')),

    #     'courses_in_cycle': AJAXSelectField('Courses of the Cycle',
    #     description='Extra Field description',
    #     datamodel=datamodel,
    #     col_name='course_id',
    #     widget=Select2SlaveAJAXWidget(master_id='cycles',
    #     endpoint='/coursespercyclemodelview/api/column/add/courses_per_cycle?_flt_0_cycle_id={{cycle_id}}'))
    #     }
    

    col_list = all_fields(CoursesPerCycle)
    # print (col_list)
    # hide mandatory/foreign keys not null field from entry and then feed it in from pre/...
    col_list = ['cycles','courses',  'course_start_date', 'course_end_date']
    # col_list = ['cycles','courses_in_cycle',  'course_start_date', 'course_end_date']
    # col_list = ['course_start_date', 'course_end_date']
    add_columns = col_list.copy()
    # add_columns = ['cycles','courses_in_cycle',  'course_start_date', 'course_end_date']
    list_columns = col_list.copy() 
    edit_columns = col_list.copy()
    show_columns = col_list.copy()

    # FE fieldd validation
    validators_columns = {
        # 'courses':[check_unique_course_cycle(datamodel),],  # temp until fixing AJAX Select2 fields
        'courses':[check_unique_compund_pk(datamodel, {'cycles':'cycle_id', 'courses':'course_id'}),],  # temp until fixing AJAX Select2 fields
        'course_end_date':[DataRequired(),                
            check_date_range('course_start_date', message=None), check_course_cycle_dates()],
        'vacation_end_date':[DataRequired(), check_date_range('vacation_start_date')],
    }
    
    
    def pre_add(self, rec: Any) -> None:
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id
        #TODODone: following validation should be done on FE using JS
        # if rec.course_start_date > rec.course_end_date:
        #     raise ValueError("Start-date cannot be after end-date ....")
        
        # TODO: this is backend validation but it flushes the entered data. should save data for retry
        # or send cycle start/end date as hidden data to be used in JS FE validation.
        if rec.course_start_date < rec.cycles.cycle_start_date or \
           rec.course_end_date > rec.cycles.cycle_end_date:
            raise ValueError("Course Start/End dates should be within Cycle's Start/Snd dates ....")
        
    def pre_edit(self, rec: Any) -> None:
        #TODODone: following validation should be done on FE using JS
        # if rec.course_start_date > rec.course_end_date:
        #     raise ValueError("Start-date cannot be after end-date ....")
        
        rec.course_id = rec.courses.course_id
        rec.cycle_id = rec.cycles.cycle_id


class EnrollmentsModelView(ModelView):
    datamodel = SQLAInterface(Enrollments)

    # col_list = all_fields(Enrollments)
    # print (col_list)
    # hide mandatory/foreign keys not null field from entry and then feed it in from pre/...
    add_columns = ['students',  'cycles', 'courses_per_cycle']
   
    list_columns = ['students', 'cycles', 'courses_per_cycle', 'enrollment_date', 'cancelled']
    edit_columns =  ['students', 'cycles','courses_per_cycle', 'enrollment_date','cancelled', 'cancellation_reason']
    #  add_exclude_columns=['id', 'status', 'add_dt', 'level', 'semester'] # auto-increment & default is active 
    # readonly fields gives error during edit : "'str' object has no attribute '_sa_instance_state'"

    # edit_form_extra_fields = {
        # 'students': StringField('students', widget=BS3TextFieldROWidget()),
    #     'cycles': StringField('cycles', widget=BS3TextFieldROWidget()),
    #     'courses_per_cycle': StringField('courses_per_cycle', widget=BS3TextFieldROWidget()),
    #     'enrollment_date': StringField('enrollment_date', widget=BS3TextFieldROWidget()),
    # }
    show_columns = edit_columns.copy()


    # def pre_add(self, rec: Any) -> None:
    #     rec.courses_per_cycle.course_id = rec.courses.course_id
    #     rec.cycle_id = rec.cycles.cycle_id
    #     rec.student_id = rec.students.student_id

    # def pre_edit(self, rec: Any) -> None:
    #     # rec.course_id = rec.courses.course_id
    #     rec.courses_per_cycle.course_id = rec.courses.course_id
    #     rec.cycle_id = rec.cycles.cycle_id
    #     rec.student_id = rec.students.student_id

    # TODO: disable primary key fiedlds during Edit
        

class ClassesModelView(ModelView):
    datamodel = SQLAInterface(Classes)

    # col_list = all_fields(Classes)
    # print (col_list)
    col_list = ['cycles', 'courses', 'class_no', 'class_title', 'teachers',  'start_date', 'end_date']
    # hide mandatory/foreign keys not null field from entry and then feed it in form pre/...
    add_columns = col_list.copy()
    list_columns = col_list.copy()
    edit_columns =  col_list.copy()
    show_columns = col_list.copy()

    validators_columns = {
        'end_date':[check_date_range('start_date')]
    }

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
    # FE field validation
    validators_columns = {
        'teachers':[check_unique_compund_pk(datamodel, {'cycles':'cycle_id', 'courses':'course_id', 'teachers':'teacher_id'}),], 
    }

    # print (col_list)
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
# appbuilder.add_api(ExampleApi)
# appbuilder.add_api(DBWithCompoundKey)
# appbuilder.add_api(TestModelApi)
