# Used to extract the month and day from a timestamp by taking just the month and day part and casting them to VARCHAR characters.
SELECT to_char(to_timestamp (date_part('month', <your-timestamp-column-here>::date)::text, 'MM'), 'Month') as month, DATE_PART('day', <your-timestamp-column-here>::date) as day FROM <your-table-here>;
