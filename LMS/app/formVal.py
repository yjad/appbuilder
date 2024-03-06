# https://wtforms.readthedocs.io/en/3.0.x/validators/

from wtforms.validators import ValidationError
from flask import request, session

# from flask_stateless_auth import current_stateless_user



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


class ValidateByEndPoint(object):
    def __init__(self, endpoint, message=None):
        if not message:
            self.message = f"EndPoint Validation Error"
        else:
            self.message = message
        self.endpoint = endpoint

    def __call__(self, form, field):

 
        with test_client() as client:
            client.get(self.end_point)
            assert request.path == self.endpoint
            assert session is not None # You can also access the session context local from here
            # assert current_stateless_user is not None

            raise ValidationError(self.message)

validate_by_endpoint = ValidateByEndPoint

# def check_from_to_range(start_date_field_name, message):
#     if not message:
#         message = f"Incorrect From/date range"
        
#     def _check_from_to_dates(form, field):
#         start_date = form[start_date_field_name].data
#         end_date = field.data
#         # print ("***Form: ", form, "\n***Field: ",end_date, "\start_date:", start_date)
#         if start_date > end_date:
#             raise ValidationError(message)

#     return _check_from_to_dates

