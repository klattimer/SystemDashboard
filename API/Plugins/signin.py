import cherrypy
from API import APIPluginInterface
from mako.lookup import TemplateLookup
import os

__plugin__ = "Signin"
__plugin_version__ = "0.1"


class Signin(APIPluginInterface):
    api_path = "/signin"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.Dispatcher(),
        }
    }

    def __init__(self, server):
        super(Signin, self).__init__(server)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Templates"))
        self.lookup = TemplateLookup(directories=[path])

    @cherrypy.expose
    def index(self):
        output = self.lookup.get_template("signin.html")
        return output.render()
