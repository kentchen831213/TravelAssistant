USE `travel_db`;
Drop PROCEDURE IF EXISTS PackageSearch;
DELIMITER |
CREATE PROCEDURE PackageSearch(IN varUser_id VARCHAR(255), IN varCity VARCHAR(255), 
					IN varAttractionType1 VARCHAR(255), IN varAttractionType2 VARCHAR(255), IN varAttractionType3 VARCHAR(255),
					IN varAccommodationMaxPrice INT, IN varAccommodationMinPrice INT, IN varAccommodationMinBeds INT, IN varAccommodationMaxBeds INT, 
                    IN varAccommodationMinBedroom INT, IN varAccommodationMaxBedroom INT, 
                    IN varRestaurantsPriceLevel VARCHAR(10),IN varRestaurantType VARCHAR(255),IN varRestaurantMinRating FLOAT,IN varRestaurantMaxRating FLOAT)

	BEGIN
    
		DECLARE cur_attraction_id INT;
        DECLARE cur_a_name VARCHAR(255);
        DECLARE cur_accommodations_id INT;
        DECLARE cur_ac_name VARCHAR(255);
        DECLARE cur_restaurants_id INT;
        DECLARE cur_r_name VARCHAR(255);
        
		DECLARE loop_exist_attractions BOOLEAN DEFAULT FALSE;
        DECLARE loop_exist_accommodations BOOLEAN DEFAULT FALSE;
        DECLARE loop_exist_restaurants BOOLEAN DEFAULT FALSE;
        
        DECLARE curAttractions CURSOR FOR (SELECT attraction_id, a_name 
								FROM attractions 
                                WHERE (category LIKE varAttractionType1 OR category LIKE varAttractionType2 OR category LIKE varAttractionType2) 
								AND city_name = varCity);
		
		DECLARE curAccommodations CURSOR FOR (SELECT accommodation_id, ac_name FROM accommodations 
							WHERE (price_level>=varAccommodationMinPrice AND price_level<=varAccommodationMaxPrice) 
								AND city_name = varCity 
                                AND (beds>=varAccommodationMinBeds AND beds<=varAccommodationMaxBeds)
                                AND (bedrooms>=varAccommodationMinBedroom AND bedrooms<=varAccommodationMaxBedroom));
                                
		DECLARE curRestaurants CURSOR FOR (SELECT restaurant_id, r_name FROM restaurants 
							WHERE (price_level LIKE varRestaurantsPriceLevel)
								AND category LIKE varRestaurantType
                                AND (avg_rating > varRestaurantMinRating AND avg_rating <= varRestaurantMaxRating));
		
        -- 
		DROP TABLE IF EXISTS PreferenceTable;
		CREATE TABLE PreferenceTable(
			preference_id INT PRIMARY KEY auto_increment, 
			user_id VARCHAR(255),
            spot_type VARCHAR(255),
			spot_id INT,
			spot_name VARCHAR(255));
		
        --
		OPEN curAttractions;
		BEGIN
			DECLARE CONTINUE handler FOR NOT FOUND SET loop_exist_attractions=TRUE;
			cloop:LOOP
				FETCH curAttractions INTO cur_attraction_id, cur_a_name;
				IF loop_exist_attractions THEN
					LEAVE cloop;
				END IF;
				
				INSERT INTO PreferenceTable (user_id, spot_type, spot_id, spot_name) VALUES(varUser_id, "attractions", cur_attraction_id, cur_a_name);
			END LOOP cloop;
		END;
        CLOSE curAttractions;
        
        --
		OPEN curAccommodations;
		BEGIN
			DECLARE CONTINUE handler FOR NOT FOUND SET loop_exist_accommodations=TRUE; 
			cloop:LOOP
				FETCH curAccommodations INTO cur_accommodations_id, cur_ac_name;
				IF loop_exist_accommodations THEN
					LEAVE cloop;
				END IF;
				
				INSERT INTO PreferenceTable (user_id, spot_type, spot_id, spot_name) VALUES(varUser_id, "accommodations", cur_accommodations_id, cur_ac_name);
			END LOOP cloop;
		END;
        CLOSE curAccommodations;       
        
        OPEN curRestaurants;
		BEGIN
			DECLARE CONTINUE handler FOR NOT FOUND SET loop_exist_restaurants=TRUE;
			cloop:LOOP
				FETCH curRestaurants INTO cur_restaurants_id, cur_r_name;
				IF loop_exist_restaurants THEN
					LEAVE cloop;
				END IF;
				
				INSERT INTO PreferenceTable (user_id, spot_type, spot_id, spot_name) VALUES(varUser_id, "restaurants", cur_restaurants_id, cur_r_name);
			END LOOP cloop;
		END;
        CLOSE curRestaurants; 
   END;
|
DELIMITER ;


-- CREATE PROCEDURE PackageSearch(IN varUser_id VARCHAR(255), IN varCity VARCHAR(255), 
-- 					IN varAttractionType1 VARCHAR(255), IN varAttractionType2 VARCHAR(255), IN varAttractionType3 VARCHAR(255),
-- 					IN varAccommodationMaxPrice INT, IN varAccommodationMinPrice INT, IN varAccommodationMinBeds INT, IN varAccommodationMaxBeds INT, 
--                     IN varAccommodationMinBedroom INT, IN varAccommodationMaxBedroom INT, 
--                     IN varRestaurantsPriceLevel VARCHAR(10),IN varRestaurantType VARCHAR(255),IN varRestaurantMinRating VARCHAR(255),IN varRestaurantMaxRating VARCHAR(255))

-- CALL PackageSearch('a15475', 'Chicago', 'museum', 'Nature', 'Park',
-- 					100, 78, 2, 6, 1, 2, '$$$', 'japanese', 0, 5);
-- SELECT * FROM PreferenceTable;



