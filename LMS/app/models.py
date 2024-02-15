import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime, CHAR, Numeric, Time, Boolean
from sqlalchemy.orm import relationship
from flask_appbuilder.security.sqla.models import User

### LMS 
# https://www.vertabelo.com/blog/database-design-management-system/
    
class Courses(Model):
    course_id = Column(String(10),  nullable=False, primary_key= True)
    category_id = Column(String(10), ForeignKey('categories.category_id'), nullable=False,)
    categories = relationship('Categories')

    course_description = Column(String(100),  nullable=False)
    # start_date = Column(Date(),  nullable=False)
    # end_date = Column(Date(),  nullable=False)
    abstract = Column(String(1000),  nullable=False)
    bibliography = Column(String(1000),  nullable=False)
    def __repr__(self):
        return f"{self.course_id}-{self.course_description}"

class Categories(Model):
    category_id = Column(String(10), nullable=False, primary_key= True)
    category_description = Column(String(100), nullable = False)
    def __repr__(self):
        return f"{self.category_id}-{self.category_description}"
    
    
class Cycles(Model):
    cycle_id = Column(String(10), nullable=False, primary_key= True)
    cycle_description = Column(String(100),  nullable=False)
    cycle_start_date = Column(Date(),  nullable=False)
    cycle_end_date = Column(Date(),  nullable=False)
    vacation_start_date = Column(Date(),  nullable=True)
    vacation_end_date = Column(Date(),  nullable=True)
    def __repr__(self):
        return f"{self.cycle_id}-{self.cycle_description}, start: {self.cycle_start_date}, end: {self.cycle_end_date}"

        
class CoursesPerCycle(Model):
    cycle_id = Column(String(10), ForeignKey('cycles.cycle_id'), nullable=False, primary_key= True)
    cycles = relationship('Cycles')
    course_cycle_id = Column(String(10), ForeignKey('courses.course_id'), nullable=False, primary_key= True)
    courses = relationship('Courses')

    course_start_date = Column(Date(),  nullable=False)
    course_end_date = Column(Date(),  nullable=False)

    def __repr__(self):
        return f"{self.course_cycle_id}-{self.courses.course_description}, {self.cycle_id}:{self.cycles.cycle_description}"


class Students(Model):
    student_id = Column(String(10), nullable=False, primary_key= True)
    student_name = Column(String(100),  nullable=False)
    email = Column(String(100),  nullable=False, unique = True)
    birth_date = Column(Date(),  nullable=False)
    phone = Column(String(11),  nullable=False)
    def __repr__(self):
        return self.student_name
    

class Enrollments(Model):
    student_id = Column(String(10), ForeignKey('students.student_id'), nullable=False, primary_key= True)
    students = relationship('Students')

    cycle_id = Column(String(10), ForeignKey('cycles.cycle_id'), nullable=False, primary_key= True)
    cycles= relationship('Cycles')

    enrollment_course_id = Column(String(10), ForeignKey('courses_per_cycle.course_cycle_id'), nullable=False, primary_key= True)
    courses_per_cycle = relationship('CoursesPerCycle', 
                                     primaryjoin="and_(Enrollments.cycle_id==CoursesPerCycle.cycle_id, Enrollments.enrollment_course_id==CoursesPerCycle.course_cycle_id)")
    
    enrollment_date = Column(Date(),  nullable=False, default= datetime.date.today())
    cancelled = Column(Boolean(),  nullable=False, default=False)
    cancellation_reason = Column(String(100),  nullable=True)

    def __repr__(self):
        return self.course_id+ ','+ self.cycle_id + ', Student'+ self.students.student_name

class Teachers(Model):
    teacher_id = Column(String(10), nullable=False, primary_key= True)
    teacher_name = Column(String(100),  nullable=False)
    email = Column(String(100),  nullable=False, unique = True)
    phone = Column(String(11),  nullable=False)
    def __repr__(self):
        return self.teacher_id+','+self.teacher_name


class TeachersPerCourse(Model):
    cycle_id = Column(String(10), ForeignKey('cycles.cycle_id'), nullable=False, primary_key= True)
    cycles= relationship('Cycles')
    course_id = Column(String(10), ForeignKey('courses.course_id'), nullable=False, primary_key= True)
    courses = relationship('Courses')
    teacher_id = Column(String(10), ForeignKey('teachers.teacher_id'),  nullable=False, primary_key= True)
    teachers = relationship('Teachers')
    
    def __repr__(self):
        return self.teacher_id+','+self.teacher_name
    

class Classes(Model):
    cycle_id = Column(String(10), ForeignKey('cycles.cycle_id'), nullable=False, primary_key= True)
    cycles= relationship('Cycles')
    course_id = Column(String(10), ForeignKey('courses.course_id'), nullable=False, primary_key= True)
    courses = relationship('Courses')
    class_no = Column(Integer(), nullable=False, primary_key= True)
    class_title = Column(String(100),  nullable=False)
    
    teacher_id = Column(String(10), ForeignKey('teachers.teacher_id'),  nullable=False)
    teachers = relationship('Teachers')
   
    start_date = Column(Date(),  nullable=False)
    end_date = Column(Date(),  nullable=False)
    def __repr__(self):
        return self.course_id+','+self.cycle_id+',class'+self.class_no +', teacher:', {self.teachers.teacher_id}
    

# class Attendances(Model):
#     cycle_id = Column(String(10), ForeignKey('cycles.cycle_id'), nullable=False, primary_key= True)
#     cycles= relationship('Cycles')
#     course_id = Column(String(10), ForeignKey('courses.course_id'), nullable=False, primary_key= True)
#     courses = relationship('Courses')
#     class_no = Column(Integer(), ForeignKey('classes.class_no'), nullable=False, primary_key= True)
#     courses = relationship('Classes.query.filter(Classess.cycle_id.has == self.cycle_id)')

#     student_id = Column(String(10), ForeignKey('students.student_id'), nullable=False, primary_key= True) ##
#     students = relationship('Students')
    
#     time_arrive = Column(Time(), nullable = True)
#     time_leave = Column(Time(), nullable = True)
#     def __repr__(self):
#         return f"Student:{self.student_id}-{self.students.student_name}, course:{self.course_id}, cycle:{self.cycle_id}, class:{self.class_no}"