import calendar

from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Contact, ContactGroup, Gender, Student, Status


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
class StudentModelView(ModelView):
    datamodel = SQLAInterface(Student)

    list_columns = ['name_en','passport_no','birth_dt','nationality','gender.name','phone_no','status.name']
    base_order = ("name_en", "asc")

    show_fieldsets = [
        ("Summary", {"fields": ['name_en','passport_no','birth_dt','nationality','gender','phone_no']}),
        (
            "Communication data",
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
                    'how_did_know'
                ],
                "expanded": True,
            },
        ),
    ]

    add_fieldsets = show_fieldsets
  

    edit_fieldsets = show_fieldsets


# ---------------
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
appbuilder.add_view(StudentModelView, "List Students", icon="fa-graduation-cap", category="Students", category_icon="fa-school")
# appbuilder.add_view(StudentModelView, "List Stuedents", icon="fa-envelope", category="Students")