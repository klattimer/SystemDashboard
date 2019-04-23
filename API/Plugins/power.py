import cherrypy
import os
from API import APIPluginInterface

__plugin__ = "PowerAPI"
__plugin_version__ = "0.1"


class PowerAPI(APIPluginInterface):
    api_path = "/api/power"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }
    styles = [
        {
            "href": "CSS/power.css",
            "rel": "stylesheet",
            "type": "text/css"
        }
    ]
    scripts = [
        {
            "src": "Javascript/power.js"
        }
    ]

    def __init__(self, server):
        super(PowerAPI, self).__init__(server)

    def GET(self, action):
        #
        # TODO: We need to set a flag for which state we're currently
        #       in so we can repeat that response when asked, if
        #       requests keep coming after the action.
        #
        if action == "reboot":
            #
            # TODO: Write the reboot log, this allows us to get an
            #       average time to reboot, meaning we can display a
            #       client side warning when that time is exceeded
            #
            os.system("sudo shutdown -r now")
            return {
                'status': "rebooting",
                'estimated reboot time': 37
            }

        if action == "shutdown":
            os.system("sudo shutdown -h now")
            return {'status': "shutting down"}

        return {"status": "running"}
