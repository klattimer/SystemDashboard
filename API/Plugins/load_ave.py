import cherrypy
import psutil
from API import APIPluginInterface
import logging
import os

__plugin__ = "LoadAveAPI"
__plugin_version__ = "0.1"


class LoadAveAPI(APIPluginInterface):
    api_path = "/api/loadave"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }
    scripts = [
        {
            "src": "Javascript/load.js"
        }
    ]

    def __init__(self, server):
        super(LoadAveAPI, self).__init__(server)

    def GET(self, **params):
        return dict(zip([1,5,15], os.getloadavg()))
