

class UWSGIConfig:
    _base = None
    _app = None
    _module = None
    _socket = None
    _chmod_socket = "chmod-socket=600"
    _callable = None
    _logto = None
    
    def __init__(self, fname):
        self.fname = fname

    def set_base(self, base):
        self._base = base

    def set_app(self, appname):
        self._app = appname
        self.module = "module=\%(%s)" % self._app
        self._callable = "callable=%s" % self._app

    def set_socket(self, socket_file):
        if self._base is not None:
            self._socket = "\%(%s)/%s" % (self._base, socket_file)
        else:
            return None

    
    def set_logto(self, logfilename):
        self._logto = logfilename

"""

[uwsgi]
base=/var/www/portal.ciplisystems.com
app=app
module=%(app)

socket=%(base)/portal.sock

chmod-socket=600

callable=app
logto=/var/log/uwsgi/portal.ciplisystems.com.log

"""
