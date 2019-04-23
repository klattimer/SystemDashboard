import os, sys
print ("Started as " + os.getlogin())
if os.geteuid() != 0:
    os.execvp("sudo", ["sudo"] + [os.environ['_']] + sys.argv)
activate_this_file = os.path.abspath("venv/bin/activate_this.py")
with open(activate_this_file) as f:
    exec(f.read(), {'__file__': activate_this_file})

import cherrypy
import logging
from API import APIRegistry
from json import JSONEncoder
import json
from copy import copy
import datetime
import re
from Tools.cp_jwtauth import JWTAuthTool, PAMAuthMech


#
# Monkey patches for JSON Serialisation
#
def _default(self, obj):
    if type(obj) == datetime.datetime:
         return obj.isoformat()
    try:
        out = getattr(obj.__class__, "serialise", _default.default)(obj)
    except:
        raise Exception("Cannot JSON Serialise object: " + obj.__class__.__name__)
    return out

_default.default = JSONEncoder.default
JSONEncoder.default = _default

def iter(obj):
    if getattr(obj.__class__, "as_dict", None) is not None:
        obj = obj.as_dict()
    if getattr(obj.__class__, "_asdict", None) is not None:
        obj = obj._asdict()
    if isinstance(obj, dict):
        items = list(obj.items())
        for k,v in items:
            obj[k] = iter(v)
    if isinstance(obj, list):
        for i, v in enumerate(copy(obj)):
            obj[i] = iter(v)
    return obj

def _encode(obj):
    return _encode.encode(iter(obj))

_encode.encode = cherrypy._json.encode
cherrypy._json.encode = _encode

class Root(object): pass

class Server(object):
    conf = {}
    def __init__(self, conf):
        self.conf = conf
        ip = self.validateIP()
        port = self.validatePort()
        cherrypy.tools.jwtauth = JWTAuthTool(
            "SystemDashboard",
            "mysupersecretpassphraseformytokens",
            PAMAuthMech
        )
        cherrypy.config.update({
            'server.socket_host': ip,
            'server.socket_port': port,
            'error_page.400': self.JSONErrorHandler,
            'error_page.404': self.JSONErrorHandler,
            'error_page.403': self.JSONErrorHandler,
            'error_page.405': self.JSONErrorHandler,
            'error_page.500': self.JSONErrorHandler,
            'error_page.441': self.JSONErrorHandler,
            'error_page.442': self.JSONErrorHandler
        })

        PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Static')
        cherrypy.tree.mount(Root(), '/', config={
            '/': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': PATH,
                    'tools.staticdir.index': 'index.html'
                },
        })

        self.api = APIRegistry(self)

    def validateIP(self):
        if re.match(r"(([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4})", self.conf["host"]) or re.match(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", self.conf["host"]):
            return self.conf["host"]
        return "0.0.0.0"

    def validatePort(self):
        if re.match(r"^\d{1,5}$", str(self.conf["port"])):
            return self.conf["port"]
        return "8080"

    def JSONErrorHandler(self, status, message, traceback, version):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'
        statusi = str(status).strip()
        r = re.compile("\d+")
        results = r.findall(statusi)
        statusi = int(results[0])
        status = status.replace(str(statusi), "").strip()
        return json.dumps({'status': statusi, 'message': message, 'error': status})

    def run(self):
        cherrypy.engine.start()
        cherrypy.engine.block()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    data = {}
    with open('config.json') as conf:
        data = json.load(conf)
    server = Server(data)
    f = open("app.pid", "w")
    f.write(str(os.getpid()))
    f.close()
    server.run()
