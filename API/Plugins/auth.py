import cherrypy
import psutil
from API import APIPluginInterface
import logging
import json

__plugin__ = "AuthAPI"
__plugin_version__ = "0.1"


class AuthAPI(APIPluginInterface):
    api_path = "/auth"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True,
            'tools.jwtauth.on': True,
            'tools.jwtauth.login': True
        }
    }

    def __init__(self, server):
        super(AuthAPI, self).__init__(server)

    def GET(self):
        # Check the request headers, if HTML is requested
        # provide HTML login page. 
        return True

    def POST(self):
        print (json.dumps(cherrypy.request.json))
        return True
