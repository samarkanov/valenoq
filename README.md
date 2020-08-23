# Valenoq Python Library

[![N|Solid](https://valenoq.com/static/modules/black-dashboard/img/apple-icon.png)](https://valenoq.com)

[![Build Status](https://travis-ci.org/samarkanov/valenoq.svg?branch=master)](https://travis-ci.org/samarkanov/valenoq)

Python package to interact with valenoq.com RESTful API

## Installation
```sh
 $ pip3 install valenoq
```

## Configuration
```python
from valenoq.api import config
config.set(api_key="yourApiKey") # the key is available upon registration at https://valenoq.com
```

## Current limitations
* **List of supported tickers:** https://valenoq.com/static/files/list_available_tickers_valenoqcom.txt
* **Supported historical dates**: 01/01/2015 - 31/07/2020

## API documentation
http://data.samarkanov.info/valenoq-python/

## Getting historical intraday data
**Basic functionality**:
```python
from valenoq.api import config, request
config.set(api_key="yourApiKey")

# End-of-the-day OHCLV bars for a ticker
data = request.get("AAPL", date="2018-05-01", frequency="day")

# Intraday 1-hour bars for a ticker
data = request.get("AAPL", date="2018-05-01")
# or
data = request.get("AAPL", date="2018-05-01", frequency="hour")

# Intraday x-minute bars for a ticker
data = request.get("AAPL", date="2018-05-01", frequency="minute", collapse=1)  # 1-minute bars
data = request.get("AAPL", date="2018-05-01", frequency="minute", collapse=5)  # 5-minutes bars
data = request.get("AAPL", date="2018-05-01", frequency="minute", collapse=10) # 10-minute bars
data = request.get("AAPL", date="2018-05-01", frequency="minute", collapse=15) # 15-minute bars
data = request.get("AAPL", date="2018-05-01", frequency="minute", collapse=5)  # 30-minute bars

# Interval of dates is supported:
data = request.get("AAPL", start="2018-05-01", end="2018-05-05", frequency="minute", collapse=15)
```

**Getting historical data for a list of tickers:**
```python
# 1-minute bars for AAPL, MU and INTC:
data = request.get(["AAPL", "MU", "INTC"], date="2018-05-01", frequency="minute", collapse=1)

# 15-minute bars between {01/May/2018 - 05/May/2018} for AAPL and INTC
request.get(["AAPL", "INTC"], start="2018-05-01", end="2018-05-05", frequency="minute", collapse=15)
```

## Getting balance sheet data
```python
# Last quarter data for a ticker:
data = request.balance_sheet("AAPL")

# Last quarter data for a list of tickers:
data = request.balance_sheet(["AAPL", "INTC"])

# Five last balance sheets:
data = request.balance_sheet("AAPL", nr_quarters=5)
```
