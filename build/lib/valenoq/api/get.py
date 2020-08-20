from pdb import set_trace as stop


def get(ticker, *args, **kwargs):
    """
    Get the time series for the provided ticker(s).

    Parameters
    ----------
    ticker : str or list
        The ticker name or list of ticker names for which the data is requested
        The maximum length of the list is 5
    api_key: str
        The API key (available after registration at https://valenoq.com);
        If no API key provided then the returned data is limited to 30 bars
    start: str or datetime
        The start date
    end: str or datetime
        The end date
    frequency: {"minute", "hour", "day"}, optional
        The data frequency. 
        Default value: "day"
    collapse: {1, 5, 10, 15, 30}, optional
        The interval of intraday data. Applicable only if the frequency is "minute".
        Example: collapse = 5: returns data represented as an array of 5-minute bars.
        Default value: 5
    out_format: {"json", "array", "pandas"}, optional
        The format of the output
    """
    pass

def balance_sheet(ticker, *args, **kwargs):
    """
    Get the balance sheet data for the provided ticker(s).

    Parameters
    -----------
    ticker : str or list
        The ticker name or list of ticker names for which the data is requested
        The maximum length of the list is 5
    api_key: str
        The API key (available after registration at https://valenoq.com);
        If no API key provided then the returned data is limited to 30 bars
    nr_quarters: int, optional
        The number of quarters (since the last one) for which the data is requested.
        Maximum limit is 12. Default value is 1 (returns the balance sheet data for
        the last quarter)
    out_format: {"json", "array", "pandas"}, optional 
        The format of the output
    """
    pass
