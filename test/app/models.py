import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime, CHAR
from sqlalchemy.orm import relationship

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
    phone_no = Column(String(20), nullable=False)
    whats_up = Column(String(20), nullable=True)
    address = Column(String(200), nullable=False)
    district = Column(String(20), nullable=True)
    street_name = Column(String(20), nullable=True)
    building_no = Column(String(20), nullable=True)
    ref_name = Column(String(20), nullable=True)
    ref_address = Column(String(20), nullable=True)
    how_did_know = Column(String(20), nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False, default=1) 
    status = relationship("Status")
    # status = Column(String(20), default='Active')

    add_dt = Column(DateTime(), nullable = False, default = datetime.datetime.utcnow())

    def __repr__(self):
        return self.name
    
class Country(Model):
    id = Column(Integer)
    country = Column(String(20))
    alpha_2_code = Column(String(2))
    alpha_3_code = Column(CHAR(3), primary_key=True)
    numeric = Column(Integer)
    country_ar = Column(String(20))
    # student_country = relationship('Student', backref='student_country', lazy=True)

    def __repr__(self):
        return f"{self.country}"