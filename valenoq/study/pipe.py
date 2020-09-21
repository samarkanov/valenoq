from pdb import set_trace as stop
from time import sleep
import pandas as pd
import requests
import json
import os
from valenoq_utils.reply import MSIxReply
from valenoq.errors import (VALENOQxNETWORKxERROR,
                            VALENOQxNOTxIMPLEMENTEDxERROR,
                            VALENOQxINITIALIZATIONxERROR)

BASE_URL_VALENOQ_SERVICES = "http://vps-640ef6ef.vps.ovh.net:13000/"


class VALENOQxHTTPxREPLY(MSIxReply):

    def __init__(self, success, res, handle=None):
        super().__init__(success, res)
        self._handle = handle
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self._handle.get_data()
        return self._data


class Pipe(object):

    def __init__(self, columns=None):
        self.columns = columns


class PipeReply(object):

    def __init__(self, pipe_obj, **kwargs):
        self.pipe = pipe_obj
        self.beg = kwargs.get("beg")
        self.end = kwargs.get("end")
        self.username = self._get_username()

    def get_data(self):
        try:
            reply = self._get_data()
        except VALENOQxINITIALIZATIONxERROR:
            err = VALENOQxINITIALIZATIONxERROR("Data is not correctly initialized").dict()
            reply = VALENOQxHTTPxREPLY(success=False, res=err)
        return reply

    def _get_username(self):
        username = os.getenv("JUPYTERHUB_USER")
        username = username.replace("@", "_40")
        username = username.replace(".", "_2E")
        return username

    def _get_data(self):
        data = []
        home = os.path.expanduser("~")
        data_dir = os.path.join(home, ".valenoq", "data")
        if not os.path.isdir(data_dir):
            raise VALENOQxINITIALIZATIONxERROR()

        _raw_data = os.listdir(data_dir)
        raw_data = [item for item in _raw_data if ".hdf5" in item]
        if not raw_data:
            raise VALENOQxINITIALIZATIONxERROR()

        for file_ in raw_data:
            data.append(pd.read_hdf(os.path.join(data_dir, file_)))

        df = pd.concat(data)
        return df

    def _prepare_env(self):
        # copy files to local
        reply = VALENOQxHTTPxREPLY(success=False, res=dict())

        if not self.pipe:
            # call notebooks-valenoq
            req_args = "?beg={beg}&end={end}&name={name}".format(beg=self.beg,
                                                                 end=self.end,
                                                                 name=self.username)
            res = requests.get("%s%s" %(BASE_URL_VALENOQ_SERVICES, req_args))

            if res.status_code != 200:
                msg = "Unsuccessful call to the backend, status code: %d" %res.status_code
                err = VALENOQxNETWORKxERROR(msg).dict()
                reply = VALENOQxHTTPxREPLY(success=False, res=err)
            else:
                res = json.loads(res.text)
                if res.get("success") == False:
                    msg = "Errors during the initialization of the environment, reply from the backend: %s" %str(res)
                    err = VALENOQxINITIALIZATIONxERROR(msg).dict()
                    reply = VALENOQxHTTPxREPLY(success=False, res=err)
                else:
                    ctx = dict()
                    ctx["data"] = res.get("result")
                    reply = VALENOQxHTTPxREPLY(success=True, res=ctx, handle=self)
        else:
            msg = "Not Implemented error"
            err = VALENOQxNOTxIMPLEMENTEDxERROR(msg).dict()
            reply = VALENOQxHTTPxREPLY(success=False, res=err)

        return reply

def check_run_on_valenoq(func):
    def wrapper(*args, **kwargs):
        ctx = dict()
        if os.getenv("JUPYTERHUB_ACTIVITY_URL") and os.getenv("PWD") == "/home/jovyan":
            ctx = func(*args, **kwargs)
        else:
            msg = "Pipe execution is only available when running from https://valenoq.com notebook"
            err = VALENOQxINITIALIZATIONxERROR(msg).dict()
            ctx = VALENOQxHTTPxREPLY(success=False, res=err)
        return ctx
    return wrapper

@check_run_on_valenoq
def run_pipe(pipe_obj, start, end):
    return PipeReply(pipe_obj, beg=start, end=end)._prepare_env()
