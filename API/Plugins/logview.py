import cherrypy
from API import APIPluginInterface
import logging
import os
__plugin__ = "LogAPI"
__plugin_version__ = "0.1"


class LogAPI(APIPluginInterface):
    api_path = "/api/log"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    def __init__(self, server):
        super(LogAPI, self).__init__(server)

    def file_len(self, fname):
        offsets = {0:0}
        i = 1
        with open(fname) as f:
            line = f.readline()
            while line:
                i += 1
                offsets[i] = f.tell()
                line = f.readline()
        return (offsets, i)

    def GET(self, **params):
        fname = 'syslog'
        if 'file' in params.keys():
            fname = params['file']

        fname = '/var/log/' + fname
        if not os.path.exists(fname):
            raise cherrypy.HTTPError(500, "Path does not exist on server")

        chunk_size = 30 # lines
        if 'size' in params.keys():
            chunk_size = int(params['size'])

        if 'start' in params.keys():
            chunk_start = int(params['start'])
        else:
            chunk_start = -1 * chunk_size


        (offsets, length) = self.file_len(fname)

        start = chunk_start % length
        end = start + chunk_size
        if start > length:
            start = length
        if end > length:
            end = length

        with open(fname) as f:
            try:
                f.seek(offsets[start])
                chunk = f.read(offsets[end] - offsets[start])
            except:
                logging.exception("Problem loading data chunk")
                logging.debug("File: %s, Length: %d, Start: %d, End: %d" % (fname, length, start, end))
        return {
            "num_lines": length,
            "start": start,
            "end": end,
            "size": end - start,
            "data": chunk
        }
