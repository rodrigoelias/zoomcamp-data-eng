from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pyarrow as pa
from pyarrow.fs import GcsFileSystem
import pyarrow.parquet as pq
import os


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/personal-gcp.json"
bucket_name = 'mage_dataset'
project_id = 'tidy-agency-412105'

table_name = 'green_taxi'

root_path = f'{bucket_name}/{table_name}/lpep_pickup_date=*/*'


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """


    # data = parquet.ParquetDataset(files, filesystem=fs)
    # multiple_dates_df = data.read().to_pandas()


    # folders = gcs.get_file_info(root_path)

    # for file_name in files_in_folder:
    #     print(file_name)
        
        # for file_name in files_in_folder:
        #     gcs_blob_path = f"{gcs_prefix}/{folder_name}/{file_name}"

        #     # Read Parquet data directly from GCS
        #     parquet_data = read_parquet_from_gcs(gcs_bucket, f"{gcs_prefix}/{folder_name}", file_name)

        #     # Load Parquet data into BigQuery
        #     load_parquet_to_bigquery(parquet_data, bq_dataset, bq_table)


        # with gcs.open_input_stream(f"{bucket_name}/{green_taxi}") as fsrc:
        #     return pq.ParquetFile(fsrc).read_row_group()



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
