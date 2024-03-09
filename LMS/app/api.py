from flask import session
from flask_appbuilder.api import BaseApi, expose, ModelRestApi    
from . import db
from . import test_client
import json
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import CoursesPerCycle, Cycles
from . import appbuilder
from flask_appbuilder.models.filters import BaseFilter

def all_fields(class_name):
    col_list = []
    for k, _ in class_name.__dict__.items():
        if not k.startswith('_'):
            col_list.append(k)
    return col_list

class PostmanBaseApi(BaseApi):
    allow_browser_login = True
    can_show=True


class ExampleApi(PostmanBaseApi):
# class ExampleApi(BaseApi):
    @expose('/greeting/<pk>')
    def greeting(self, pk):
        # self.datamodel = SQLAInterface(CoursesPerCycle)
        # datamodel = SQLAInterface(Cycles, db.session)
        # print (all_fields(datamodel))
        # pk = self._deserialize_pk_if_composite(datamodel,pk)
        print (pk)
        # self.endpoint = f'/coursespercyclemodelview/api/get/{pk}'
        self.endpoint = '/coursesmodelview/api/get/%5B"1",%20"MATH103"%5D'
        # self.endpoint = 'http://127.0.0.1:5000/api/v1/test/%5B"1",%20"MATH103"%5D'
        
        with test_client as client:
            x = client.get(self.endpoint)
            # print (x, f"status_code: {x.status_code}", "request:", x.json)
            # print (x, f"status_code: {x.status_code},", x.json)

            # message = f"status_code:{x.status_code}, data: {x.json}"
            # message = f"status_code:{x.status_code}"
            # message = f"code:{x.status_code}, x: {x.json}"
            print (x.status_code, x.json)

        return self.response(200, message=pk)
    
    def _deserialize_pk_if_composite(self, datamodel, pk):
        def date_deserializer(obj):
            if "_type" not in obj:
                return obj

            from dateutil import parser

            if obj["_type"] == "datetime":
                return parser.parse(obj["value"])
            elif obj["_type"] == "date":
                return parser.parse(obj["value"]).date()
            return obj

        if datamodel.is_pk_composite():
            try:
                pk = json.loads(pk, object_hook=date_deserializer)
            except Exception:
                pass
        return pk

class DBWithCompoundKey(BaseApi):
    @expose('/get/<pk>')

    def greeting(self, pk):
        # self.datamodel = SQLAInterface(CoursesPerCycle)
        datamodel = SQLAInterface(Cycles, db.session)
        print (all_fields(datamodel))
        print (datamodel.list_columns)
        # pk = self._deserialize_pk_if_composite(datamodel,pk)
        print (pk)
        d = datamodel.get(pk)
        return self.response(200, pk=pk, data=d)
    
    # def _deserialize_pk_if_composite(self, datamodel, pk):
    #     def date_deserializer(obj):
    #         if "_type" not in obj:
    #             return obj

    #         from dateutil import parser

    #         if obj["_type"] == "datetime":
    #             return parser.parse(obj["value"])
    #         elif obj["_type"] == "date":
    #             return parser.parse(obj["value"]).date()
    #         return obj

    #     if datamodel.is_pk_composite():
    #         try:
    #             pk = json.loads(pk, object_hook=date_deserializer)
    #         except Exception:
    #             pass
    #     return pk


# url="/api/get/<pk>"
appbuilder.add_api(DBWithCompoundKey)
    
class CustomFilter(BaseFilter):
    name = "Custom Filter"
    arg_name = "opr"

    def apply(self, query, value):
        return query.filter(
            or_(Contact.name.like(value + "%"), Contact.address.like(value + "%"))
        )
    
class CyclesModelApi(ModelRestApi):
    resource_name = "cycle"
    datamodel = SQLAInterface(Cycles)
    allow_browser_login = True

    search_filters = {"name": [CustomFilter]}
    openapi_spec_methods = {
        "get_list": {"get": {"description": "Get all contacts, filter and pagination"}}
    }



# appbuilder.add_api(CyclesModelApi)
    
class TestModelApi(ModelRestApi):
    resource_name = "test"
    datamodel = SQLAInterface(CoursesPerCycle)
    allow_browser_login = True

    # search_filters = {"name": [CustomFilter]}
    # openapi_spec_methods = {
    #     "get_list": {"get": {"description": "Get all contacts, filter and pagination"}}
    # }
    # print ("**** from testModelApi(ModelRestApi)")

# appbuilder.add_api(TestModelApi)

# '/coursespercyclemodelview/api/column/add/courses_per_cycle?_flt_0_cycle_id={{cycle_id}}'