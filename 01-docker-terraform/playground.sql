SELECT count (1)
	FROM public.green_taxi
		WHERE lpep_pickup_datetime BETWEEN timestamp '2019-09-18 00:00:00' and timestamp '2019-09-18 23:59:59'
		and lpep_dropoff_datetime BETWEEN timestamp '2019-09-18 00:00:00' and timestamp '2019-09-18 23:59:59'
---15612
	
-- Which was the pick up day with the largest trip distance 
-- Use the pick up time for your calculations.
SELECT date(lpep_pickup_datetime)  from green_taxi
	where trip_distance = (select max(trip_distance) from green_taxi)
--"2019-09-26"
		
-- Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown
-- Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
-- magic numbers -> Unknown = 263 and 264. primitive. 
SELECT "Borough", sum(total_amount) as total
	FROM public.green_taxi
	INNER JOIN public.Zones ON "PULocationID" = "LocationID"
	WHERE lpep_pickup_datetime BETWEEN timestamp '2019-09-18 00:00:00' and timestamp '2019-09-18 23:59:59'
	AND "PULocationID" NOT IN (263, 264)
	GROUP BY "Borough"
	ORDER BY total DESC LIMIT 3
-- "Brooklyn"	96333.23999999919
-- "Manhattan"	91796.62999999849
-- "Queens"	78671.70999999919


-- For the passengers picked up in September 2019 in the zone name Astoria
-- which was the drop off zone that had the largest tip? 
-- We want the name of the zone, not the id.
SELECT Zones."Zone", max(tip_amount) as tips FROM public.green_taxi
INNER JOIN Zones ON "DOLocationID" = "LocationID"
WHERE lpep_pickup_datetime BETWEEN timestamp '2019-09-01 00:00:00' and timestamp '2019-09-30 23:59:59'
AND "PULocationID" = (SELECT "LocationID" from Zones where "Zone" = 'Astoria')
GROUP BY "DOLocationID", "Zone"
ORDER BY tips DESC LIMIT 1
-- "JFK Airport"	62.31