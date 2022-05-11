DELIMITER |
CREATE TRIGGER Trig
	BEFORE UPDATE ON  users
    FOR EACH ROW
    BEGIN 
		SET @total_restaurant_number = (SELECT count(*) 
        FROM users JOIN restaurants_comments USING(user_id) 
        WHERE user_id = new.user_id);
		
        SET @total_attraction_number = (SELECT count(*) 
        FROM users JOIN attractions_comments USING(user_id) 
        WHERE user_id = new.user_id);
		
		SET @total_accommodations_number = (SELECT count(*) 
        FROM users JOIN accommodations_comments USING(user_id) 
        WHERE user_id = new.user_id);
	
    IF (@total_restaurant_number+@total_attraction_number+
		@total_accommodations_number>2) THEN
        SET new.superstar = True;
	END IF;
        
END;
|
DELIMITER ;
