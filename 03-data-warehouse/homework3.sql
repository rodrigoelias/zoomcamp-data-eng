-- gs://mage_dataset/2024/02/12/homework3.parquet
CREATE OR REPLACE EXTERNAL TABLE `tidy-agency-412105.mage_dataset.homework3`
OPTIONS (
  format = 'parquet',
  uris = ['gs://mage_dataset/2024/02/12/homework3.parquet']
);


SELECT count(distinct(PULocationID)) FROM `tidy-agency-412105.mage_dataset.homework3` ;
--  will process 0 B when run

SELECT count(distinct(PULocationID)) FROM `tidy-agency-412105.mage_dataset.homework3_native`
-- will process 6.41 MB when run


-- A: 0 MB for the External Table and 6.41MB for the Materialized Table


SELECT count(1) FROM `tidy-agency-412105.mage_dataset.homework3_native` where fare_amount = 0
-- 1622 (1,622)


CREATE OR REPLACE TABLE `tidy-agency-412105.mage_dataset.homework3_part`
PARTITION BY DATE(clean_lpep_dropoff_datetime)
CLUSTER BY PULocationID AS (
  SELECT *, TIMESTAMP_MICROS(CAST(lpep_dropoff_datetime / 1000 AS INT64)) as clean_lpep_dropoff_datetime FROM `tidy-agency-412105.mage_dataset.homework3_native`
);
-- 120Mb

-- NOTE TO SELF: Not really the same tables/structure anymore since I've added a new column to the partitioned table and I'm querying different fields
--  Hope its good enough for the homework.
SELECT DISTINCT PULocationID
FROM `tidy-agency-412105.mage_dataset.homework3_part`
WHERE clean_lpep_dropoff_datetime >= TIMESTAMP('2022-06-01')
  AND clean_lpep_dropoff_datetime <= TIMESTAMP('2022-06-30')
-- 1.12MB

SELECT DISTINCT PULocationID
FROM `tidy-agency-412105.mage_dataset.homework3_native`
WHERE lpep_dropoff_datetime >= UNIX_SECONDS(TIMESTAMP('2022-06-01'))
  AND lpep_dropoff_datetime <= UNIX_SECONDS(TIMESTAMP('2022-06-30'))
-- 12.82 MB
-- Yeah, it was good enough


SELECT count(*) FROM `tidy-agency-412105.mage_dataset.homework3_native`
-- 0MB
-- Making a primitive assumption: Number of Rows is a metadata to the table. Doesn't need to execute anything.
-- It's like an array datastructure containing a size/length property