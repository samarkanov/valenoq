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


class NodeVisitor(object):

    def _visit(self, node):
        if not node:
            return
        method_name = 'visit_' + node.type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit(self, node):
        return self._visit(node)

    def generic_visit(self, node):
        raise Exception('No visit_{type} method'.format(type=node.type))


class Interpreter(NodeVisitor):

    def __init__(self, df):
        self.df = df
        self.df["ticker"] = self.df.index
        self.df.set_index(self.df.date, inplace=True)
        del self.df["date"]
        self.df.rename(columns={'c': 'close', 'o': 'open', 'h': 'high', 'l': 'low', 'v': 'volume'}, inplace=True)
        self.df.sort_index(inplace=True)

    def get_df(self):
        return self.df

    def interpret(self, algo_node):
        return self.visit(algo_node)

    def visit_str(self, node):
        return node.value

    def visit_int(self, node):
        return node.value

    def visit_math(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.value == "DIV":
            return left / right
        elif node.value == "SUB":
            return left - right
        elif node.value == "ADD":
            return left + right
        elif node.value == "MUL":
            return left * right
        else:
            raise VALENOQxNOTxIMPLEMENTEDxERROR()

    def visit_func(self, node):
        if node.value == "SMA":
            type = self.visit(node.params[0])
            window = self.visit(node.params[1])
            group = self.df.groupby('ticker')[type]
            return group.transform(lambda x: x.rolling(window).mean())
        else:
            raise VALENOQxNOTxIMPLEMENTEDxERROR()


class PipeReply(object):

    def __init__(self, pipe_obj, **kwargs):
        self.pipe = pipe_obj
        self.beg = kwargs.get("beg")
        self.end = kwargs.get("end")
        self.username = self._get_username()

    def _get_username(self):
        username = os.getenv("JUPYTERHUB_USER")
        username = username.replace("@", "_40")
        username = username.replace(".", "_2E")
        return username

    def get_data(self):
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
        interp = Interpreter(df)

        if self.pipe:
            # post-processing of data:
            for new_col, algo_node in self.pipe.columns.items():
                df[new_col] = interp.interpret(algo_node)
        else:
            df = interp.get_df()
            
        return df

    def _prepare_env(self):
        # copy files to local
        reply = VALENOQxHTTPxREPLY(success=False, res=dict())

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

# @check_run_on_valenoq # TODO: uncomment
def run_pipe(pipe_obj, start, end):
    return PipeReply(pipe_obj, beg=start, end=end)._prepare_env()
