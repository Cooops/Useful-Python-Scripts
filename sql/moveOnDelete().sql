# Automatic PostgreSQL trigger to move rows-to-be-delete to a seperate, historical table to be backed up
CREATE FUNCTION moveDeleted() RETURNS trigger AS $$
    BEGIN
       INSERT INTO <your-historical-table-here> VALUES((OLD).*);
       RETURN OLD;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER moveDeleted
BEFORE DELETE ON <your-table-here>
FOR EACH ROW
EXECUTE PROCEDURE moveDeleted();

# Used to delete the function if need be
DROP FUNCTION moveDeleted() CASCADE;
