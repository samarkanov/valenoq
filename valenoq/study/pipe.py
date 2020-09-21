from pdb import set_trace as stop
from time import sleep
import requests
import json
import os
from valenoq_utils.reply import MSIxReply
from valenoq.errors import (VALENOQxNETWORKxERROR,
                            VALENOQxNOTxIMPLEMENTEDxERROR,
                            VALENOQxINITIALIZATIONxERROR)

BASE_URL_VALENOQ_SERVICES = "http://vps-640ef6ef.vps.ovh.net:13000/"

class Pipe(object):

    def __init__(self, columns=None):
        self.columns = columns

class PipeReply(object):

    def __init__(self, pipe_obj, **kwargs):
        self.pipe = pipe_obj
        self.beg = kwargs.get("beg")
        self.end = kwargs.get("end")
        self.username = self.get_username()

    def get_username(self):
        # if 0: # TODO: remove me
        username = os.getenv("JUPYTERHUB_USER")
        username = username.replace("@", "_40")
        username = username.replace(".", "_2E")
        # else:
        #     username = "samarkanov_40gmail_2Ecom" # TODO: remove me

        return username

    def ask(self):
        reply = MSIxReply(success=False, res=dict())

        if not self.pipe:
            # call notebooks-valenoq
            req_args = "?beg={beg}&end={end}&name={name}".format(beg=self.beg,
                                                                 end=self.end,
                                                                 name=self.username)
            res = requests.get("%s%s" %(BASE_URL_VALENOQ_SERVICES, req_args))

            if res.status_code != 200:
                msg = "Unsuccessful call to the backend, status code: %d" %res.status_code
                err = VALENOQxNETWORKxERROR(msg).dict()
                reply = MSIxReply(success=False, res=err)
            else:
                res = json.loads(res.text)
                if res.get("success") == False:
                    msg = "Errors during the initialization of the environment, reply from the backend: %s" %str(res)
                    err = VALENOQxINITIALIZATIONxERROR(msg).dict()
                    reply = MSIxReply(success=False, res=err)
                else:
                    ctx = dict()
                    ctx["data"] = res.get("result")
                    reply = MSIxReply(success=True, res=ctx)
        else:
            msg = "Not Implemented error"
            err = VALENOQxNOTxIMPLEMENTEDxERROR(msg).dict()
            reply = MSIxReply(success=False, res=err)

        return reply

def check_run_on_valenoq(func):
    def wrapper(*args, **kwargs):
        ctx = dict()
        if os.getenv("JUPYTERHUB_ACTIVITY_URL") and os.getenv("PWD") == "/home/jovyan":
            ctx = func(*args, **kwargs)
        else:
            msg = "Pipe execution is only available when running from https://valenoq.com notebook"
            err = VALENOQxINITIALIZATIONxERROR(msg).dict()
            ctx = MSIxReply(success=False, res=err)
        return ctx
    return wrapper

@check_run_on_valenoq
def run_pipe(pipe_obj, start, end):
    return PipeReply(pipe_obj, beg=start, end=end).ask()
