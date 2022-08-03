import pandas as pd
import os


def readFilesForBooking(mews: str, booking: str):

    if not os.path.exists(mews) or not os.path.exists(booking):
        return "File not found"

    # if user not fellow the instructions on the front-end, then it will throw an error
    try:
        if booking.split('.')[-1] == 'csv':
            booking = pd.read_csv(booking, usecols=[
                'Guest name', 'Final amount', 'Arrival', 'Departure'])
        else:
            booking = pd.read_excel(booking, usecols=[
                'Guest name', 'Final amount', 'Arrival', 'Departure'], sheet_name='Sheet1')

        if mews.split('.')[-1] == 'csv':
            mews = pd.read_csv(mews, usecols=['Last name', 'First name', 'Email',
                                              'Total amount', 'Arrival', 'Departure'])
        else:
            mews = pd.read_excel(mews, usecols=['Last name', 'First name', 'Email',
                                                'Total amount', 'Arrival', 'Departure', 'Identifier'], sheet_name='Reservations')
    except Exception as e:
        return 'Something want wrong!' + str(e)

    # merging first name and last name
    mews['Guest name'] = mews['First name'] + ' ' + mews['Last name']
    mews.drop(['First name', 'Last name'], axis=1, inplace=True)
    mews['Guest name'] = list(map(lambda x: str(x).lower(), mews['Guest name']))
    booking['Guest name'] = list(map(lambda x: str(x).lower(), booking['Guest name']))
    booking.rename(columns={'Final amount': 'Total amount'}, inplace=True)

    return mews, booking  # returning the dataframes


def readFilesForSiteminder(mews: str, siteminder: str):
    if not os.path.exists(mews) or not os.path.exists(siteminder):
        return "File not found"

    # if user not fellow the instructions on the front-end, then it will throw an error
    try:
        if siteminder.split('.')[-1] == 'csv':
            siteminder = pd.read_csv(siteminder, usecols=[
                'First name', 'Last name', 'E-mail', 'Check-in date', 'Check-out date', 'Subtotal amount'])
        else:
            siteminder = pd.read_excel(siteminder, usecols=[
                'First name', 'Last name', 'E-mail', 'Check-in date', 'Check-out date', 'Subtotal amount'])

        if mews.split('.')[-1] == 'csv':
            mews = pd.read_csv(mews, usecols=['Last name', 'First name', 'Email',
                                              'Total amount', 'Arrival', 'Departure'])
        else:
            mews = pd.read_excel(mews, usecols=['Last name', 'First name', 'Email',
                                                'Total amount', 'Arrival', 'Departure', 'Identifier'], sheet_name='Reservations')

    except Exception as e:
        return 'Something want wrong!' + str(e)

    siteminder.rename(columns={'E-mail': 'Email', 'Check-in date': 'Arrival',
                      'Check-out date': 'Departure', 'Subtotal amount': 'Total amount'}, inplace=True)

    mews['Last name'] = list(map(lambda x: str(x).lower(), mews['Last name']))
    siteminder['Last name'] = list(map(lambda x: str(x).lower(), siteminder['Last name']))
    mews['First name'] = list(map(lambda x: str(x).lower(), mews['First name']))
    siteminder['First name'] = list(map(lambda x: str(x).lower(), siteminder['First name']))
    siteminder['Total amount'] = siteminder['Total amount'].apply(int)
    mews['Total amount'] = mews['Total amount'].apply(int)
    return mews, siteminder  # returning the dataframes


def readFilesForExpedia(mews: str, expedia: str):
    if not os.path.exists(mews) or not os.path.exists(expedia):
        return "File not found"

    # if user not fellow the instructions on the front-end, then it will throw an error
    try:
        if expedia.split('.')[-1] == 'csv':
            expedia = pd.read_csv(
                expedia, usecols=['Guest', 'Check-in ', 'Check-out ', 'Reservation Amount'])
        else:
            expedia = pd.read_excel(
                expedia, usecols=['Guest', 'Check-in ', 'Check-out ', 'Reservation Amount'])

        if mews.split('.')[-1] == 'csv':
            mews = pd.read_csv(mews, usecols=['Last name', 'First name', 'Email',
                                              'Total amount', 'Arrival', 'Departure'])
        else:
            mews = pd.read_excel(mews, usecols=['Last name', 'First name', 'Email',
                                                'Total amount', 'Arrival', 'Departure', 'Identifier'], sheet_name='Reservations')
        
    except Exception as e:
        return 'Something want wrong! ' + str(e)
    
    # creating a new column for the guest name & removing the last name and first name
    mews['Guest'] = mews['First name'] + ' ' + mews['Last name']
    mews.drop(['First name', 'Last name'], axis=1, inplace=True)
    mews['Guest'] = list(map(lambda x: str(x).lower(), mews['Guest']))
    expedia['Guest'] = list(map(lambda x: str(x).lower(), expedia['Guest']))
    expedia.rename(columns={'Reservation Amount': 'Total amount',
                   'Check-in ': 'Arrival', 'Check-out ': 'Departure'}, inplace=True)

    mews['Total amount'] = mews['Total amount'].apply(int)
    expedia['Total amount'] = expedia['Total amount'].apply(int)

    return mews, expedia  # returning the dataframes