import calendar
from typing import Any#, List, Optional
from flask_appbuilder import ModelView
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
<<<<<<< HEAD
from flask import g, flash, abort, redirect, send_file # current user
=======
from flask import g, flash, abort, redirect # current user
>>>>>>> 1dbcd4ce0a22d059543cb5d0db7c7b25c5c72957
from flask_appbuilder.actions import action

from . import appbuilder, db
from .models import Contact, ContactGroup, Gender, Student, Status, Semester, Level, Teller
from wtforms.fields import StringField


def voucher_print(rec):
     
    if rec.db_cr == 'Cr':
        print ('credit Voucher:', vars(rec))

        # print ('trx code:', rec.trx_code_desc.trx_code)
        # print ('trx amount:', rec.amount)
<<<<<<< HEAD
    file_name  = r"C:\Users\yahia\Downloads\TAX ID.pdf"
    return file_name
=======

>>>>>>> 1dbcd4ce0a22d059543cb5d0db7c7b25c5c72957
        

def fill_gender():
    try:
        db.session.add(Gender(name="Male"))
        db.session.add(Gender(name="Female"))
        db.session.commit()
    except Exception:
        db.session.rollback()

def fill_status():
    try:
        db.session.add(Status(name="Active"))
        db.session.add(Status(name="Inactive"))
        db.session.commit()
    except Exception:
        db.session.rollback()

def format_datetime(x):
    if x:
        return x.strftime("%Y-%m-%d %H:%M:%S") 
    else: 
        return None

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ["name", "personal_celphone", "birthday", "contact_group.name"]

    base_order = ("name", "asc")
    show_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)


def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = "Grouped Birth contacts"
    chart_type = "AreaChart"
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            "group": "month_year",
            "formatter": pretty_month_year,
            "series": [(aggregate_count, "group")],
        },
        {
            "group": "year",
            "formatter": pretty_year,
            "series": [(aggregate_count, "group")],
        },
    ]

# --------------
# Sutdents
# ------------------
    

class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)


    
class StudentModelView(ModelView):
    datamodel = SQLAInterface(Student)

    list_columns = ['id','name_en','passport_no','birth_dt','nationality','gender.name','phone_no','status.name']
    base_order = ("name_en", "asc")

    show_fieldsets = [
        ("Summary", {"fields": ['id','name_en','passport_no','birth_dt','nationality','gender','phone_no']}),
        (
            "Student data",
            {
                "fields": [
                    'name',
                    'whats_up',
                    'address',
                    'district',
                    'street_name',
                    'building_no',
                    'ref_name',
                    'ref_address',
                    'how_did_know',
                    'status',
                    'add_dt'
                ],
                "expanded": True,
            },
        ),
    ]

    # add_fieldsets = show_fieldsets
    add_exclude_columns=['id', 'status', 'add_dt'] # auto-increment & default is active 
    
    edit_form_extra_fields = {
        'id': StringField('id', widget=BS3TextFieldROWidget())
    }
    edit_fieldsets = [
        ("Summary", {"fields": ['id','name_en','passport_no','birth_dt','nationality','gender','phone_no']}),
        (
            "Student data",
            {
                "fields": [
                    'name',
                    'whats_up',
                    'address',
                    'district',
                    'street_name',
                    'building_no',
                    'ref_name',
                    'ref_address',
                    'how_did_know',
                    'status',
                    'add_dt'
                ],
                "expanded": True,
            },
        ),
    ]


class SemesterModelView(ModelView):
    datamodel = SQLAInterface(Semester)
    list_columns = ['semester_no','description','book_start_date','exam_start_date','exam_end_date','create_date','status.name']
    base_order = ("semester_no", "asc")
    add_exclude_columns=['status', 'create_date'] # auto-increment & default is active 
    show_fieldsets = [
        ("Semesters", {"fields": 
            ['semester_no','description','book_start_date','exam_start_date','exam_end_date','create_date','status']
            })]

    edit_fieldsets = [
        ("Semesters", {"fields": 
            ['semester_no','description','book_start_date','exam_start_date','exam_end_date','create_date','status']
            })]
    edit_exclude_columns=['semester_no', 'create_date'] # auto-increment & default is active 
    edit_form_extra_fields = {
    'semester_no': StringField('semester_no', widget=BS3TextFieldROWidget())
    }

    def pre_add(self, rec: Any) -> None:
    #     # raise ValueError("from pre_add")
        print ("========= from pre_add ==============",vars(rec))
    
    def post_add(self, rec: Any) -> None:
        print ("========= from post_add ==============", vars(rec))
        raise ValueError("from post_add")   # does not apply here
    
    def pre_update(self, rec: Any) -> None:
        print ("+++++++++++ from pre_update ++++++++++++")
        # raise ValueError("from pre_update")
    

