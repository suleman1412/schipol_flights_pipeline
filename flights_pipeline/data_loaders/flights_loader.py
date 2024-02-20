
import pandas as pd
import requests
import re
import time
start = time.time()
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

headers = {
        "Accept": "application/json",
        "app_id": "209909bd",
        "app_key": "319a2568d3b0b765b33f8cbcc89f490c",
        "ResourceVersion": "v4",
    }

def acq_data(url):

    while url:
        print(url)
        response = requests.get(url, headers=headers,stream=True)
        if response.status_code != 200:
            return False
        links = re.findall(r"https[^<>]+",response.headers.get('link'))
        rel = re.findall(r'rel="([^"]\w*)',response.headers.get('link'))
        res = {rel[x]:links[x] for x in range(len(rel))}
        pages = re.findall(r"page=(\d*)",response.headers.get('link'))
        
        print(res)
        if 'last'in res:
            if 'next' in res:
                url = res['next']
            else:
                url = res['last']
        else:
            url = False
            
        json_raw = response.json()
        df = pd.json_normalize(json_raw['flights'])
        yield df
        




@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    flight_df = pd.DataFrame
    flight_url = "https://api.schiphol.nl/public-flights/flights?sort=%2BscheduleTime&page=1"


    
    flight_df = pd.concat(acq_data(flight_url))
    # Drop all empty columns here
    # flight_df.dropna(how='all', axis=1, inplace=True)
    
    #Drop irrelevant columns
    # flight_df.drop(
    #     [
    #     'aircraftRegistration', 
    #     'expectedSecurityFilter', 
    #     'flightNumber',
    #     'mainFlight',
    #     'prefixIATA',
    #     'prefixICAO', 
    #     'airlineCode',
    #     'schemaVersion',
    #     'aircraftType.iataMain',
    #     'aircraftType.iataSub',
    #     'codeshares.codeshares',
    #     'route.eu',
    #     'route.visa',
    #     'checkinAllocations.checkinAllocations'

    # ], axis=1,inplace=True)
    
    # Drop all incomplete rows here
    # flight_df.dropna(inplace=True)

    
    #Update Dtypes
    flight_df['lastUpdatedAt'] = pd.to_datetime(flight_df['lastUpdatedAt'])
    flight_df['estimatedLandingTime'] = pd.to_datetime(flight_df['estimatedLandingTime'])
    flight_df['expectedTimeBoarding'] = pd.to_datetime(flight_df['expectedTimeBoarding'])
    flight_df['expectedTimeGateClosing'] = pd.to_datetime(flight_df['expectedTimeGateClosing'])
    flight_df['expectedTimeGateOpen'] = pd.to_datetime(flight_df['expectedTimeGateOpen'])
    flight_df['scheduleDateTime'] = pd.to_datetime(flight_df['scheduleDateTime'])

    # print(flight_df.head())
    print(flight_df.info())
    
    end = time.time()
    print(end - start)
    return flight_df
 


 ###############################################
 #REFER ME.
 #for future suleman, need to consider rows with complete data and perform aggreagations 
 #(like which airline comes in the most, where does most fly to from schipol, average boarding time categorized by airlines and much more)
 



# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'
