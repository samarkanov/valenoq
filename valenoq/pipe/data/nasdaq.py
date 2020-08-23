import os
import requests
import json
from pdb import set_trace as stop
from valenoq.api.request import BASE_URL, ValenoqAPICall404, extract_data
from valenoq.api import config


class ValenoqLazyTS(object):

    def __init__(self, param):
        self.param = param
        api_key = config.get("api_key")
        url = "eod?key={key}&start=20000101&end=20250101&ticker=all".format(key=api_key)
        url = os.path.join(BASE_URL, url)
        reply = requests.get(url)
        if reply.status_code != 200:
            raise ValenoqAPICall404("{url} cannot be reached. Please retry later".format(url=url))

        self.lazy_data = extract_data(json.loads(reply.text))


close = ValenoqLazyTS("close")