# ---------------
class TellerModelView(ModelView):
    datamodel = SQLAInterface(Teller)
    list_columns = ['trx_date', 'amount', 'trx_code_desc', 'student_name', 'reversed', ]# 'user.user_name'
    add_exclude_columns=['reversed','reverse_date', 'trx_date', 'user_name', 'db_cr'] # auto-increment & default is active 
    # search_columns = ['name','address']
    # extra filed validation
    # validators_columns = {
    #     'my_field1':[EqualTo('my_field2', message=gettext('fields must match'))]
    # }
    formatters_columns = {
            "amount": lambda x: f"{x:.02f}",
            'trx_date': lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
            # 'reverse_date': lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if x else None # didnt work
            'reverse_date': format_datetime,
            'reversed': lambda x: not bool(x)
        }
    base_permissions = ['can_add','can_show','can_list','can_delete']   # remove edit button for trx.

    def pre_add(self, rec: Any) -> None:
        rec.user_id = g.user.id         # g is the current user record
        rec.db_cr = rec.trx_code_desc.db_cr
        # print ('===========> from pre_add', rec.trx_code, rec.trx_code_desc,'\n', vars(rec))

        if rec.trx_code_desc.trx_code == 100:
            if rec.semester is None or rec.level is None:
                raise ValueError("Semister and Level are mandatory for trx 100")
            

    def post_add(self, rec: Any):
        print ("=========Printing ==== from post_add", '\n', vars(rec))
        voucher_print(rec)
        file_name = r"C:\Users\yahia\Downloads\TAX ID.pdf"
        return send_file(file_name)
           
<<<<<<< HEAD
    @action("print_voucher", "rePrint", "Reprint?", "fa-print")
=======
    @action("print_voucher", "Print", "Reprint?", "fa-printer")
>>>>>>> 1dbcd4ce0a22d059543cb5d0db7c7b25c5c72957
    def print_voucher(self, items):
        if isinstance(items, list): # called from list
            # self.datamodel.delete_all(items)
            # self.update_redirect()
            pass    # do nothing 
        else:
            voucher_print(items)
<<<<<<< HEAD
        file_name = r"C:\Users\yahia\Downloads\TAX ID.pdf"
        return send_file(file_name)
        # return redirect(self.get_redirect())
=======
        return redirect(self.get_redirect())
>>>>>>> 1dbcd4ce0a22d059543cb5d0db7c7b25c5c72957

class RegFeesTellerModelView(TellerModelView):
    datamodel = SQLAInterface(Teller)

    add_exclude_columns=['reversed','reverse_date', 'trx_date', 'user_name', 'db_cr', 'payee', 'trx_code_desc'] # auto-increment & default is active 
    # add_form_extra_fields = {
    #     'trx_id': StringField('trx_id', widget=BS3TextFieldROWidget())
    # }
    # add_fieldsets = [
    #     ("", {"fields": ['trx_id','student_name','level','semester','amount','description']}),
    # ]

    base_permissions = ['can_add','can_list']   # remove edit button for trx.
    add_title = 'Collect Registeration Fees'
    # list_title = 'Collect Registeration Fees'
    # show_title = 'Collect Registeration Fees'
    def pre_add(self, rec: Any) -> None:
        print (vars(rec))
        rec.user_id = g.user.id         # g is the current user record
        rec.db_cr = 'Cr'
        rec.trx_code = 100
        # print (vars(rec))
            
    """
    base_order = ("semester_no", "asc")
    show_fieldsets = [
        ("Semesters", {"fields": 
            ['semester_no','description','book_start_date','exam_start_date','exam_end_date','create_date','status']
            })]

    edit_fieldsets = [
        ("Semesters", {"fields": 
            ['semester_no','description','book_start_date','exam_start_date','exam_end_date','create_date','status']
            })]
    edit_exclude_columns=['semester_no', 'create_date'] # auto-increment & default is active 
    edit_form_extra_fields = {
    'semester_no': StringField('semester_no', widget=BS3TextFieldROWidget())
    }
    """

class CrTellerModelView(TellerModelView):
    datamodel = SQLAInterface(Teller)

    add_exclude_columns=['reversed','reverse_date', 'trx_date', 'user_name', 'db_cr', 'payee', 'level', 'semester'] # auto-increment & default is active 
    # add_form_extra_fields = {
    #     'trx_id': StringField('trx_id', widget=BS3TextFieldROWidget())
    # }
    # add_fieldsets = [
    #     ("", {"fields": ['trx_id','student_name','level','semester','amount','description']}),
    # ]

    add_title = 'Collect payment'
    # list_title = 'Collect Registeration Fees'
    # show_title = 'Collect Registeration Fees'
    # def pre_add(self, rec: Any) -> None:
    #     print (vars(rec))
    #     rec.user_id = g.user.id         # g is the current user record
    #     rec.db_cr = 'Cr'
        

# ----------------------------    
db.create_all()
fill_gender()
fill_status()

appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Contacts", category_icon="fa-envelope")
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_separator("Contacts")
appbuilder.add_view(
    ContactTimeChartView,
    "Contacts Birth Chart",
    icon="fa-dashboard",
    category="Contacts",
)

#--------------------------------
# TODO: change layout of fields to be on 2 columns rather than as it is now. Needed for long pages like Student.
appbuilder.add_view(StudentModelView, "Students", icon="fa-graduation-cap", category="Students", category_icon="fa-school")
appbuilder.add_view(SemesterModelView, "Semisters",  category="Students")

#---------------------

appbuilder.add_view(TellerModelView, "Credit Trx", icon="fa-sack-dollar", category="Teller", category_icon="fa-sack-dollar")
appbuilder.add_view(RegFeesTellerModelView, "Collect Reg fees",  category="Teller", icon="fa-address-card",)
appbuilder.add_view(CrTellerModelView, "Collect payment",  category="Teller", icon= 'fa-file-invoice')
