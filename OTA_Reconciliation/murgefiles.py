import pandas as pd
from datetime import datetime
from OTA_Reconciliation.readFiles import readFilesForBooking, readFilesForExpedia, readFilesForSiteminder
from OTA_Reconciliation.dateverification import verifyDateForBooking, verifyDateForExpedia, verifyDateForSitminder
from hashlib import md5


def getBookingTotalAmount(amount):
    if (amount != 'nan' and amount != 0):
        return (12/100)*amount + amount
    return 0


def generateHash(arrival, departure, guest: str, totalAmount):
    arrival = str(arrival)
    departure = str(departure)
    guest = str(guest)
    totalAmount = str(totalAmount)
    return md5((arrival + departure + guest + totalAmount).encode()).hexdigest()


# merging booking and mews df based on the Guest name, arrival, departure
def booking_mews_merge(mews: str, booking: str):

    mews_booking_df = readFilesForBooking(mews, booking)

    # if return type is string, then it means there is an error
    if type(mews_booking_df) == str:
        return mews_booking_df

    mews_booking_df = verifyDateForBooking(
        mews=mews_booking_df[0], booking=mews_booking_df[1])

    # booking doesn't have the gross amount, so we need to calculate it
    mews_booking_df[1]['Total amount'] = list(
        map(getBookingTotalAmount, mews_booking_df[1]['Total amount']))

    # genetation unique id for each row
    mews_booking_df[1]['id'] = list(map(generateHash, mews_booking_df[1]['Arrival'], mews_booking_df[1]['Departure'], mews_booking_df[1]['Guest name'], mews_booking_df[1]['Total amount']))
    mews_booking_df[0]['id'] = list(map(generateHash, mews_booking_df[0]['Arrival'], mews_booking_df[0]['Departure'], mews_booking_df[0]['Guest name'], mews_booking_df[0]['Total amount']))

    # merging mews and booking
    merged = pd.merge(mews_booking_df[0], mews_booking_df[1], on=['Guest name', 'Arrival', 'Departure'],
                      indicator=True, how='right', suffixes=('_mews', '_booking'))

    # calculating the difference between the mews & booking total amount
    merged['Difference'] = merged['Total amount_mews'] - \
        merged['Total amount_booking']

    # removing the rows with has diffrence value -1 to 1
    merged['Difference'] = merged['Difference'].apply(
        lambda x: 0 if (-1 <= x <= 1) else x)
    
    merged.drop_duplicates(inplace=True)
    rowWithZero = merged[merged['Difference'] == 0]
    merged.drop(rowWithZero.index, inplace=True)
    merged.reset_index(inplace=True)
    merged['_merge'] = list(map(lambda x: "Found in both Sheet" if x ==
                            'both' else 'Only found in Booking.com sheet', merged['_merge']))
    merged.rename({'_merge': 'Matched Side'}, axis=1, inplace=True)
    merged.index.rename('Index', inplace=True)
    merged.drop(columns=['index'], inplace=True)

    # generating the filename
    filename = datetime.strftime(
        datetime.now(), '%Y-%m-%d-%H-%M-%S') + '_booking.xlsx'
    # saving the file
    merged.to_excel(
        f'./static/generatedSheet/{filename}', sheet_name='Reconciliation')
    return filename


