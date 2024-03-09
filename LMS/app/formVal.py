# https://wtforms.readthedocs.io/en/3.0.x/validators/

from wtforms.validators import ValidationError
# from flask import request, session
# from flask_appbuilder.models.sqla.interface import SQLAInterface


class CheckDateRange(object):
    def __init__(self, start_date_field_name, message=None):
        if not message:
            self.message = f"Incorrect From/date range"
        else:
            self.message = message
        self.start_date_field_name = start_date_field_name

    def __call__(self, form, field):
        start_date = form[self.start_date_field_name].data
        end_date = field.data
        if start_date and end_date:
            if  start_date > end_date:
                raise ValidationError(self.message)
check_date_range = CheckDateRange


class CheckCourseCycleDates(object):
    def __init__(self,  message=None):
        pass

    def __call__(self, form, field):
        cycles = form['cycles'].data
        if form['course_start_date'].data < cycles.cycle_start_date or \
           form['course_end_date'].data > cycles.cycle_end_date:
            raise ValidationError(f"Course Start/End dates should be within Cycle's Start/End dates:{cycles.cycle_start_date} - {cycles.cycle_end_date}")
        
check_course_cycle_dates = CheckCourseCycleDates


class CheckUniqueCourseCycle(object):  # multi-field key
    def __init__(self,  datamodel, message=None):
        self.datamodel = datamodel
       
    def __call__(self, form, field):
        if '_id' in form.__dict__.keys(): # Edit Mode, don't check. _id = ['1', "MATH101"]
            return
        
        # Add Mode
        result = self.datamodel.get(id=(form['cycles'].data.cycle_id, form['courses'].data.course_id), filters=None)
        if result:
            raise ValidationError(f"Course already exist in cycle {form['cycles'].data.cycle_id}")
        
check_unique_course_cycle = CheckUniqueCourseCycle


#TODO: to be completed
# class ValidateByEndPoint(object):
#     def __init__(self, endpoint, message=None):
#         if not message:
#             self.message = f"EndPoint Validation Error"
#         else:
#             self.message = message
#         self.endpoint = endpoint

#     def __call__(self, form, field):

 
#         with client():
#             client.get(self.end_point)
#             assert request.path == self.endpoint
#             assert session is not None # You can also access the session context local from here
#             # assert current_stateless_user is not None

#             raise ValidationError(self.message)

# validate_by_endpoint = ValidateByEndPoint

