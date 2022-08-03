import pandas as pd
import re

def verifyDateForBooking(mews: pd.DataFrame, booking: pd.DataFrame):
    
    # changing datatype, datadatetime to string
    booking['Arrival'] = booking['Arrival'].astype(str)
    booking['Departure'] = booking['Departure'].astype(str)
    mews['Arrival'] = mews['Arrival'].astype(str)
    mews['Departure'] = mews['Departure'].astype(str)

    # verify the date format
    mews['Arrival'] = list(map(lambda x: x.split(' ')[0] if re.compile(
        r'(\d{4})-(\d+)-(\d+) *').match(x) else 'invalid format. use date as yyyy-mm-dd', mews['Arrival']))

    mews['Departure'] = list(map(lambda x: x.split(' ')[0] if re.compile(
        r'(\d{4})-(\d+)-(\d+) *').match(x) else 'invalid format. use date as yyyy-mm-dd', mews['Departure']))

    booking['Arrival'] = list(map(lambda x: x if re.compile(r'(\d{4})-(\d+)-(\d+)').match(x) else 'invalid format. use date as yyyy-mm-dd', booking['Arrival']))

    booking['Departure'] = list(map(lambda x: x if re.compile(r'(\d{4})-(\d+)-(\d+)').match(x) else 'invalid format. use date as yyyy-mm-dd', booking['Departure']))

    return mews, booking   # return the dataframe with the new date format


def verifyDateForSitminder(mews: pd.DataFrame, siteminder: pd.DataFrame):
    
    # changing datatype, datadatetime to string
    siteminder['Arrival'] = siteminder['Arrival'].astype(str)
    siteminder['Departure'] = siteminder['Departure'].astype(str)
    mews['Arrival'] = mews['Arrival'].astype(str)
    mews['Departure'] = mews['Departure'].astype(str)


    mews['Arrival'] = list(map(lambda x: x.split(' ')[0] if re.compile(
        r'(\d{4})-(\d+)-(\d+) *').match(x) else 'invalid format. use date as yyyy-mm-dd', mews['Arrival']))

    mews['Departure'] = list(map(lambda x: x.split(' ')[0] if re.compile(
        r'(\d{4})-(\d+)-(\d+) *').match(x) else 'invalid format. use date as yyyy-mm-dd', mews['Departure']))

    siteminder['Arrival'] = list(map(lambda x: x if re.compile(r'(\d{4})-(\d+)-(\d+)').match(x) else 'invalid format. use date as yyyy-mm-dd', siteminder['Arrival']))

    siteminder['Departure'] = list(map(lambda x: x if re.compile(r'(\d{4})-(\d+)-(\d+)').match(x) else 'invalid format. use date as yyyy-mm-dd', siteminder['Departure']))

    return mews, siteminder  # return the dataframe with the new date format


def verifyDateForExpedia(mews: pd.DataFrame, expedia: pd.DataFrame):
        
    # changing datatype, datadatetime to string
    expedia['Arrival'] = expedia['Arrival'].astype(str)
    expedia['Departure'] = expedia['Departure'].astype(str)
    mews['Arrival'] = mews['Arrival'].astype(str)
    mews['Departure'] = mews['Departure'].astype(str)

    # verify the date format
    mews['Arrival'] = list(map(lambda x: x.split(' ')[0] if re.compile(
        r'(\d{4})-(\d+)-(\d+) *').match(x) else 'invalid format. use date as yyyy-mm-dd', mews['Arrival']))

    mews['Departure'] = list(map(lambda x: x.split(' ')[0] if re.compile(
        r'(\d{4})-(\d+)-(\d+) *').match(x) else 'invalid format. use date as yyyy-mm-dd', mews['Departure']))

    expedia['Arrival'] = list(map(lambda x: x if re.compile(r'(\d{4})-(\d+)-(\d+)').match(x) else 'invalid format. use date as yyyy-mm-dd', expedia['Arrival']))

    expedia['Departure'] = list(map(lambda x: x if re.compile(r'(\d{4})-(\d+)-(\d+)').match(x) else 'invalid format. use date as yyyy-mm-dd', expedia['Departure']))

    return mews, expedia  # return the dataframe with the new date format