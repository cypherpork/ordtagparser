ALTER TABLE inscr28 
DISABLE KEYS
	;
LOAD DATA INFILE '/Users/arrowhost/data/inscription_number_to_id.tsv' INTO TABLE inscr28 FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES  (
	ord_id,
	inscr_id,
        inscr_loc
	);
COMMIT;
ALTER TABLE inscr28 ENABLE KEYS;
