import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

import pandas as pd
import re
import datetime
import requests

def get_historic_data(ticker,start_date,end_date=None):
    '''
    The ticker symbol, start date, and end date strings are used to construct
    the http get request for the historic stock data, and returns the response
    as a string

    Parameters
    ----------
    ticker: a string
    start_date: a string
    end_date: a string

    Returns
    -------
    a string
    '''

    base_url = 'http://ichart.finance.yahoo.com/table.csv'

    #define local function to check format of ticker symbol
    def check_get_ticker(ticker,param_dict):

        regex_match = re.match('^[A-Z]*$',ticker)

        if regex_match is not None:
            param_dict['s'] = ticker

    #define local function to check format of dates
    def check_get_date(date,param_dict,keys):

        try:
            #the date must be formmated as month/day/year
            dt = datetime.datetime.strptime(date, '%m/%d/%Y')
        except (ValueError, TypeError):
            raise ValueError('Date is not properly formatted.')

        param_dict[keys[0]] = str(dt.month-1) #yahoo api uses zero based months
        param_dict[keys[1]] = str(dt.day)
        param_dict[keys[2]] = str(dt.year)

    params = dict() #http url parameters

    #vaidate the input strings and populate the dictionary of parameters
    check_get_ticker(ticker,params)

    check_get_date(start_date,params,keys=['a','b','c'])

    check_get_date(end_date,params,keys=['d','e','f'])

    #indicate that we want daily frequency
    params['g'] = 'd'

    #send the http request
    r = requests.get(base_url,params)

    if r.status_code == 200:

        return r.text

    else:

        return None

def get_historic_dataframe(ticker,start_date,end_date=None):
    '''
    The ticker symbol, start date, and end date strings are used to construct
    the http get request for the historic stock data, and returns the response
    as pandas dataframe

    Parameters
    ----------
    ticker: a string
    start_date: a string
    end_date: a string

    Returns
    -------
    a pandas dataframe
    '''

    text = get_historic_data(ticker,start_date,end_date)

    #if the return value is not None then it's garunteed to obtain the data
    if text is not None:

        return pd.read_csv(StringIO(text),parse_dates=['Date'],
                infer_datetime_format=True)

    else:

        return None
