# CS411 PT1 - Stage 3

---
## Section 0. Database implementation
#### Database implementation on GCP SQL instance connected via MySQL workbench
The public ip address screenshot from GCP SQL instance 
![GCP_ip](https://media.github-dev.cs.illinois.edu/user/14619/files/46268c5a-0685-4dab-8d17-81d583f2a080)

Test connection successful screenshot from MySQL workbench while connecting to the GCP public ip
![MySQL_workbench_test_connection](https://media.github-dev.cs.illinois.edu/user/14619/files/a999142a-3fc7-4575-b982-f3b1e8a4be35)

---
## Section 1. Data Definition Language (DDL) commands
### Create the Schema
```sql
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema travel_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `travel_db`;
CREATE SCHEMA IF NOT EXISTS `travel_db` DEFAULT CHARACTER SET utf8 ;
USE `travel_db`;
```

### Create tables: city
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`city`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `city` ;

CREATE TABLE IF NOT EXISTS `city` (
  `city_name` VARCHAR(255) NOT NULL,
  `state` VARCHAR(255),
  `country` VARCHAR(255),
  `introduction` TEXT,
  `area` VARCHAR(255),
  `temperature` FLOAT,
  PRIMARY KEY (`city_name`)
);
```

### Create tables: attractions
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`attractions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `attractions` ;

CREATE TABLE IF NOT EXISTS `attractions` (
  `attraction_id` INT NOT NULL,
  `ranking` INT,
  `city_name` VARCHAR(255) NULL,
  `a_name` VARCHAR(255),
  `categories` VARCHAR(255),
  `a_address` TEXT,
  `latitude` FLOAT,
  `longitude` FLOAT,
  PRIMARY KEY (`attraction_id`),
  FOREIGN KEY (`city_name`) REFERENCES `city`(`city_name`)
  ON DELETE SET NULL
  ON UPDATE CASCADE
);
```

### Create tables: laundry
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`laundry`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `laundry` ;

CREATE TABLE IF NOT EXISTS `Laundry` (
  `laundry_id` INT NOT NULL,
  `l_name` VARCHAR(255),
  `city_name` VARCHAR(255) NULL,
  `service_type` VARCHAR(255),
  `l_address` VARCHAR(255),
  `price_range` VARCHAR(5),
  `latitude` FLOAT,
  `longitude` FLOAT,
  PRIMARY KEY (`laundry_id`),
  FOREIGN KEY (`city_name`) REFERENCES `city`(`city_name`)
  ON DELETE CASCADE
);
```

### Create tables: markets
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`markets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `markets` ;

CREATE TABLE IF NOT EXISTS `markets` (
  `market_id` INT NOT NULL,
  `city_name` VARCHAR(255) NOT NULL,
  `m_name` VARCHAR(255),
  `avg_rating` FLOAT,
  `m_address` VARCHAR(255),
  `latitude` FLOAT,
  `longitude` FLOAT,
  PRIMARY KEY (`market_id`),
  FOREIGN KEY (`city_name`) REFERENCES `city`(`city_name`)
  ON DELETE CASCADE
);
```

### Create tables: users
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `users` ;

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `gender` VARCHAR(255) NULL,
  `email` VARCHAR(255) NOT NULL,
  `phone` CHAR(12) NOT NULL,
  `city` VARCHAR(255) NOT NULL,
  `birth_date` DATE NOT NULL,
  PRIMARY KEY (`user_id`)
);
```

### Create tables: preference
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`preference`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `preference` ;

CREATE TABLE IF NOT EXISTS `preference` (
  `Users_user_id` VARCHAR(255) NOT NULL,
  `outdoor_love_type` VARCHAR(255) NOT NULL,
  `food_preference` VARCHAR(255) NOT NULL,
  `budget_type` VARCHAR(255) NOT NULL,
  `art_type` VARCHAR(255) NOT NULL,
  `museum_type` VARCHAR(255) NOT NULL,
  `city_trip_type` VARCHAR(255) NOT NULL,
  `transportation_type` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  FOREIGN KEY (`_user_id`) REFERENCES `users`(`user_id`)
);
```

### Create tables: restaurants
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`restaurants`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `restaurants` ;

CREATE TABLE IF NOT EXISTS `restaurants` (
  `restaurant_id` INT NOT NULL AUTO_INCREMENT,
  `r_name` VARCHAR(255),
  `category` VARCHAR(255),
  `city_name` VARCHAR(255) NOT NULL,
  `latitude` FLOAT,
  `longitude` FLOAT,
  `avg_rating` FLOAT,
  `review` TEXT,
  `r_address` VARCHAR(255),
  `description` TEXT,
  `price_level` VARCHAR(255),
  PRIMARY KEY (`restaurant_id`),
  FOREIGN KEY (`city_name`) REFERENCES `city`(`city_name`)
);
```

### Create tables: accommodations
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`accommodations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `accommodations` ;

CREATE TABLE IF NOT EXISTS `accommodations` (
  `accommodation_id` INT NOT NULL,
  `ac_name` VARCHAR(255) NOT NULL,
  `county` VARCHAR(255) NULL,
  `city_name` VARCHAR(255) NOT NULL,
  `latitude` FLOAT,
  `longitude` FLOAT,
  `avg_rating` FLOAT,
  `price_level` VARCHAR(5),
  `type` VARCHAR(255),
  `bathroom` VARCHAR(45),
  `bedrooms` INT,
  `beds` INT,
  PRIMARY KEY (`accommodation_id`),
  FOREIGN KEY (`city_name`) REFERENCES `city`(`city_name`)
);
```

### Create tables: restaurants_comments
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`restaurants_comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `restaurants_comments` ;

CREATE TABLE IF NOT EXISTS `restaurants_comments` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL,
  `restaurant_id` INT NOT NULL,
  `comment_date` DATE,
  `rating` FLOAT,
  `comment` TEXT,
  `comment_likes` INT,
  PRIMARY KEY (`comment_id`, `user_id`, `restaurant_id`),
  FOREIGN KEY (`user_id`) REFERENCES `rsers`(`user_id`),
  FOREIGN KEY (`restaurant_id`)REFERENCES `restaurants`(`restaurant_id`)
);
```

### Create tables: accommodations_comments
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`accommodations_comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `accommodations_comments` ;

