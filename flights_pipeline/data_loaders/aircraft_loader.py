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
    url = 'https://raw.githubusercontent.com/timrogers/iata-code-decoder-api/main/data/aircraft.json'
    response = requests.get(url)
    result = response.json()
    df = pd.DataFrame.from_records(result)
    print(df.info())
    return df
