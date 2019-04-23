import cherrypy
import psutil
from API import APIPluginInterface
import logging
import struct
from datetime import datetime
import pwd
import psutil



__plugin__ = "UsersAPI"
__plugin_version__ = "0.1"


LASTLOG_STRUCT = 'i32s256s'
LASTLOG_STRUCT_SIZE = struct.calcsize(LASTLOG_STRUCT)

class UsersAPI(APIPluginInterface):
    api_path = "/api/users"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    scripts = [
        {
            "src": "Javascript/users.js"
        }
    ]

    def __init__(self, server):
        super(UsersAPI, self).__init__(server)

    def lastlog(self):
        filename = '/var/log/lastlog'
        result = []
        uid = 0
        with open(filename, 'rb') as fp:
            while True:
                bytes = fp.read(LASTLOG_STRUCT_SIZE)
                if len(bytes) < LASTLOG_STRUCT_SIZE or bytes is None: break
                data = struct.unpack(LASTLOG_STRUCT, bytes)
                if data[0] != 0:
                    data = list(data)
                    data[1] = data[1].replace(b'\x00',b'').decode("utf-8")
                    data[2] = data[2].replace(b'\x00',b'').decode("utf-8")
                    data.append(pwd.getpwuid(uid).pw_name)

                    data[0] = datetime.fromtimestamp(data[0])
                    result.append(dict(zip(['timestamp', 'terminal', 'host', 'name'], data)))
                uid += 1

        return result

    def GET(self, **params):
        errors = []
        try:
            users = psutil.users()
            for i, user in enumerate(users):
                d = user._asdict()
                d['started'] = datetime.fromtimestamp(d['started'])
                process = psutil.Process(d['pid'])
                d['process_name'] = process.name()
                users[i] = d
        except:
            logging.exception("Cannot get psutil data")
            self.errors.append({"type": "critical", "message": "psutil exception"})
        try:
            lastlog =  self.lastlog()
        except:
            logging.exception("Cannot get lastlog data")
            self.errors.append({"type": "error", "message": "lastlog exception"})

        return {
            "logged_in": users,
            "last_logins": lastlog,
            "errors": errors
        }
