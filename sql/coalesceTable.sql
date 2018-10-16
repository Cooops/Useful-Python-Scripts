# Used to re-align the primary_ids and their corresponding sequences. Usually run after the two values get out of place due to inserting data from a previously populate table into a brand new one.
-- What is the result?
SELECT MAX(primary_ids) FROM <your-table-here>;
-- Then run...
-- This should be higher than the last result.
SELECT nextval('<your-table-here>_primary_ids_seq');
-- If it's not higher... run this set the sequence last to your highest id. 
-- (wise to run a quick pg_dump first...)
BEGIN;
-- protect against concurrent inserts while you update the counter
LOCK TABLE <your-table-here> IN EXCLUSIVE MODE;
-- Update the sequence
SELECT setval('<your-table-here>_primary_ids_seq', COALESCE((SELECT MAX(primary_ids)+1 FROM <your-table-here>), 1), false);
COMMIT;
