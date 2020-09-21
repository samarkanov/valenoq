import sys
import json
import inspect
from pdb import set_trace as stop

def err_as_dict(err_obj):
    res = {"error": err_obj.errtype, "text": err_obj.text}
    return res

class VALENOQxBASExERROR(Exception):

    def __init__(self, msg):
        try:
            ln = sys.exc_info()[-1].tb_lineno
        except AttributeError:
            ln = inspect.currentframe().f_back.f_lineno
        self.message = "{0.__name__}: {1}".format(type(self), msg)
        self.text = msg
        self.errtype = type(self).__name__
        self.msg = msg

    def dict(self):
        ctx = dict()
        ctx["errtype"] = self.errtype
        ctx["msg"] = self.msg
        return ctx

class VALENOQxNETWORKxERROR(VALENOQxBASExERROR):
    pass

class VALENOQxINITIALIZATIONxERROR(VALENOQxBASExERROR):
    pass

class VALENOQxNOTxIMPLEMENTEDxERROR(VALENOQxBASExERROR):
    pass