CREATE TABLE IF NOT EXISTS `accommodations_comments` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL,
  `accommodation_id` INT NOT NULL,
  `comment_date` DATE,
  `rating` FLOAT,
  `comment` TEXT,
  `comment_likes` INT,
  PRIMARY KEY (`comment_id`, `user_id`, `accommodation_id`),
  FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`),
  FOREIGN KEY (`accommodation_id`) REFERENCES `accommodations`(`accommodation_id`)
);
```

### Create tables: attractions_comments
```sql
-- -----------------------------------------------------
-- Table `travel_db`.`attractions_comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `attractions_comments` ;

CREATE TABLE IF NOT EXISTS `attractions_comments` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL,
  `attraction_id` INT NOT NULL,
  `comment_date` DATE,
  `rating` FLOAT,
  `comment` TEXT,
  `comment_likes` INT,
  PRIMARY KEY (`comment_id`, `user_id`, `attraction_id`),
  FOREIGN KEY (`attraction_id`) REFERENCES `attractions` (`attraction_id`)
);
```
---

## Section 2. Insert Data
### Example inserting for each table available
#### We only have 2 variation interms of syntax, the major difference is whether the auto increment keys are activated in the table. Few rows are provided here:

#### city table
```sql
INSERT INTO city VALUES
('Chicago','Illinois','USA',"officially the City of Chicago, is the most populous city in the U.S. state of Illinois, and the third-most populous city in the United States, following New York City and Los Angeles. With a population of 2,746,388 in the 2020 census,[4] it is also the most populous city in the Midwestern United States and the fifth most populous city in North America. Chicago is the county seat of Cook County, the second most populous county in the U.S., while a small portion of the city's O'Hare Airport also extends into DuPage County. Chicago is the principal city of the Chicago metropolitan area, defined as either the U.S. Census Bureau's metropolitan statistical area (9.6 million people) or the combined statistical area (almost 10 million residents), often called Chicagoland. It is one of the 40 largest urban areas in the world.",'234.53 sq mi',52);
```

#### attractions table
```sql
INSERT INTO attractions VALUES
(1,24173,'Chicago','The Art Institute of Chicago','museum','The Art Institute of Chicago, 111, South Michigan Avenue, Printers Row, Loop, Chicago, Cook County, Illinois, 60603, United States',41.8796009,-87.623082804204);
```

#### laundry table
```sql
INSERT INTO laundry VALUES
(1,'Alex Cleaners','Austin','Laundry Services','2110 Pecan St W',NULL,30.2732081,-97.758429),
(2,'EZ Care Cleaners','Austin','Dry Cleaning',NULL,NULL,NULL,NULL);
```

#### market table
```sql
INSERT INTO markets VALUES
(1,'Chicago','DAW Trading',5,'141 W Jackson Blvd # 1531A',41.8781829,-87.6287514),
(2,'Chicago','Cleos Southern Cuisine',4,'916 W Fulton Market',41.8869631,-87.6505461);
```

#### user table
```sql
INSERT INTO users VALUES
('yycc11','weneeds','John','Trump','Male','yycc1@gmail.com','423-739-2384','Chicago','1982-04-18'),
('yycc22','omejobst','Tom','Caesar','Male','yycc2@gmail.com','879-655-9877','New York','1986-03-17');
```

#### restaurant table
#### This is one on the table using auto-incremneting key. Thus we need to specify the column for inserting data rows.
```sql
INSERT INTO restaurants (r_name, category, city_name, latitude, longitude,avg_rating,review,r_address,description,price_level) VALUES ('Bertuccis Italian Restaurant','Italian restaurant','Boston',NULL,NULL,3.9,400,'799 Main St','NULL','$$');
INSERT INTO restaurants (r_name, category, city_name, latitude, longitude,avg_rating,review,r_address,description,price_level) VALUES ('The Oceanaire Seafood Room','Fine dining restaurant','Boston',42.3590304,-71.0591935,4.4,802,'40 Court St','NULL','$$$$');
```

#### accommodation table
```sql
INSERT INTO accommodations VALUES
(1,'Hyde Park - Walk to University of Chicago','Hyde Park','Chicago',41.7879,-87.5878,4.99,95,1,'1 shared bath',1,1),
(2,'Tiny Studio Apartment 94 Walk Score','Ukrainian Village','Chicago',41.90166,-87.68021,4.67,65,2,'1 bath',1,1);

```

#### restaurants_comments table
```sql
INSERT INTO restaurants_comments (user_id, restaurant_id, comment_date, rating, comment, comment_likes) VALUES ('eu25190',377,'2019-02-20',5,'THE BEST RESTAURANT IN CHICAGO. Period. We love sushi and this is the only place that has ever gotten us to not order it and instead only get the special things on the menu. THATs how good it all is. The brothers have crafted the simplest, most delicious bites that its a waste to order anything else.',2);
```

#### accommodations_comments table
```sql
INSERT INTO accommodations_comments (user_id, accommodation_id, comment_date, rating, comment, comment_likes) VALUES ('vitae1580',4329,'2019-02-20',5,'If you are needing to go to Chicago and find adequate lodging at an affordable rate this is the apartment for you. Everything was as stated in the description and pictures. The host is very responsive. This neighborhood is ok if you are just here to sleep and go about your day. Overall a really great experience at a great price. The unit is warm and accommodating. I would definitely rent this spot again.',2);
INSERT INTO accommodations_comments (user_id, accommodation_id, comment_date, rating, comment, comment_likes) VALUES ('luctus0123',3735,'2017-10-15',5,'It was exactly as listed ! Perfect, quiet , clean, & an amazing value for the area and proximity to downtown !',3);
```

#### attractions_comments table
```sql
INSERT INTO attractions_comments (user_id, attraction_id, comment_date, rating, comment, comment_likes) VALUES ('elementum23143',1,'2020-09-16',5,'Still great food; Havent been here for nearly 18 months as we often dined here once a week at least. The food is still very good and service also.; Jolsha',1);
INSERT INTO attractions_comments (user_id, attraction_id, comment_date, rating, comment, comment_likes) VALUES ('vitae3832',2,'2021-12-09',4,'Very good !; We stayed here before flight as we had booked business class seats with AER Lingus. It is ideally situated and offers everything from champagne to cooked break...; Escape Lounge - T2',41);
```

---

### The result after inserting
#### city
```sql
SELECT COUNT(*) FROM city;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/442c4f71-1d6a-427a-886f-791d30cf00c1">

