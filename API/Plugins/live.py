import cherrypy
import psutil
from API import APIPluginInterface
import logging

__plugin__ = "LiveAPI"
__plugin_version__ = "0.1"


class LiveAPI(APIPluginInterface):
    api_path = "/api/live"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True,
            'tools.jwtauth.on': True,
            'tools.jwtauth.required': True
        }
    }

    def __init__(self, server):
        super(LiveAPI, self).__init__(server)

    def GET(self):
        return True
