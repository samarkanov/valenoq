import json
import requests
import pandas as pd
from valenoq.api import config
from pdb import set_trace as stop

BASE_URL = "https://valenoq.com/api/v1/"


class ValenoqAPICall404(Exception):
    pass


class ValenoqDateInterval(object):

    def __init__(self, start_end, frequency, collapse):
        self.api_type = "eod" if frequency == "day" else "intraday"

        if frequency == "minute":
            self.frequency = "min"
            self.collapse = collapse
        else:
            self.frequency = frequency
            self.collapse = 1

        self.start_end = [pd.to_datetime(item) for item in start_end]

    def get_start(self):
        return self.start_end[0].strftime("%Y%m%d")

    def get_end(self):
        return self.start_end[1].strftime("%Y%m%d")

    def get_req_url(self):
        req_url = str()
        start = self.get_start()
        end = self.get_end()
        if self.api_type == "intraday":
            req_url = ("datefrom={start}&dateto={end}&step={step}&duration={duration}"
            ).format(start=start, end=end, step=self.frequency, duration=self.collapse)
        elif self.api_type == "eod":
            req_url = ("start={start}&end={end}").format(start=start, end=end)
        return req_url


class ValenoqApiReqest(object):

    def __init__(self, api_key, date_interval):
        self.api_key = api_key
        self.date_interval = date_interval
        self.url = self._create_url()

    def _create_url(self):
        url = ("{base_url}{api_type}?{date_url}&key={api_key}"
               ).format(api_key=self.api_key,
                        base_url=BASE_URL,
                        api_type=self.date_interval.api_type,
                        date_url=self.date_interval.get_req_url())
        return url

    def ask_valenoq(self, ticker):
        self.url += "&ticker={ticker}".format(ticker=ticker)
        reply = requests.get(self.url)
        if reply.status_code != 200:
            raise ValenoqAPICall404("{url} cannot be reached. Please retry later".format(url=self.url))
        return json.loads(reply.text)

    def format(self, raw):
        res = dict()
        if self.date_interval.api_type == "intraday":
            # flatten the nested structure
            if raw:
                for date_str, val in raw.items():
                    for time_str, ohclv in val.items():
                        res["%s%s" %(date_str, time_str)] = ohclv
        else:
            res = raw
        return res

def get(ticker, *args, **kwargs):
    """
    Get the time series data for the provided ticker(s).

    Parameters
    ----------
    ticker : str or list
        The ticker name or list of ticker names for which the data is requested
        The maximum length of the list is 5
    start: str or datetime, optional
        The start date of the data series
    end: str or datetime, optional
        The end date of the data series
        Must be provided is the `start` day is not empty
    date: str or datetime, optional
        The requested date
        If:
            - No `date` is provided
            - And no <`start`, `end`> dates are provided
            then no data will be returned
    api_key: str, optional
        The API key (available after registration at https://valenoq.com)
        If:
            - No API key provided
            - And ~/.valenoq/api.config does not exist
            - And ~/.valenoq/api.config does not contain the correct api_key
            then the returned time series data will be truncated
    frequency: {"minute", "hour", "day"}, optional
        The data frequency.
        Default value: "hour"
    collapse: {1, 5, 10, 15, 30}, optional
        The interval of intraday data. If:
            - the requested frequency is "hour"
            - or the requested frequency is "day"
            the provided value of `collapse` is ignored and set to default 1
        If:
            - the requested frequency is "minute"
            the provided of `collapse` value is taken
        Example:
            - `collapse` = 5
            - and `frequency` = "minute"
            returns data represented as an array of 5-minute bars.
        Default values:
            - 5 if the requested `frequency` is "minute"
            - 1 otherwise
    out_format: {"json", "dict", "pandas"}, optional
        The format of the output.
        Default value: pandas DataFrame object
    """
    result = dict()

    api_key = kwargs.get("api_key", config.get("api_key"))

    if isinstance(ticker, str):
        ticker = [ticker]

    start_end = list()
    start = kwargs.get("start")
    end = kwargs.get("end")
    date = kwargs.get("date")

    if start and end:
         start_end = [start, end]

    if start and not end:
         start_end = [start, start]

    if date:
         start_end = [date, date]

    frequency = kwargs.get("frequency", "hour")
    collapse = kwargs.get("collapse", 5)
    date_interval = ValenoqDateInterval(start_end, frequency, collapse)

    api_req = ValenoqApiReqest(api_key, date_interval)

    for tick in set(ticker):
        res = api_req.ask_valenoq(tick)
        if res.get("success") == False:
            res = res.get("result", {"error": "VALENOQx404",
                                     "text": "Error while making API call. Please retry later"})
            err_msg = res.get("text")
            err_code = res.get("error")
            raise ValenoqAPICall404("%s (error code: %s)" %(err_msg, err_code))
        else:
            res = res.get("result")
            result[tick] = api_req.format(res)

    outformat = kwargs.get("out_format", "pandas")

    if outformat == "pandas":
        df_list = list()
        for tick, data in result.items():
            df = pd.DataFrame(data).transpose()
            df.index = pd.to_datetime(df.index)
            df.index.name = "date"
            df["ticker"] = tick
            df_list.append(df)
        result = pd.concat(df_list)

    elif outformat == "json":
        result = json.dumps(result)

    return result


def balance_sheet(ticker, *args, **kwargs):
    """
    Get the balance sheet data for the provided ticker(s).

    Parameters
    -----------
    ticker : str or list
        The ticker name or list of ticker names for which the data is requested
        The maximum length of the list is 5
    api_key: str, optional
        The API key (available after registration at https://valenoq.com)
        If:
            - No API key provided
            - Or ~/.valenoq/api.config does not exist
            - Or ~/.valenoq/api.config does not contain the correct api_key
            then the returned balance sheet data will truncated
    nr_quarters: int, optional
        The number of quarters (since the last one) for which the data is requested.
        Maximum limit is 12.
        Default value: 1 (latest reported balance sheet)
    out_format: {"json", "array", "pandas"}, optional
        The format of the output.
        Default value: pandas DataFrame object
    """
    pass
