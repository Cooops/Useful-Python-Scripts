# Used to set an upper and lower bound range using a modified calculation using the average and standard deviations of any given column. 
# Useful when trying to find a range of outliers to remove from a dataset. The `1.5` an `50` variables are completely maleable.
WITH bounds as (
    SELECT (AVG(<your-float-column-here>) - STDDEV_SAMP(<your-float-column-here>) * 1.5) as lower_bound,
           (AVG(<your-float-column-here>) + STDDEV_SAMP(<your-float-column-here>) * 50) as upper_bound
    FROM <your-table-here>
	WHERE <your-indicator-column-here> = '<your-primary-ids or any-other-indicator-column-here>'
)
SELECT round(AVG(<your-float-column-here>)) as average
FROM <your-table-here>
WHERE <your-float-column-here> BETWEEN (SELECT lower_bound FROM bounds) AND (SELECT upper_bound FROM bounds)
