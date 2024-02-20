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
    url = 'https://cdn.jsdelivr.net/gh/besrourms/airlines@latest/airlines.json'
    response = requests.get(url)
    result = response.json()
    # print(response.json())
    df = pd.DataFrame.from_records(result)
    return df
