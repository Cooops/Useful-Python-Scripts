# Used as a template to both create and then insert db data into a table that has been dumped into a CSV.
CREATE TABLE active_products_historical(primary_ids SERIAL PRIMARY KEY, active_product_nick VARCHAR(255) NOT NULL, active_product_titles VARCHAR(255) NOT NULL, active_product_ids BIGSERIAL NOT NULL, active_product_prices FLOAT NOT NULL, active_product_cat_names VARCHAR(255) NOT NULL, active_product_cat_ids INT NOT NULL, active_product_img_thumb VARCHAR(255) NOT NULL, active_product_img_url VARCHAR(255) NOT NULL, active_product_lst_type VARCHAR(255) NOT NULL, active_product_watch_count INT NOT NULL, active_product_con VARCHAR(255) NOT NULL, active_product_loc VARCHAR(255) NOT NULL, active_product_start VARCHAR(255) NOT NULL, active_product_end VARCHAR(255) NOT NULL, active_product_depth INT NOT NULL, timestamp timestamp default current_timestamp);
COPY active_products(primary_ids, active_product_nick, active_product_titles, active_product_ids, active_product_prices, active_product_cat_names, active_product_cat_ids, active_product_img_thumb, active_product_img_url, active_product_lst_type, active_product_watch_count, active_product_con, active_product_loc, active_product_start, active_product_end, active_product_depth, timestamp)
FROM '/home/coopes/abupower/backup_csvs/active_products.csv' DELIMITER ',' CSV;