#### attractions
```sql
SELECT COUNT(*) FROM attractions;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/a135a0d9-8ca2-4d42-9266-70bc7113f3f7">

#### laundry
```sql
SELECT COUNT(*) FROM laundry;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/38730c1a-52b2-4b5d-b574-452c9f1dabad">

#### markets
```sql
SELECT COUNT(*) FROM markets;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/d9163ab5-68b4-4999-b184-1ace540df4fb">

#### users
```sql
SELECT COUNT(*) FROM users;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/3a2ffd22-2780-404b-8c90-eab6129355d5">

#### restaurants
```sql
SELECT COUNT(*) FROM restaurants;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/3df71b7a-366a-423d-80b3-3cd90d0f7581">

#### accommodations
```sql
SELECT COUNT(*) FROM accommodations;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/567f18fd-7a48-406a-8b8f-af4c1ece6f50">

#### restaurants_comments
```sql
SELECT COUNT(*) FROM restaurants_comments;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/4fba433b-de6b-406d-96c0-3c75033b305a">

#### accommodations_comments
```sql
SELECT COUNT(*) FROM accommodations_comments;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/4eb795bf-734d-45d1-8541-a37faa9ff93f">

#### attractions_comments
```sql
SELECT COUNT(*) FROM attractions_comments;
```
<img width="80" alt="image" src="https://media.github-dev.cs.illinois.edu/user/14617/files/1da161e8-800f-4bb4-8cc3-15691bf17b9a">

---

