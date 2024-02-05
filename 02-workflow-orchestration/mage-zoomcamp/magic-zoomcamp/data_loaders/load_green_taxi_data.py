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

    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/'
    base_filename = 'green_tripdata_{0}-{1}.csv.gz'
    months = [10, 11, 12]
    year = '2020'

    taxi_dtypes = {
        '': pd.Int64Dtype(),  
        'passenger_count': pd.Int64Dtype(), 
        'trip_distance': float, 
        'RatecodeID': pd.Int64Dtype(), 
        'store_and_fwd_flag': str, 
        'PULocationID': pd.Int64Dtype(), 
        'DOLocationID': pd.Int64Dtype(), 
        'payment_type': pd.Int64Dtype(), 
        'fare_amount': float, 
        'extra': float, 
        'mta_tax': float, 
        'tip_amount': float, 
        'ehail_fee': float,
        'tolls_amount': float, 
        'improvement_surcharge': float,
        'total_amount': float, 
        'congestion_surcharge': float,
        'trip_type': pd.Int64Dtype()
    }

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    dfs = []

    for month in months:
        file_path = url+base_filename.format(year, month)
        print(f'Reading from {file_path}' )
        response = requests.get(file_path)
        result = pd.read_csv(io.BytesIO(response.content),compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
        dfs.append(result)


    return pd.concat(dfs)

# 266,855 rows x 20 columns

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
