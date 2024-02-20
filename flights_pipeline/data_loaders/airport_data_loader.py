import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://raw.githubusercontent.com/ip2location/ip2location-iata-icao/master/iata-icao.csv'
    response = requests.get(url)

    return pd.read_csv(io.StringIO(response.text), sep=',')
