import cherrypy
from API import APIPluginInterface
import logging
import glob
import os
__plugin__ = "LogsAPI"
__plugin_version__ = "0.1"


class LogsAPI(APIPluginInterface):
    api_path = "/api/logs"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    def __init__(self, server):
        super(LogsAPI, self).__init__(server)

    def GET(self):
        logs = glob.glob('/var/log/**/*log', recursive=True)

        excludes = [
        	"/var/log/lastlog"
        ]

        return [log for log in logs if log not in excludes]
