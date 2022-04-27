# CS411 PT1 - Stage 2


## UML Diagram
!['The diagram'](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team046-YYCC/blob/41bae591c002b24df4e70cb3c86a04bf8d2deb27/doc/CS411_PT2_diagram.jpg)

----
## Relationship and assumptions
In our current UML design, we have the assumption that all of the facilities, no matter which kind of facilities or services, can always be found inside the range of a city. Therefore, the real question is how to relate user preference to the right place? In this version of UML, we propose the user can independently create their preference for each restaurant, accommodation, and tourist. One question will definitely raise why the laundry and market do not need a preference table? Since we have the geo-coordinates for those two tables, we can instead recommend the shops providing such services within the proximity of the user. Additional preference table for market and laundry is not provided here.

----
## Relational Schema
Preference(UserID:INT \[PK\]\[FK to Users.UserID\], OutdoorLoverType:REAL, FoodPreference:VARCHAR(255), BudgetType:REAL, ArtType:REAL, MuseumType:REAL, CityTripType:REAL, TransportationType:VARCHAR(255))

Users(UserID:INT \[FK\], Password:VARCHAR(255), FirstName:VARCHAR(255), LastName:VARCHAR(255), Email:VARCHAR(255), Phone:VARCHAR(255), City:VARCHAR(255), Birthdate:DATE)

ResaurantComment(CommentID:INT \[PK\], UserID:INT \[FK to Users.UserID\], StoreID:INT \[FK to Restaurant.RestaurantID\], Comment:TEXT)

AccomodatationComment(CommentID:INT \[PK\], UserID:INT \[FK to Users.UserID\], StoreID:INT \[FK to Accomodation.AccomodationID\], Comment:TEXT)

SpotsComment(CommentID:INT \[PK\], UserID:INT \[FK to Users.UserID\], StoreID:INT \[FK to TouristSpot.SpotID\], Comment:TEXT)

Market(MarketID:INT \[PK\], MarketName:VARCHAR(255), Address:VARCHAR(255), City:VARCHAR(255) \[FK to City.City\], PostalCode:VARCHAR(10), Latitude:REAL, Longitude:REAL, PriceLevel:INT)

Laundry(LaundryID:INT \[PK\], LaundryName:VARCHAR(255), Address:VARCHAR(255), City:VARCHAR(255) \[FK to City.City\], PostalCode:VARCHAR(10), Latitude:REAL, Longitude:REAL, PriceLevel:INT)

Restaurant(RestaurantID:INT \[PK\], RestaurantName:VARCHAR(255), Address:VARCHAR(255), City:VARCHAR(255) \[FK to City.City\], PostalCode:VARCHAR(10), Latitude:REAL, Longitude:REAL, PriceLevel:INT, AvgRating:REAL, Categories:VARCHAR(255))

Accomodation(AccommodationID:INT \[PK\], AccommodationName:VARCHAR(255), Address:VARCHAR(255), City:VARCHAR(255) \[FK to City.City\], PostalCode:VARCHAR(10), Latitude:REAL, Longitude:REAL, PriceLevel:INT, AvgRating:REAL, Categories:VARCHAR(255)

TouristSpot(SpotID:INT \[PK\], SpotName:VARCHAR(255), Address:VARCHAR(255), City:VARCHAR(255) \[FK to City.City\], PostalCode:VARCHAR(10), Latitude:REAL, Longitude:REAL, AvgRating:REAL, PriceLevel:INT)

City(City:VARCHAR(255), State:VARCHAR(255), Country:VARCHAR(255), Introduction:Text, Area:REAL, TemperatureRange:VARCHAR(255))

----
## Relations and Assumptions
### Relationship between users and preference table
We assume that every user can have either zero or many preference profiles linked to their account. This provides the users whose planning trip alone or together as a group can store multiple trip preferences to have more flexibility to adjust their plan accordingly to the different parts of the trip. The data required to fill in the table is expected to have users complete a questionnaire to supply the table.

### Relationship between user and Restaurant, Accommodation, Tourist Spot
Each user can leave comments on many restaurants (accommodation, tourist spot) and each restaurant (accommodation, touristspot) can have many comments from users, so it’s a many-to-many relationship. We add RestaurantComment (AccommodationComment, SpotsComment) as an intermediate table. For each comment in this table, there must only be one restaurant (accomodation, touristspot) and one user. 

### Relationship between City, Restaurant, Accommodation, and TourtistSpot
In our system, we assume each city has many restaurants and each restaurant is located in one city, each city has many accommodations and each accommodation is located in one city, and each city has many tourist spots and each tourist spot is located in one city.

### Relationship between City, Market, and Laundry
In our system, we assume that there are several markets or several laundries in a city. We allow zero to many markets or laundries in a city. On the other hand, The relationship between a market to the city and the laundry to the city is one to one; that is a market or a laundry should only belong to one city.

