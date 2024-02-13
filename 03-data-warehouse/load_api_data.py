import io
import pandas as pd
import pyarrow.parquet as pq
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

    months = [*range(1,13,1)]
    year = '2022'

    taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),  
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
        'tolls_amount': float, 
        'improvement_surcharge': float,
        'total_amount': float, 
        'congestion_surcharge': float
    }

    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    dfs = []
    

    for month in months:
        file_path = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet'
        print(f'Reading from {file_path}' )
        response = requests.get(file_path)
        # response.raise_for_status()
        data = io.BytesIO(response.content)
        
        df = pq.read_table(data).to_pandas()
        dfs.append(df)

    return pd.concat(dfs)

# Answer 1: 840402
