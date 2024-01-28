#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine

def validate_table(engine, tablename, expected):
    print(f'Validating {tablename}...' )

    count_query = f"SELECT count(1) from {tablename};"
    expected = expected

    with engine.begin() as conn:
        result = pd.read_sql(count_query, con=conn)

    count = result.at[0, 'count']

    if count == expected:
        print(f'{tablename} Valid!')
        return 1
    else:
        print(f'Something went wrong with {tablename}. Expected: {expected} got: {count}')
        return 0        

def process_schema(engine, csv_file):
    df = pd.read_csv(csv_file)
    df.to_sql('zones', con=engine, index=False)


def process_ny_taxi_data(engine, db_name, csv_file):
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)
    df = next(df_iter)

    ######## Creates the table schema with no data
    ### converts pickup/dropoff fields into datetime(=timestamp)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    print(f'Effectively creating the table {db_name}')
    df.head(n=0).to_sql(name=db_name, con=engine, if_exists='replace')
    print(f'done creating the table {db_name}')

    query = f"""
    SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{db_name}';
    """

    with engine.begin() as conn:
        print(pd.read_sql(query, con=engine))

    df.to_sql(name=db_name, con=engine, index=True, if_exists='append')

    from time import time
    
    while True:
        t_start = time()
        df = next(df_iter)

        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.to_sql(name=db_name, con=engine, if_exists='append')

        t_end = time()


        print('inserted another chunk, took %.3f seconds ' %(t_end - t_start))

def main(params):

    taxi_csv = 'green-taxi-data.csv'
    zones_csv = 'zones.csv'

    db_name = params.table_name

    taxi_expected_count = 1369765
    green_taxi_expected_count = 449063

    zones_dbname = 'zones'
    zones_expected_count = 265

    zones_csv_url = 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'

    if(os.path.exists(zones_csv) == False):
        os.system(f"wget {zones_csv_url} -O {zones_csv}")

    #download CSV
    if(os.path.exists(taxi_csv) == False):
        os.system(f"wget {params.url} -O {taxi_csv}.gz")
        os.system(f"gzip -d *.gz > {taxi_csv}")
    
    engine = create_engine(f'postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}')

    if(validate_table(engine, db_name, green_taxi_expected_count)):
        print('Taxi Data already loaded into the database.')
    else:
        print('Taxi Data NOT FOUND. Loading it from CSV file...')
    process_ny_taxi_data(engine, db_name, taxi_csv)

    if(validate_table(engine, zones_dbname, zones_expected_count)):
        print('Zones data already loaded into the database.')
    else:
        print('Zones data not found in the database.')
        process_schema(engine, zones_csv)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres.')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='the name of the  database to write results to')
    parser.add_argument('--url', help='url of the CSV file')

    args = parser.parse_args()
    main(args)


# Usage:
# Make sure docker is up.
# > docker compose up
# IMPORTANT: postgres' name on docker-compose.yaml is host/path for pgadmin
# run script (or use the dockerfile.notuused thingy - overkill?)
# > python populate_db_pipeline.py \
#     --user=root \
#     --password=root \
#     --host=localhost \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=green_taxi \
#     --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"