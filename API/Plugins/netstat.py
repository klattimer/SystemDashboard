import cherrypy
import psutil
from API import APIPluginInterface
import subprocess
import logging
import pwd
import os
import re
import glob
import socket

__plugin__ = "NetstatAPI"
__plugin_version__ = "0.1"

PROC_TCP = "/proc/net/tcp"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
    }


class NetstatAPI(APIPluginInterface):
    api_path = "/api/netstat"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    scripts = [
        {
            "src": "Javascript/netstat.js"
        }
    ]

    def __init__(self, server):
        super(NetstatAPI, self).__init__(server)

    def _load(self):
        ''' Read the table of tcp connections & remove header  '''
        with open(PROC_TCP,'r') as f:
            content = f.readlines()
            content.pop(0)
        return content

    def _hex2dec(self, s):
        return str(int(s,16))

    def _ip(self, s):
        ip = [(self._hex2dec(s[6:8])),(self._hex2dec(s[4:6])),(self._hex2dec(s[2:4])),(self._hex2dec(s[0:2]))]
        return '.'.join(ip)

    def _remove_empty(self, array):
        return [x for x in array if x !='']

    def _convert_ip_port(self, array):
        host,port = array.split(':')
        return self._ip(host),self._hex2dec(port)

    def _get_pid_of_inode(self, inode):
        '''
        To retrieve the process pid, check every running process and look for one using
        the given inode.
        '''
        for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
            try:
                if re.search(inode,os.readlink(item)):
                    return item.split('/')[2]
            except:
                pass
        return None

    def netstat(self):
        '''
        Function to return a list with status of tcp connections at linux systems
        To get pid of all network process running on system, you must run this script
        as superuser
        '''

        content=self._load()
        result = []
        for line in content:
            line_array = self._remove_empty(line.split(' '))     # Split lines and remove empty spaces.
            l_host,l_port = self._convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal.
            r_host,r_port = self._convert_ip_port(line_array[2])
            tcp_id = line_array[0]
            state = STATE[line_array[3]]
            uid = pwd.getpwuid(int(line_array[7]))[0]       # Get user from UID.
            inode = line_array[9]                           # Need the inode to get process pid.
            pid = self._get_pid_of_inode(inode)                  # Get pid prom inode.
            try:                                            # try read the process name.
                exe = os.readlink('/proc/'+pid+'/exe')
            except:
                exe = None
            try:
                service = socket.getservbyport(int(l_port))
            except:
                service = None

            connection = {
                'id': tcp_id,
                'uid': uid,
                'service': service,
                'local_port': int(l_port),
                'local_address': l_host,
                'local': l_host+':'+l_port,
                'remote': r_host+':'+r_port,
                'remote_port': int(r_port),
                'remote_address': r_host,
                'state': state,
                'pid': pid,
                'executable': exe
            }
            result.append(connection)
        return result

    def GET(self, **params):
        return self.netstat()
