from flask_appbuilder.api import BaseApi, expose
from . import appbuilder


class ExampleApi(BaseApi):
    @expose('/greeting')
    def greeting(self):
        
        return self.response(200, message="Hello")


appbuilder.add_api(ExampleApi)