## Section 3. Two Advanced SQL Queries
### First query
#### Choose the neighborhood market and laundry for the specific accommodation
```sql
SELECT *
FROM (
        (SELECT ac_name, m_name as name, 'market' as type, SQRT(power((ac.latitude - m.latitude), 2) + power((ac.longitude - m.longitude), 2)) * 100 AS approximate_distance
        FROM markets m JOIN accommodations ac USING(city_name)
        WHERE SQRT(power((ac.latitude - m.latitude), 2) + power((ac.longitude - m.longitude), 2)) * 100 < 5 
        AND m.latitude IS NOT NULL AND m.longitude IS NOT NULL AND ac_name = 'Tiny Studio Apartment 94 Walk Score')
        UNION
        (SELECT ac_name, l_name as name, 'laundry' as type, SQRT(power((ac.latitude - l.latitude), 2) + power((ac.longitude - l.longitude), 2)) * 100 AS approximate_distance
        FROM laundry l JOIN accommodations ac USING(city_name)
        WHERE SQRT(power((ac.latitude - l.latitude), 2) + power((ac.longitude - l.longitude), 2)) * 100 < 5 AND 
        l.latitude IS NOT NULL AND l.longitude IS NOT NULL AND ac_name = 'Tiny Studio Apartment 94 Walk Score')
	) AS temp
ORDER BY approximate_distance
LIMIT 15;
```
![first_advanced_query_result](https://media.github-dev.cs.illinois.edu/user/14613/files/6c97e1e1-c79d-4d04-93e5-695a323d0e5c)

In this question, our system provides a function which informed the travelers where are the nearest laundries and markets in the neiborhood of their accomodation. We defined the neiborhood by the approximate distance calculated by the coordinates from stores to the accomodation, which should less than 5 kilometers. The query will perform the selection for supermarkets and laundries seperately. Then finally, we will join the result and perform to the user.

In this case, a user lived in 'Tiny Studio Apartment 94 Walk Score', and our system will present the nearest markets and laundries to that user.

---

### Second query
#### Choose the specific category restaurant for the specific type of attractions and accommodations
```sql
SELECT a.a_name, r.r_name,
       SQRT(power((ac.latitude - a.latitude), 2) + power((ac.longitude - a.longitude), 2)) * 100 AS ac_a_distance,
       SQRT(power((a.latitude - r.latitude), 2) + power((a.longitude - r.longitude), 2)) * 100 AS a_r_distance
FROM attractions a JOIN accommodations ac USING (city_name) JOIN restaurants r USING (city_name)
WHERE ac_name = 'Tiny Studio Apartment 94 Walk Score' AND
     (a.categories LIKE '%Museum%' OR a.categories LIKE '%museum%') AND
     SQRT(power((a.latitude - r.latitude), 2) + power((a.longitude - r.longitude), 2)) * 100 < 1 AND
     r.restaurant_id IN (SELECT r.restaurant_id
                         FROM restaurants_comments rm JOIN restaurants r ON r.restaurant_id = rm.restaurant_id
                         WHERE r.city_name = 'Chicago' AND r.category = 'American'
                         GROUP BY rm.restaurant_id
                         HAVING COUNT(rm.restaurant_id) > 0)
ORDER BY ac_a_distance, r.r_name DESC
LIMIT 15;
```
![second_advanced_query_result](https://media.github-dev.cs.illinois.edu/user/14613/files/27d75209-ea8c-4ee9-93dd-94704ff490fb)

In this question, we can imagine a scenario for a user who wants to visit a specific type of attraction, and our system will generate those attractions in that type. Also, our system will recommend the restaurants the users preferred at the same time for each tourist attraction. We also yield the approximate distance between attractions and the distance between attractions and restaurants.

In this case, the user lived in the accommodation named 'Tiny Studio Apartment 94 Walk Score' (we know it is in Chicago), and the user would like to visit the museum. Also, the user enjoyed the restaurant "American" type for cuisine. The system will automatically generate a list of attractions with American types of restaurants.

---
## Section 4. Indexing

### First query: Choose the neighborhood market and laundry for the specific accommodation
<!---
- Original(not add any index)
Before add the index, it need about 3369 ms to execute the query
![query_1_original_gcp](https://media.github-dev.cs.illinois.edu/user/14613/files/9edc561f-0d08-4b85-a770-796737c05050)

- Original(not add any index) and without "limit"
Before add the index and without "limit", it need about 0.011 ms to execute the query
![query_1_explain_analyze_ac_idx_no_limit_orderBy_gcp](https://media.github-dev.cs.illinois.edu/user/14613/files/04ce5091-b2ba-4e4c-94d0-d0167b226581)


- add the restaurant as index
After add the restaurant as the index and without "limit", it need about 3321 ms to execute the query
![query_1_explain_analyze_with_midx](https://media.github-dev.cs.illinois.edu/user/14613/files/fa7a6523-ad2f-4613-8005-35d5f716c3ac)

Based on our analyzing, indexing did improve the query speed in certain conditions. For example, when we included the query without Limit clause. The query
efficiency was improved drastically. But when we included the Limit clause, the efficiency brought by indexing was significantly impacted by having Limit clause included.
--->

We try indexing on `accommodations.accommodation_id`, `laundry.city_name`, `accommodations.latitude`,  `accommodations.longitude`, and `accommodations.ac_name`. The result suggested that only the index for `accommodations.ac_name` had significant effect on the cost, which involved in a searching process for the accommodations' names.

#### query 1 without indexing
```
-> Limit: 15 row(s)  (cost=1456.89..1456.89 rows=15) (actual time=12.931..12.934 rows=15 loops=1)
    -> Sort: temp.approximate_distance, limit input to 15 row(s) per chunk  (cost=1456.89..1456.89 rows=797) (actual time=12.930..12.932 rows=15 loops=1)
        -> Table scan on temp  (cost=92.05 rows=796) (actual time=0.002..0.021 rows=163 loops=1)
            -> Union materialize with deduplication  (cost=1456.89..1456.89 rows=797) (actual time=12.836..12.866 rows=163 loops=1)
                -> Nested loop inner join  (cost=688.59 rows=399) (actual time=3.881..8.764 rows=86 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=1.309..5.633 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=1.303..4.981 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - m.latitude),2) + pow((ac.longitude - m.longitude),2))) * 100) < 5) and (m.latitude is not null) and (m.longitude is not null))  (cost=0.25 rows=1) (actual time=2.568..3.117 rows=86 loops=1)
                        -> Index lookup on m using city_name (city_name=ac.city_name)  (cost=0.25 rows=1) (actual time=2.548..2.990 rows=236 loops=1)
                -> Nested loop inner join  (cost=688.59 rows=399) (actual time=0.343..3.535 rows=77 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.063..2.795 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.062..2.367 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - l.latitude),2) + pow((ac.longitude - l.longitude),2))) * 100) < 5) and (l.latitude is not null) and (l.longitude is not null))  (cost=0.25 rows=1) (actual time=0.279..0.733 rows=77 loops=1)
                        -> Index lookup on l using city_name (city_name=ac.city_name)  (cost=0.25 rows=1) (actual time=0.263..0.629 rows=261 loops=1)
```

#### index_acc_id: add index on accommodations.accommodation_id
```
-> Limit: 15 row(s)  (cost=1456.89..1456.89 rows=15) (actual time=6.970..6.973 rows=15 loops=1)
    -> Sort: temp.approximate_distance, limit input to 15 row(s) per chunk  (cost=1456.89..1456.89 rows=797) (actual time=6.969..6.971 rows=15 loops=1)
        -> Table scan on temp  (cost=92.05 rows=796) (actual time=0.002..0.022 rows=163 loops=1)
            -> Union materialize with deduplication  (cost=1456.89..1456.89 rows=797) (actual time=6.876..6.907 rows=163 loops=1)
                -> Nested loop inner join  (cost=688.59 rows=399) (actual time=0.128..3.282 rows=86 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.085..2.853 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.080..2.405 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - m.latitude),2) + pow((ac.longitude - m.longitude),2))) * 100) < 5) and (m.latitude is not null) and (m.longitude is not null))  (cost=0.25 rows=1) (actual time=0.042..0.421 rows=86 loops=1)
                        -> Index lookup on m using city_name (city_name=ac.city_name)  (cost=0.25 rows=1) (actual time=0.036..0.347 rows=236 loops=1)
                -> Nested loop inner join  (cost=688.59 rows=399) (actual time=0.138..3.343 rows=77 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.098..2.875 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.097..2.437 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - l.latitude),2) + pow((ac.longitude - l.longitude),2))) * 100) < 5) and (l.latitude is not null) and (l.longitude is not null))  (cost=0.25 rows=1) (actual time=0.039..0.462 rows=77 loops=1)
                        -> Index lookup on l using city_name (city_name=ac.city_name)  (cost=0.25 rows=1) (actual time=0.032..0.385 rows=261 loops=1)
```
This index was not used in the execution.

### index_lan_city: add index on laundry.city_name
```
-> Limit: 15 row(s)  (cost=21548.25..21548.25 rows=15) (actual time=14.543..14.547 rows=15 loops=1)
    -> Sort: temp.approximate_distance, limit input to 15 row(s) per chunk  (cost=21548.25..21548.25 rows=78046) (actual time=14.542..14.545 rows=15 loops=1)
        -> Table scan on temp  (cost=8782.56 rows=78045) (actual time=0.003..0.034 rows=163 loops=1)
            -> Union materialize with deduplication  (cost=21548.25..21548.25 rows=78046) (actual time=14.412..14.460 rows=163 loops=1)
                -> Nested loop inner join  (cost=688.59 rows=399) (actual time=0.245..7.554 rows=86 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.141..6.552 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.133..5.666 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - m.latitude),2) + pow((ac.longitude - m.longitude),2))) * 100) < 5) and (m.latitude is not null) and (m.longitude is not null))  (cost=0.25 rows=1) (actual time=0.103..0.986 rows=86 loops=1)
                        -> Index lookup on m using city_name (city_name=ac.city_name)  (cost=0.25 rows=1) (actual time=0.092..0.825 rows=236 loops=1)
                -> Nested loop inner join  (cost=13055.06 rows=77647) (actual time=1.543..6.329 rows=77 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=1.003..5.238 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=1.000..4.580 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - l.latitude),2) + pow((ac.longitude - l.longitude),2))) * 100) < 5) and (l.latitude is not null) and (l.longitude is not null))  (cost=6.03 rows=158) (actual time=0.538..1.082 rows=77 loops=1)
                        -> Index lookup on l using index_lan_city (city_name=ac.city_name)  (cost=6.03 rows=195) (actual time=0.525..0.961 rows=261 loops=1)
```
The index was used for looking up the city name for the laundry table when joining laundry and accommodations tables. However, there is no significant effect on the execution time cost, and the reason might be that the city name is a foreign key to the city table. It automatically applied indexing in My SQL, and there is no additional effect when adding this index.

### index_acc_lat and index_acc_lon: add index on accommodations.latitude and accommodations.longitude
```
-> Limit: 15 row(s)  (cost=21548.25..21548.25 rows=15) (actual time=9.829..9.832 rows=15 loops=1)
    -> Sort: temp.approximate_distance, limit input to 15 row(s) per chunk  (cost=21548.25..21548.25 rows=78046) (actual time=9.828..9.830 rows=15 loops=1)
        -> Table scan on temp  (cost=8782.56 rows=78045) (actual time=0.002..0.021 rows=163 loops=1)
            -> Union materialize with deduplication  (cost=21548.25..21548.25 rows=78046) (actual time=9.741..9.771 rows=163 loops=1)
                -> Nested loop inner join  (cost=688.59 rows=399) (actual time=0.188..6.020 rows=86 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.098..5.160 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.092..4.393 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - m.latitude),2) + pow((ac.longitude - m.longitude),2))) * 100) < 5) and (m.latitude is not null) and (m.longitude is not null))  (cost=0.25 rows=1) (actual time=0.087..0.845 rows=86 loops=1)
                        -> Index lookup on m using city_name (city_name=ac.city_name)  (cost=0.25 rows=1) (actual time=0.078..0.693 rows=236 loops=1)
                -> Nested loop inner join  (cost=13055.06 rows=77647) (actual time=0.218..3.304 rows=77 loops=1)
                    -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.062..2.791 rows=1 loops=1)
                        -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.060..2.365 rows=4989 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - l.latitude),2) + pow((ac.longitude - l.longitude),2))) * 100) < 5) and (l.latitude is not null) and (l.longitude is not null))  (cost=6.03 rows=158) (actual time=0.156..0.506 rows=77 loops=1)
                        -> Index lookup on l using index_lan_city (city_name=ac.city_name)  (cost=6.03 rows=195) (actual time=0.146..0.426 rows=261 loops=1)
```
We tried to apply an index on latitude and longitude for table accommodations since the report suggested that several parts are using these two attributes for searching. However, the indexes were not used in the execution. The reason might be that we used the `WHERE` statement with calculation for these two attributes, and the index would have no effect in this situation. 

### index_acc_name: add index on accommodations.ac_name
```
-> Limit: 15 row(s)  (cost=42.39..42.39 rows=15) (actual time=1.248..1.251 rows=15 loops=1)
    -> Sort: temp.approximate_distance, limit input to 15 row(s) per chunk  (cost=42.39..42.39 rows=159) (actual time=1.247..1.249 rows=15 loops=1)
        -> Table scan on temp  (cost=20.39 rows=159) (actual time=0.001..0.021 rows=163 loops=1)
            -> Union materialize with deduplication  (cost=42.39..42.39 rows=159) (actual time=1.169..1.199 rows=163 loops=1)
                -> Nested loop inner join  (cost=0.70 rows=1) (actual time=0.078..0.461 rows=86 loops=1)
                    -> Index lookup on ac using index_acc_name (ac_name='Tiny Studio Apartment 94 Walk Score')  (cost=0.35 rows=1) (actual time=0.046..0.047 rows=1 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - m.latitude),2) + pow((ac.longitude - m.longitude),2))) * 100) < 5) and (m.latitude is not null) and (m.longitude is not null))  (cost=0.33 rows=1) (actual time=0.030..0.406 rows=86 loops=1)
                        -> Index lookup on m using city_name (city_name=ac.city_name)  (cost=0.33 rows=1) (actual time=0.023..0.329 rows=236 loops=1)
                -> Nested loop inner join  (cost=25.83 rows=158) (actual time=0.101..0.468 rows=77 loops=1)
                    -> Index lookup on ac using index_acc_name (ac_name='Tiny Studio Apartment 94 Walk Score')  (cost=0.35 rows=1) (actual time=0.008..0.009 rows=1 loops=1)
                    -> Filter: (((sqrt((pow((ac.latitude - l.latitude),2) + pow((ac.longitude - l.longitude),2))) * 100) < 5) and (l.latitude is not null) and (l.longitude is not null))  (cost=21.78 rows=158) (actual time=0.093..0.453 rows=77 loops=1)
                        -> Index lookup on l using index_lan_city (city_name=ac.city_name)  (cost=21.78 rows=195) (actual time=0.088..0.379 rows=261 loops=1)
```

Finally, we tried indexing on the `accommodations.ac_name` since we required a searching process for the accommodations' name in the query. The report suggested that the index has a significant effect. The total cost time was reduced from 9.8 ms to 1.2 ms, and for the searching process, the cost was reduced from 516.35 to 0.35 and time reduced from 0.098 to 0.046 per sub execution. 

---
### Second query: Choose the specific category restaurant for the specific type of attractions and accommodations
<!---
-  Original(not add any index)
Before add the index, it need about 20 ms to execute the query
![query_2_explain_analyze_original](https://media.github-dev.cs.illinois.edu/user/14613/files/20849b05-2942-4e10-a717-d55d1ba7c7e0)

- add the restaurant as index
After ad the restaurant as the index, it need about 20ms to execute the query
![query_2_explain_analyze_restaurant_idx](https://media.github-dev.cs.illinois.edu/user/14613/files/16bde74a-734b-4f8f-90bf-e644018a77c1)

- add the attraction and restaurant as index
After add the accommodation and restaurant as index, it need about 20ms to execute the query
![query_2_explain_analyze_with_res_idx+att_idx](https://media.github-dev.cs.illinois.edu/user/14613/files/4ed9e394-2997-442c-83b4-02009eed2d27)
- add the attraction, restaurant, and accommodation as index
After add the accommodation,restaurant, and attraction as index, it need about 20ms to execute the query
![query_2_explain_analyze_with_res_att_acco_idx](https://media.github-dev.cs.illinois.edu/user/14613/files/343ae712-482f-4d08-b2d6-30f7af1462cb)
--->

We try several indexing on `restaurants_comments.restaurant_id`, `restaurants.category`, `accommodations.ac_name`, and `attractions.categories`. We can find out the query used these indexes when filtering or searching, and the results in some executing sections have significant change after the implementation. We can find out that the time cost was reduced from about 7ms to less than 1ms without ordering the results. (The third line in the report starts with the description `Stream results`.) However, the total time spent did not significantly change (the first two rows in the reports). We can find out that the time of `sorting` (the `ORDER BY` statement) dominated most of the time cost (sorting is about 25ms, far more than other parts with a cost about 1 to 7 ms)

#### Query 2 without indexing
```
-> Limit: 15 row(s)  (actual time=25.017..25.020 rows=15 loops=1)
    -> Sort: ac_a_distance, r.r_name DESC, limit input to 15 row(s) per chunk  (actual time=25.017..25.019 rows=15 loops=1)
        -> Stream results  (cost=661851.47 rows=542557) (actual time=6.917..24.938 rows=24 loops=1)
            -> Nested loop inner join  (cost=661851.47 rows=542557) (actual time=6.911..24.888 rows=24 loops=1)
                -> Inner hash join (a.city_name = ac.city_name)  (cost=4733.48 rows=1534) (actual time=5.210..6.657 rows=40 loops=1)
                    -> Filter: ((a.categories like '%Museum%') or (a.categories like '%museum%'))  (cost=1.16 rows=74) (actual time=0.099..1.486 rows=170 loops=1)
                        -> Table scan on a  (cost=1.16 rows=1769) (actual time=0.095..0.761 rows=1769 loops=1)
                    -> Hash
                        -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.093..5.053 rows=1 loops=1)
                            -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.089..4.160 rows=4989 loops=1)
                -> Filter: (((sqrt((pow((a.latitude - r.latitude),2) + pow((a.longitude - r.longitude),2))) * 100) < 1) and <in_optimizer>(r.restaurant_id,r.restaurant_id in (select #2)))  (cost=16.50 rows=354) (actual time=0.355..0.456 rows=1 loops=40)
                    -> Index lookup on r using city_name (city_name=ac.city_name)  (cost=16.50 rows=354) (actual time=0.043..0.334 rows=388 loops=40)
                    -> Select #2 (subquery in condition; run only once)
                        -> Filter: ((r.restaurant_id = `<materialized_subquery>`.restaurant_id))  (cost=0.00..0.00 rows=0) (actual time=0.003..0.003 rows=0 loops=532)
                            -> Limit: 1 row(s)  (actual time=0.003..0.003 rows=0 loops=532)
                                -> Index lookup on <materialized_subquery> using <auto_distinct_key> (restaurant_id=r.restaurant_id)  (actual time=0.000..0.000 rows=0 loops=532)
                                    -> Materialize with deduplication  (cost=0.00..0.00 rows=0) (actual time=1.664..1.664 rows=20 loops=1)
                                        -> Filter: (count(rm.restaurant_id) > 0)  (actual time=1.396..1.402 rows=20 loops=1)
                                            -> Table scan on <temporary>  (actual time=0.001..0.003 rows=20 loops=1)
                                                -> Aggregate using temporary table  (actual time=1.394..1.398 rows=20 loops=1)
                                                    -> Nested loop inner join  (cost=33.96 rows=39) (actual time=0.142..1.341 rows=26 loops=1)
                                                        -> Filter: (r.category = 'American')  (cost=20.38 rows=39) (actual time=0.125..1.151 rows=49 loops=1)
                                                            -> Index lookup on r using city_name (city_name='Chicago')  (cost=20.38 rows=388) (actual time=0.117..1.090 rows=388 loops=1)
                                                        -> Covering index lookup on rm using restaurant_id (restaurant_id=r.restaurant_id)  (cost=0.25 rows=1) (actual time=0.003..0.004 rows=1 loops=49)
```

#### index_rm_id: add index on restaurants_comments.restaurant_id
```
-> Limit: 15 row(s)  (actual time=36.225..36.230 rows=15 loops=1)
    -> Sort: ac_a_distance, r.r_name DESC, limit input to 15 row(s) per chunk  (actual time=36.224..36.227 rows=15 loops=1)
        -> Stream results  (cost=661851.47 rows=542557) (actual time=4.289..36.141 rows=24 loops=1)
            -> Nested loop inner join  (cost=661851.47 rows=542557) (actual time=4.283..36.088 rows=24 loops=1)
                -> Inner hash join (a.city_name = ac.city_name)  (cost=4733.48 rows=1534) (actual time=3.225..6.168 rows=40 loops=1)
                    -> Filter: ((a.categories like '%Museum%') or (a.categories like '%museum%'))  (cost=1.16 rows=74) (actual time=0.092..2.910 rows=170 loops=1)
                        -> Table scan on a  (cost=1.16 rows=1769) (actual time=0.090..1.458 rows=1769 loops=1)
                    -> Hash
                        -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.099..3.112 rows=1 loops=1)
                            -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.095..2.677 rows=4989 loops=1)
                -> Filter: (((sqrt((pow((a.latitude - r.latitude),2) + pow((a.longitude - r.longitude),2))) * 100) < 1) and <in_optimizer>(r.restaurant_id,r.restaurant_id in (select #2)))  (cost=16.50 rows=354) (actual time=0.601..0.748 rows=1 loops=40)
                    -> Index lookup on r using city_name (city_name=ac.city_name)  (cost=16.50 rows=354) (actual time=0.077..0.596 rows=388 loops=40)
                    -> Select #2 (subquery in condition; run only once)
                        -> Filter: ((r.restaurant_id = `<materialized_subquery>`.restaurant_id))  (cost=0.00..0.00 rows=0) (actual time=0.002..0.002 rows=0 loops=532)
                            -> Limit: 1 row(s)  (actual time=0.002..0.002 rows=0 loops=532)
                                -> Index lookup on <materialized_subquery> using <auto_distinct_key> (restaurant_id=r.restaurant_id)  (actual time=0.000..0.000 rows=0 loops=532)
                                    -> Materialize with deduplication  (cost=0.00..0.00 rows=0) (actual time=1.061..1.061 rows=20 loops=1)
                                        -> Filter: (count(rm.restaurant_id) > 0)  (actual time=0.773..0.777 rows=20 loops=1)
                                            -> Table scan on <temporary>  (actual time=0.000..0.002 rows=20 loops=1)
                                                -> Aggregate using temporary table  (actual time=0.771..0.774 rows=20 loops=1)
                                                    -> Nested loop inner join  (cost=50.71 rows=53) (actual time=0.125..0.732 rows=26 loops=1)
                                                        -> Filter: (r.category = 'American')  (cost=20.38 rows=39) (actual time=0.108..0.609 rows=49 loops=1)
                                                            -> Index lookup on r using city_name (city_name='Chicago')  (cost=20.38 rows=388) (actual time=0.103..0.570 rows=388 loops=1)
                                                        -> Covering index lookup on rm using index_rm_id (restaurant_id=r.restaurant_id)  (cost=0.65 rows=1) (actual time=0.002..0.002 rows=1 loops=49)
```
As we can see, the index `index_rm_id` is used for looking on the ids between restaurants_comments and restaurants tables. However, the result in the last line `(cost=0.65 rows=1) (actual time=0.002..0.002 rows=1 loops=49)` suggested that there is no big difference when adding the index. The reason might be that the records need to be search in restaurants_comments are far less than those in the restaurants table.

#### index_r_cat: add index on restaurants.category
```
-> Limit: 15 row(s)  (actual time=30.323..30.327 rows=15 loops=1)
    -> Sort: ac_a_distance, r.r_name DESC, limit input to 15 row(s) per chunk  (actual time=30.323..30.325 rows=15 loops=1)
        -> Stream results  (cost=661851.47 rows=542557) (actual time=4.435..30.236 rows=24 loops=1)
            -> Nested loop inner join  (cost=661851.47 rows=542557) (actual time=4.428..30.189 rows=24 loops=1)
                -> Inner hash join (a.city_name = ac.city_name)  (cost=4733.48 rows=1534) (actual time=3.624..5.510 rows=40 loops=1)
                    -> Filter: ((a.categories like '%Museum%') or (a.categories like '%museum%'))  (cost=1.16 rows=74) (actual time=0.089..1.905 rows=170 loops=1)
                        -> Table scan on a  (cost=1.16 rows=1769) (actual time=0.086..0.989 rows=1769 loops=1)
                    -> Hash
                        -> Filter: (ac.ac_name = 'Tiny Studio Apartment 94 Walk Score')  (cost=516.35 rows=492) (actual time=0.112..3.496 rows=1 loops=1)
                            -> Table scan on ac  (cost=516.35 rows=4921) (actual time=0.107..3.005 rows=4989 loops=1)
                -> Filter: (((sqrt((pow((a.latitude - r.latitude),2) + pow((a.longitude - r.longitude),2))) * 100) < 1) and <in_optimizer>(r.restaurant_id,r.restaurant_id in (select #2)))  (cost=16.50 rows=354) (actual time=0.483..0.617 rows=1 loops=40)
                    -> Index lookup on r using city_name (city_name=ac.city_name)  (cost=16.50 rows=354) (actual time=0.064..0.495 rows=388 loops=40)
                    -> Select #2 (subquery in condition; run only once)
                        -> Filter: ((r.restaurant_id = `<materialized_subquery>`.restaurant_id))  (cost=0.00..0.00 rows=0) (actual time=0.002..0.002 rows=0 loops=532)
                            -> Limit: 1 row(s)  (actual time=0.002..0.002 rows=0 loops=532)
                                -> Index lookup on <materialized_subquery> using <auto_distinct_key> (restaurant_id=r.restaurant_id)  (actual time=0.000..0.000 rows=0 loops=532)
                                    -> Materialize with deduplication  (cost=0.00..0.00 rows=0) (actual time=0.804..0.804 rows=20 loops=1)
                                        -> Filter: (count(rm.restaurant_id) > 0)  (actual time=0.553..0.557 rows=20 loops=1)
                                            -> Table scan on <temporary>  (actual time=0.000..0.001 rows=20 loops=1)
                                                -> Aggregate using temporary table  (actual time=0.552..0.554 rows=20 loops=1)
                                                    -> Nested loop inner join  (cost=54.01 rows=50) (actual time=0.205..0.514 rows=26 loops=1)
                                                        -> Filter: ((r.city_name = 'Chicago') and (r.category = 'American'))  (cost=25.09 rows=37) (actual time=0.160..0.362 rows=49 loops=1)
                                                            -> Index range scan on r using intersect(index_r_cat,city_name)  (cost=25.09 rows=37) (actual time=0.158..0.346 rows=49 loops=1)
                                                        -> Covering index lookup on rm using index_rm_id (restaurant_id=r.restaurant_id)  (cost=0.65 rows=1) (actual time=0.003..0.003 rows=1 loops=49)
```
As we can see, the index `index_r_cat` was used for joining the tables `restaurants` and `restaurants_comments` for the searching stage. The searching rows reduced from 388 to 37, but the actual time spending was not reduced. 

#### index_ac_name: add index on accommodations.ac_name
```
-> Limit: 15 row(s)  (actual time=24.811..24.813 rows=15 loops=1)
    -> Sort: ac_a_distance, r.r_name DESC, limit input to 15 row(s) per chunk  (actual time=24.810..24.812 rows=15 loops=1)
        -> Stream results  (cost=3901.93 rows=26269) (actual time=1.088..24.744 rows=24 loops=1)
            -> Nested loop inner join  (cost=3901.93 rows=26269) (actual time=1.084..24.701 rows=24 loops=1)
                -> Nested loop inner join  (cost=49.98 rows=74) (actual time=0.291..1.878 rows=40 loops=1)
                    -> Index lookup on ac using index_ac_name (ac_name='Tiny Studio Apartment 94 Walk Score')  (cost=0.35 rows=1) (actual time=0.062..0.063 rows=1 loops=1)
                    -> Filter: ((a.categories like '%Museum%') or (a.categories like '%museum%'))  (cost=21.67 rows=74) (actual time=0.228..1.810 rows=40 loops=1)
                        -> Index lookup on a using city_name (city_name=ac.city_name)  (cost=21.67 rows=354) (actual time=0.225..1.629 rows=300 loops=1)
                -> Filter: (((sqrt((pow((a.latitude - r.latitude),2) + pow((a.longitude - r.longitude),2))) * 100) < 1) and <in_optimizer>(r.restaurant_id,r.restaurant_id in (select #2)))  (cost=16.98 rows=354) (actual time=0.446..0.570 rows=1 loops=40)
                    -> Index lookup on r using city_name (city_name=ac.city_name)  (cost=16.98 rows=354) (actual time=0.065..0.461 rows=388 loops=40)
                    -> Select #2 (subquery in condition; run only once)
                        -> Filter: ((r.restaurant_id = `<materialized_subquery>`.restaurant_id))  (cost=0.00..0.00 rows=0) (actual time=0.002..0.002 rows=0 loops=532)
                            -> Limit: 1 row(s)  (actual time=0.002..0.002 rows=0 loops=532)
                                -> Index lookup on <materialized_subquery> using <auto_distinct_key> (restaurant_id=r.restaurant_id)  (actual time=0.000..0.000 rows=0 loops=532)
                                    -> Materialize with deduplication  (cost=0.00..0.00 rows=0) (actual time=0.818..0.818 rows=20 loops=1)
                                        -> Filter: (count(rm.restaurant_id) > 0)  (actual time=0.574..0.578 rows=20 loops=1)
                                            -> Table scan on <temporary>  (actual time=0.001..0.002 rows=20 loops=1)
                                                -> Aggregate using temporary table  (actual time=0.573..0.576 rows=20 loops=1)
                                                    -> Nested loop inner join  (cost=54.01 rows=50) (actual time=0.232..0.543 rows=26 loops=1)
                                                        -> Filter: ((r.city_name = 'Chicago') and (r.category = 'American'))  (cost=25.09 rows=37) (actual time=0.196..0.400 rows=49 loops=1)
                                                            -> Index range scan on r using intersect(index_r_cat,city_name)  (cost=25.09 rows=37) (actual time=0.194..0.384 rows=49 loops=1)
                                                        -> Covering index lookup on rm using index_rm_id (restaurant_id=r.restaurant_id)  (cost=0.65 rows=1) (actual time=0.003..0.003 rows=1 loops=49)
```
After implementing this index, we can find out the performance significantly reduced without considering the orders (line 4, which started with `Stream results`). The time was reduced from 4.4 ms to about 1 ms, and the cost was reduced from 661851.47 to 3901.93. The index `index_ac_name` is used to look up the ac_name, the `WHERE` condition statement in the query. In the rows of the result, we can find out that the cost was reduced from 516.35 to 0.35, and time was reduced from 0.1 to 0.06 for each sub-execution. 

#### index_a_cat: add index on attractions.categories
```
-> Limit: 15 row(s)  (actual time=26.500..26.508 rows=15 loops=1)
    -> Sort: ac_a_distance, r.r_name DESC, limit input to 15 row(s) per chunk  (actual time=26.499..26.505 rows=15 loops=1)
        -> Stream results  (cost=3901.93 rows=26269) (actual time=0.994..26.392 rows=24 loops=1)
            -> Nested loop inner join  (cost=3901.93 rows=26269) (actual time=0.991..26.344 rows=24 loops=1)
                -> Nested loop inner join  (cost=49.98 rows=74) (actual time=0.292..0.950 rows=40 loops=1)
                    -> Index lookup on ac using index_ac_name (ac_name='Tiny Studio Apartment 94 Walk Score')  (cost=0.35 rows=1) (actual time=0.053..0.056 rows=1 loops=1)
                    -> Filter: ((a.categories like '%Museum%') or (a.categories like '%museum%'))  (cost=21.67 rows=74) (actual time=0.237..0.889 rows=40 loops=1)
                        -> Index lookup on a using city_name (city_name=ac.city_name)  (cost=21.67 rows=354) (actual time=0.235..0.659 rows=300 loops=1)
                -> Filter: (((sqrt((pow((a.latitude - r.latitude),2) + pow((a.longitude - r.longitude),2))) * 100) < 1) and <in_optimizer>(r.restaurant_id,r.restaurant_id in (select #2)))  (cost=16.98 rows=354) (actual time=0.507..0.635 rows=1 loops=40)
                    -> Index lookup on r using city_name (city_name=ac.city_name)  (cost=16.98 rows=354) (actual time=0.064..0.509 rows=388 loops=40)
                    -> Select #2 (subquery in condition; run only once)
                        -> Filter: ((r.restaurant_id = `<materialized_subquery>`.restaurant_id))  (cost=0.00..0.00 rows=0) (actual time=0.002..0.002 rows=0 loops=532)
                            -> Limit: 1 row(s)  (actual time=0.002..0.002 rows=0 loops=532)
                                -> Index lookup on <materialized_subquery> using <auto_distinct_key> (restaurant_id=r.restaurant_id)  (actual time=0.000..0.000 rows=0 loops=532)
                                    -> Materialize with deduplication  (cost=0.00..0.00 rows=0) (actual time=0.739..0.739 rows=20 loops=1)
                                        -> Filter: (count(rm.restaurant_id) > 0)  (actual time=0.501..0.506 rows=20 loops=1)
                                            -> Table scan on <temporary>  (actual time=0.001..0.002 rows=20 loops=1)
                                                -> Aggregate using temporary table  (actual time=0.501..0.503 rows=20 loops=1)
                                                    -> Nested loop inner join  (cost=54.01 rows=50) (actual time=0.157..0.466 rows=26 loops=1)
                                                        -> Filter: ((r.city_name = 'Chicago') and (r.category = 'American'))  (cost=25.09 rows=37) (actual time=0.136..0.340 rows=49 loops=1)
                                                            -> Index range scan on r using intersect(index_r_cat,city_name)  (cost=25.09 rows=37) (actual time=0.135..0.322 rows=49 loops=1)
                                                        -> Covering index lookup on rm using index_rm_id (restaurant_id=r.restaurant_id)  (cost=0.65 rows=1) (actual time=0.002..0.002 rows=1 loops=49)
```

We try to apply the index on the categories of attractions because we considered that there might be a significant effect in the searching process like the previous index `index_ac_name`. However, the execution did not include the index `index_a_cat`. This might result from the query that we used the `LIKE` statement. (`a.categories LIKE '%Museum%'`)

