import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime, CHAR, Numeric
from sqlalchemy.orm import relationship
from flask_appbuilder.security.sqla.models import User

mindate = datetime.date(datetime.MINYEAR, 1, 1)


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Status(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey("gender.id"), nullable=False)
    gender = relationship("Gender")

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)
    
class Student(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=False, nullable=True)
    name_en = Column(String(20), unique=False, nullable=False)
    passport_no = Column(String(20), nullable=False)
    birth_dt= Column(Date(), nullable = False)
    nationality_id = Column(CHAR(3), ForeignKey('country.alpha_3_code'), nullable=False) 
    nationality = relationship("Country")
    # gender = Column(CHAR(), nullable = False, default = 'M')
    gender_id = Column(Integer, ForeignKey("gender.id"), nullable=False)
    gender = relationship("Gender")
    phone_no = Column(String(11), nullable=False)
    whats_up = Column(String(11), nullable=True)
    address = Column(String(200), nullable=False)
    district = Column(String(20), nullable=True)
    street_name = Column(String(20), nullable=True)
    building_no = Column(String(20), nullable=True)
    ref_name = Column(String(20), nullable=True)
    ref_address = Column(String(20), nullable=True)
    how_did_know = Column(String(20), nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False, default=1) 
    status = relationship("Status")

    level_id = Column(Integer, ForeignKey('level.id'), nullable=True) 
    level = relationship("Level")
    semester_id = Column(Integer, ForeignKey('semester.id'), nullable=True) 
    semester = relationship("Semester")
    add_dt = Column(Date(), nullable = False, default = datetime.date.today())

    def __repr__(self):
        return f"{self.id:04d}-{self.name} Level:{self.level.level if self.level else 'Not registered'} Semester: {self.semester}"
    
class Country(Model):
    id = Column(Integer)
    country = Column(String(20))
    alpha_2_code = Column(String(2))
    alpha_3_code = Column(CHAR(3), primary_key=True)
    un_code = Column(Integer)
    country_ar = Column(String(20))
    # student_country = relationship('Student', backref='student_country', lazy=True)

    def __repr__(self):
        return f"{self.country}"
    

class Semester(Model):
    id	        = Column(Integer, unique = True, nullable=False, primary_key=True)
    semester_no	= Column(CHAR(5), unique = True, nullable=False)
    description	= Column(String(20), nullable=False)
    book_start_date	= Column(Date(), nullable=False)
    exam_start_date	= Column(Date(), nullable=True)
    exam_end_date	= Column(Date(), nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False, default=1) 
    status = relationship("Status")
    create_date = Column(Date(), nullable = False, default = datetime.date.today())

    def __repr__(self):
        return f"{self.id:02d}- {self.description}"

class Level(Model):
    id = Column(CHAR(2), primary_key=True, unique=True, nullable=False)
    level = Column(String(50),nullable=False)

    def __repr__(self):
        return self.level
    
class StudentLevel(Model):
    student_id	= Column(Integer, ForeignKey('student.id'), nullable=False, primary_key=True) 
    student_name = relationship("Student")

    level_id = Column(CHAR(2), ForeignKey('level.id'), nullable=False, primary_key=True)
    # level_id = Column(CHAR(2), ForeignKey('level.id'), nullable=False)
    level = relationship("Level")

    comment = Column(String(40))
    user_id	= Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    create_date = Column(Date(), nullable = False, default = datetime.date.today())

    def __repr__(self):
        return f"{self.student_id}-{self.student_name}- {self.level}"
    
#------------------------------------------------------
## 3 primary keys didnt work in edit/delete/show
# -----------------------------------------------------
class StudentSemester(Model):

    # id	= Column(Integer, nullable=False, primary_key=True, autoincrement = True) 
    student_id	= Column(Integer, ForeignKey('student.id'), nullable=False, primary_key=True) 
    student_data = relationship("Student")

    level_id = Column(CHAR(5), nullable=False, primary_key=True) 

    semester_id = Column(CHAR(5), ForeignKey('semester.id'), nullable=False, unique=True, primary_key=True) 
    semester = relationship("Semester")

    comment = Column(String(40))
    user_id	= Column(Integer, ForeignKey('ab_user.id'))
    create_date = Column(Date(), nullable = False, default = datetime.date.today())

    def __repr__(self):
        return f"{self.student_id}-{self.student_data}- Semester: {self.semester_no}"


class Teller(Model):
    trx_id	= Column(Integer, primary_key=True)
    user_id	= Column(Integer, ForeignKey('ab_user.id'))
    user_name = relationship("User", primaryjoin="Teller.user_id == User.id")
    trx_date	= Column(DateTime(), nullable=False, default=datetime.datetime.now())
    amount	= Column(Numeric, nullable=False)
    db_cr	= Column(CHAR(2)) #, default=TrxCode.get_trx_code_db_cr())
    trx_code	= Column(Integer, ForeignKey('trx_code.trx_code'), nullable=False) 
    trx_code_desc = relationship("TrxCode")
    description	= Column(String(40))
    reversed	= Column(CHAR(1), default=0)
    reverse_date	= Column(DateTime)
    student_id	= Column(Integer, ForeignKey('student.id'), nullable=False) 
    student_name = relationship("Student")

    level_id = Column(CHAR(2), ForeignKey('level.id'), nullable=False)
    level = relationship("Level")

    semester_no = Column(CHAR(5), ForeignKey('semester.id'), nullable=False) 
    semester = relationship("Semester")

    payee	= Column(String(20))

    def __repr__(self):
        return f"[Trx {self.trx_id}, {self.user_id}, {self.trx_date} {self.amount} {self.trx_code} {self.db_cr}]"
    

class TrxCode(Model):
    trx_code = Column(Integer, primary_key=True)
    description = Column(String(40))
    db_cr = Column(CHAR(2))

    def __repr__(self):
        return f"{self.db_cr}{self.trx_code}- {self.description}"