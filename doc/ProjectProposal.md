
# Team 046 YYCC - A Travel Assistant

## Project Summary
Most of the travel websites focus on search, price comparison, or comments. The information they provided is locations based rather than users based. Users will spend some time to find out what restaurants, tourist spots, or accommodations really suit their budget or preference. Our project aims to provide a simple, more user-relevant, painless information searching solution for travelers.

We will focus on building a database containing real-world data, including basic information for restaurants, tourist spots, and accommodations. The database will also include data revealing preferences such as reviews, scoring, or visiting information. The data sources of the database will be web scraping data or open-source data sets from famous platforms, such as Yelp, Airbnb, etc. With a massive amount of data, we aim to build our searching sites and recommender systems. As for user data, we will create a mock database that contains individual information, behaviors, and opinions. Finally, we will use the mock data to test our travel information searching system.

----
## Description
Basic recommender based on trips locations: the user provides the main place they are traveling to, and the system will generate several places for restaurants and tourist spots. Ranked by ratings on several websites.

#### Additional Ideas:
1. The conventional recommendation results are various for the conventional trip-advising platform. But we found filtering the recommended list of results is prone to cause difficulties to choice. On top of this, we noticed some unrealistic results for budget travelers. Results include but are not limited to high-end hotels, restaurants,s or the service price simply a mismatch for travelers or tourists with serious budget management needs.

2. Budget management is a crucial topic for backpackers. Instead of recommending the best restaurant that the travel destination has to offer, we would like to recommend the optimal choices for the current time and place. Judging from the available budget balance of the user, we aimed to provide the suitable food choice based on the budget, meals count for the trip, and personal preferences. Even if we skipped meals, the service will come up with choices taken those budget headroom into consideration.

3. Amenity support: Not everyone gets to stay in Airbnb or a hotel. Sometimes the logistics of a trip can be a problem. The user can receive the location of the nearest supermarkets, coin laundry, and possibly coffee shops if desired. This will significantly reduce the time searching back and forth on other services and improve the quality of the journey.

#### Difficulties:
- Mapping between different tables / data sources: The names between google map and yelp of the tourist spots or restaurants might be different. We should consider additional attributes that might share a similar property

----
## Usefulness
One of the problems that every member encountered when planning their trip was how closely the place they stayed could be far away from the tourist spots they planned to visit. A functionality recommending hotels that are near to given tourist spots can address this issue. In short, the reservation site has recommendations based on where you decided to stay or where you plan to visit instead of planning for a visit. This functionality aims to become a one-stop site by filling the gap between the discrepancy and conflicting choices we made during the early trip planning process. 

----
## Realness
The datasets are collected from Yelp, Airbnb, Booking, Expedia, and Tripadvisor. For the restaurants’ data, we will use the datasets with detailed properties provided by Yelp. We will organize and mine the data into the formats we expect. For the accommodation and travel data, we aim to scrap from Airbnb, Tripadvisor, and organize them into the data format we want.

The realness of these datasets is reliable, the Yelp datasets are collected from real-world users, and Airbnb and Expedia are the most popular accommodation websites in the world. Hence, these datasets are real and reliable.

----
## Functionality
### Data
#### User Data
The mock data that what users will do on our website, including the places they like, the types of their cursine preferences, the places they have visited, the reviews they left on our website, etc.

- User: account data / past search data / liked places data / preference data

#### Restaurant Data
This part of data will based on the open-source dataset provided by Yelp. We will also included other data by web scraping Google Map and reviews on Tripadvisor. The attributes will include name, location, address, open hours, categories, reviews, rating, etc. The Yelp dataset: <https://www.yelp.com/dataset>.

- Restaurant data: restaurant name/ city/ category/longitude/ latitude/rating

#### Tourist Spots Data
The data will be scraped from Google Map, including name, location (longitude and latitude), types, reviews, etc.

- Tourist Spot: name / city / category / longitude / latitude / rating

#### Hotels / Accommodation data
The data will include a open-source dataset from Airbnb. Also, we will try to scrap data from Google maps and booking websites. We will include the attributes such as name, location (longtitude and latitude), address, reviews, etc. The airbnb dataset: <http://insideairbnb.com/get-the-data.html>

Hotels / Accommodation data: name / city / longitude / price /latitude / rating

### Functions
- User create account
- User login/logout
- Recommend Restaurants
- Recommend Tourist Spots
- Recommend Hotels 
  
For restaurant and tourist spots recommendation, user can choose what kind of restaurant and tourist spots they want to visit, we will query corresponding results for them. For accommodation, users can select specific price range, we will query corresponding hotels for them. Lastly, we will query addtional information such as laundries, supermarkets that nearby with the accommodation location.

#### Basic Search for Restaurants, Tourist Spots, and Accomodations (Basic)
Just tell us where you are, where you want to go, and we will list out most popular, hot-trend, must-go spots for you. The relevant information will base on reviews count, reviews, ratings, or vistors count from the data set.

#### User Based Recommendations (Complex)
Just tell us where you are, where you want to go, and we will recommend the best restaurants, tourist spots, or accomodations that suits you! We will learn what users' preference by the users' previous likes, reviews, budgets, or places they often visits and give users their personal relevant recommendations.

#### Intimate Service (Complex)
Never worry about being hungry or being messy! Our system has a intimate service that simply provide information about supermarkets or laundry near where you accommodate.

----
## UI Mockup
![mock_ui_1](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team046-YYCC/blob/b2c58a87a59e919b569af08b8cc8e038ffc955af/doc/mock_ui/mock_ui_1.png)
![mock_ui_2](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team046-YYCC/blob/b2c58a87a59e919b569af08b8cc8e038ffc955af/doc/mock_ui/mock_ui_2.png)
![mock_ui_3](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team046-YYCC/blob/b2c58a87a59e919b569af08b8cc8e038ffc955af/doc/mock_ui/mock_ui_3.png)
![mock_ui_4](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team046-YYCC/blob/b2c58a87a59e919b569af08b8cc8e038ffc955af/doc/mock_ui/mock_ui_4.png)
![mock_ui_5](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team046-YYCC/blob/b2c58a87a59e919b569af08b8cc8e038ffc955af/doc/mock_ui/mock_ui_5.png)
![mock_ui_6](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team046-YYCC/blob/b2c58a87a59e919b569af08b8cc8e038ffc955af/doc/mock_ui/mock_ui_6.png)

----
## Project Work Distribution

|   Info                 |              Work Distribution               |
| ---------------------- | -------------------------------------------- |
| Lai, Yu-Wei            |   backend   |
| Chang, Tessa           |   backend   |
| Chen, Yuan-Chih        |   frontend   |
| Lin, Chung-Kuang       |   full stack   |