def expedia_mews_merge(mews: str, expedia: str):

    mews_expedia_df = readFilesForExpedia(mews, expedia)

    # if return type is string, then it means there is an error
    if type(mews_expedia_df) == str:
        return mews_expedia_df

    mews_expedia_df = verifyDateForExpedia(
        mews=mews_expedia_df[0], expedia=mews_expedia_df[1])

    #generating unique id for each row
    mews_expedia_df[1]['id'] = list(map(generateHash, mews_expedia_df[1]['Arrival'], mews_expedia_df[1]['Departure'], mews_expedia_df[1]['Guest'], mews_expedia_df[1]['Total amount']))
    mews_expedia_df[0]['id'] = list(map(generateHash, mews_expedia_df[0]['Arrival'], mews_expedia_df[0]['Departure'], mews_expedia_df[0]['Guest'], mews_expedia_df[0]['Total amount']))

    # merging mews and expedia
    merged = pd.merge(mews_expedia_df[0], mews_expedia_df[1], on=['Guest', 'Arrival', 'Departure'],
                      indicator=True, how='right', suffixes=('_mews', '_expedia'))

    # calculating the difference between the mews & expedia total amount
    merged['Difference'] = merged['Total amount_mews'] - \
        merged['Total amount_expedia']

    # removing the rows with has diffrence value -1 to 1
    merged['Difference'] = merged['Difference'].apply(
        lambda x: 0 if (-1 <= x <= 1) else x)

    merged.drop_duplicates(inplace=True)
    rowWithZero = merged[merged['Difference'] == 0]
    merged.drop(rowWithZero.index, inplace=True)
    merged.reset_index(inplace=True)
    merged['_merge'] = list(map(lambda x: "Found in both Sheet" if x ==
                            'both' else 'Only found in Expeida.com sheet', merged['_merge']))
    merged.rename({'_merge': 'Matched Side'}, axis=1, inplace=True)
    merged.index.rename('Index', inplace=True)
    merged.drop(columns=['index'], inplace=True)

    # generating the filename
    filename = datetime.strftime(
        datetime.now(), '%Y-%m-%d-%H-%M-%S') + '_expedia.xlsx'

    # saving the file
    merged.to_excel(
        f'./static/generatedSheet/{filename}', sheet_name='Reconciliation')
    return filename


def sitminder_mews_merge(mews: str, sitminder: str):

    mews_sitminder_df = readFilesForSiteminder(mews, sitminder)

    # if return type is string, then it means there is an error
    if type(mews_sitminder_df) == str:
        return mews_sitminder_df

    mews_sitminder_df = verifyDateForSitminder(
        mews=mews_sitminder_df[0], siteminder=mews_sitminder_df[1])

    # merging mews and sitminder
    merge1 = pd.merge(mews_sitminder_df[0][['Arrival', 'Departure', 'Last name', 'First name', 'Total amount', 'Identifier']], mews_sitminder_df[1][[
                      'Arrival', 'Departure', 'Last name', 'First name', 'Total amount']], on=['First name', 'Last name', 'Arrival', 'Departure'], how='right', suffixes=('_mews', '_siteminder'))


    merge2 = pd.merge(mews_sitminder_df[0][['Arrival', 'Departure', 'Email', 'Total amount', 'Identifier']], mews_sitminder_df[1][[
                      'Arrival', 'Departure', 'Email', 'Total amount']], on=['Email', 'Arrival', 'Departure'], how='right', suffixes=('_mews', '_siteminder'))

    # calculating the difference between the mews & sitminder total amount
    merge1['Difference'] = merge1['Total amount_mews'] - merge1['Total amount_siteminder']
    merge2['Difference'] = merge2['Total amount_mews'] - merge2['Total amount_siteminder']


    merged = pd.merge(merge1, merge2, on=['Arrival', 'Departure', 'Total amount_mews', 'Total amount_siteminder', 'Difference', 'Identifier'], how='outer')

    # removing the rows with has diffrence value -1 to 1
    merged['Difference'] = merged['Difference'].apply(
        lambda x: 0 if (-1 <= x <= 1) else x)
    
    rowWithZero = merged[merged['Difference'] == 0]
    merged.drop(rowWithZero.index, inplace=True)
    merged.index.rename('Index', inplace=True)
    merged.drop(columns=['index'], inplace=True)

    # remove duplicates
    merged.drop_duplicates(inplace=True)
    merged.reset_index(inplace=True)

    filename = datetime.strftime(
        datetime.now(), '%Y-%m-%d-%H-%M-%S') + '_siteminder.xlsx'
    merged.to_excel(
        f'./static/generatedSheet/{filename}', sheet_name='Reconciliation')
    return filename
