import pandas as pd
from pdb import set_trace as stop


class ValenoqDateInterval(object):

    def __init__(self, start_end, frequency):
        self.api_type = "intraday"
        if frequency == "day":
            self.api_type = "eod"
        self.start_end = [pd.to_datetime(item) for item in start_end]


class ValenoqApiReqest(object):

    def __init__(self, date_interval, collapse):
        pass

    def _create_url(self):
        pass

    def ask_valenoq(self, ticker):
        pass


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
        Default value: "day"
    collapse: {1, 5, 10, 15, 30}, optional
        The interval of intraday data. Applicable only if the frequency is "minute".
        Example: collapse = 5: returns data represented as an array of 5-minute bars.
        Default value: 5
    out_format: {"json", "array", "pandas"}, optional
        The format of the output.
        Default value: pandas DataFrame object
    """
    result = dict()

    api_key = kwargs.get("api_key")
    # validate api_key: TODO

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

    frequency = kwargs.get("frequency", "day")
    date_interval = ValenoqDateInterval(start_end, frequency)

    collapse = kwargs.get("collapse", 5)
    api_req = ValenoqApiReqest(date_interval, collapse)

    for tick in set(ticker):
        result[tick] = api_req.ask_valenoq(tick)

    format = kwargs.get("out_format", "pandas")
    # adjust results to correct format TODO


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
