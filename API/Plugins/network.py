import cherrypy
import psutil
from API import APIPluginInterface
import logging

__plugin__ = "NetworkAPI"
__plugin_version__ = "0.1"


class NetworkAPI(APIPluginInterface):
    api_path = "/api/network"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    scripts = [
        {
            "src": "Javascript/network.js"
        }
    ]

    def __init__(self, server):
        super(NetworkAPI, self).__init__(server)

    def GET(self, **params):
        psutil.net_io_counters(pernic=True)
        return {
            "addresses": psutil.net_if_addrs(),
            "io": psutil.net_io_counters(pernic=True, nowrap=True),
            "stats": psutil.net_if_stats(),
            "radar_data": []
        }
