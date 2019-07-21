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
    menuitems = [{
        "id": "users",
        "icon": "fas fa-users",
        "name": "Users",
        "order": 6
    }]
    widgets = {
        "logged_in": {
            "type": "Table",
            "size": "w2h1",
            "id": "logged_in",
            "fa_icon": "fas fa-key",
            "title_label": "Logged in Users",
            "headers": [
                {"title": "User"},
                {"title": "TTY"},
                {"title": "Host"},
                {"title": "Process"}
            ],
            "menuitem": "users"
        },
        "lastog": {
            "type": "Table",
            "size": "w2h1",
            "id": "lastlog",
            "fa_icon": "fas fa-history",
            "title_label": "Recent Logins",
            "headers": [
                {"title": "User"},
                {"title": "Time"},
                {"title": "Host"}
            ],
            "menuitem": "users"
        }
    }
    templates = [
        "Table"
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
            logging.warning("Cannot get psutil data")
            errors.append({"type": "critical", "message": "psutil exception"})
        lastlog = None
        try:
            lastlog =  self.lastlog()
        except:
            logging.warning("Cannot get lastlog data")
            errors.append({"type": "error", "message": "lastlog exception"})

        return {
            "logged_in": users,
            "last_logins": lastlog,
            "errors": errors
        }
