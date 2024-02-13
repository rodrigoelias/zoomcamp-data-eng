if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd


@transformer
def transform(data, *args, **kwargs):
    """
         ---- --- -- -- - -- DOES NOT WORK --- - - -- - - - - - -

    My guess: BigQuery will define the Schema without taking into consideration whatever I do here
    """
    # Specify your transformation logic here
    print(data.dtypes)
    data.lpep_pickup_datetime = pd.to_datetime(data.lpep_pickup_datetime)
    data.lpep_dropoff_datetime = pd.to_datetime(data.lpep_dropoff_datetime)
    print(data.dtypes)
    return data
