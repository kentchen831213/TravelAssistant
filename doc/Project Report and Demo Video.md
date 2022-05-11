# Team 046 YYCC - A Travel Assistant

## 1. Please list out changes in direction of your project if the final project is different from your original proposal (based on your stage 1 proposal submission)

Originally, when we were designing our website interface, we got ideas from some stylish websites we’ve seen before. When actually constructing the pages we found that some features that seemed to be simple were actually hard to implement. We failed to consider that the tools we use to develop might have limitations to what we want to present or it could take a great amount of time to achieve, which we didn’t have. We have to adjust our design of the pages while still maintaining the functions.

----
## 2. Discuss what you think your application achieved or failed to achieve regarding its usefulness.

Achieve usefulness in our application is to provide the nearest laundry and supermarket according to the user's accommodation. When people travel, they always need 
to buy some food, wine, and laundry. Therefore, this function is beneficial for all our application's users. It makes people enjoy their journey and not worry about 
food or laundry issues. Another useful service is our recommendation system. Users only need to choose some preferences, and we would recommend specific travel schedules
for them, which would make them not need to spend much time planning their journey. By clicking some button, Travelassistant would recommend the most suitable travel plan. 
Lastly, our comment functions are helpful as well. Users can write comments and ratings for each accommodation, restaurant, and attraction. They also can see other people's 
comments, which make them can planing their travel according to other people's experiences. All the above functions are beneficial for all Travelassistant's users. 
It is not the end of our project. We would continue to update our application to make it become a more comprehensive travel website. 

----
## 3. Discuss if you changed the schema or source of the data for your application

During the early phase of our project, we strive to preserve the structure of our original schema instead of trying to alter it to adapt the dataset. For example, 
in the current database, the laundry table consists of coordinates information. Both longitude and latitude were added to the raw dataset by checking the postal
code of the scrapped dataset. But most of the time, we are choosing part of the raw dataset to fit into our schema. The raw data can have duplicate information 
which is not preferable for the schema for normalization reasons.


----
## 4. Discuss what you change to your ER diagram and/or your table implementations. What are some differences between the original design and the final design? Why? What do you think is a more suitable design? 

Overall, our UML diagram is the same as our proposal, all the tables have been created, and the columns are similar. The only difference is on the Preference table, 
we utilize the stored procedure to generate the Preference table rather than make it initially. It will be better if we can create it initially. When the query executes 
the stored procedure, the preference table would be updated, and all the information would be lost. It's not a suitable method. Therefore, it would be better if we could 
create a preference table initially. 

----
## 5. Discuss what functionalities you added or removed. Why?

We added the comment functions in our application. Because we think it would be helpful if our users can write some comments for all the restaurants, attractions, and accommodations. Moreover, users can also see other people's comments, making them know the objective rating for all the restaurants, attractions, and accommodations. Lastly, we did not remove any function since all the functions are valuable and practical. 

----
## 6. Explain how you think your advanced database programs complement your application.


### Advanced Query
Query 1: Find the utilities when searching for an accommodations
The first query is to solve a common problem while traveling. We are dealing with logistics problems for example, where to buy groceries and supplies. In some cases even coin laundry service. The query is to find out those services and present this extra information to users. It helps people to evaluate whether they are making a decent choice by taking a few logistics problems into account. We believed that this will greatly help with the early planning phase of the trip.


Query 2: An Advance Search
Normally, users need to individually search for the place to visit and discuss where to eat and rest after they are done with a tourist spot. The second query search for the nearest tourist spot from the place they stayed and the restaurant of particular interest within the proximity of the tourist spot. It helped the user to worry less about how to arrange their schedule and smoothen their trip experience. It is mainly targeted at people who found organizing trips to be tiring.

### Trigger
The trigger was used for checking if a user is a local guide (a special kind of user) or not. The criteria are based on how many comments are left on our website. In this case, a user will become a local guide when they leave three or more comments. Triggers are very useful for requirements. For each time a comment is added or deleted, the trigger will be executed. We don’t need an additional process in the backend to deal with the case.

### Stored Procedure
The stored procedure is based on the user's personal preference. When users tell us their personal preferences, we would collect this information, and we would query specific recommendation packages from restaurants, attractions and accommodations tables. Therefore, the users can get the results that they prefer. And we would insert all this data to PreferenceTable. Through the easy questionnaire, we would build up the PreferenceTable so that we can suggest a travel package for them. It is a valuable and helpful function.  

----
## 7. Each team member should describe one technical challenge that the team encountered.  This should be sufficiently detailed such that another future team could use this as helpful advice if they were to start a similar project or where to maintain your project. 

Kent: 
The writing formats for request URL methods are different. Initially, we utilized the Django Forms API to help us get the user requests and implement the corresponding action. Lastly, we change the format for request URL methods by using HTML to get the user’s requests. This change makes our coding style not unified and challenging to maintain. The advice for this challenge is that before starting a project and coding, every member should discuss and have a unified coding style. By unifying all the coding styles and methods, it would be easier for everyone to maintain and update the systems. 

Chung-Kuang Lin:
Collecting real-world data without proper tools can be challenging to reach the targeted scale of each schema table since the fact that more sites nowadays are scraper-proof. We eventually use a web browser extension “Instant Data Scraper” to obtain the dataset we need. Another challenge is to clean the raw data into the legal format in the SQL database. Not only the single quote will cause the insert clause to parse incorrectly, but the emoji included in the string will be a source of the problem. It is crucial to develop a workflow to accelerate the data-cleaning process. At each phase, make sure to have a simple diagram to record the current state of the schema otherwise it is quite often to get confused with the different build-state of each schema.

Yu-Wei Lai
Since we used django and didn’t separate frontend and backend, it was hard for us to divide the work by roles. At first we developed some fancy frontend pages but couldn’t find a way to combine it with our backend data. During this project, we each had to write some frontend and backend so the style was not unified and the code was messy. Also, it would be more efficient if one person just focused on learning one programming language instead of mixing HTML, css, JavaScript and python all together. The process of combining everything together was time consuming and a big challenge for us. In the future, when developing a website, how the frontend and backend are connected should always be considered.

Tessa Chang:
In order for this website to be used by real world users, the website should contain the latest information for the sites in the cities. However, we don’t have a mechanism to update our location information periodically. We got our data from various sources. Some data came from open sources that we could download, some data came from scraping other similar websites and some data came from scraping google maps. It took us a lot of time to clean the data and it was a one time task. But the spots actually update very frequently. For example, hotels opening or closing, restaurants changing the opening hours or new traveling sites discovering. This constantly changing data should be updated to our website so the users could get the most accurate information. There should be a data pipeline that updates our data and website periodically.



----
## 8. Are there other things that changed comparing the final application with the original proposal?

Better Recommendation
The current recommendations system is based on one-time user input and the history rating record of the target. It is now only based on the popularity to make recommendations, i.e. not necessarily related to users’ preferences. 
Code Quality and efficiency
Right now we developed the application based on the function we want it to achieve. Although it worked as we wanted, the code was messy and thus made it hard for future development. Duplicate or unused code should be removed. Also, the efficiency of our program should be considered since it is an important issue when having multiple users using it.
Use Rest API to separate frontend and backend
Separating frontend and backend would be a wise way to develop a website. This helped with distributing the work and the consistency of code. Furthermore, it would make expanding the scale of our application easier.
concurrency control
We need to allow the website to process different tasks at the same time. When the website is in production, there will be multiple users using different functions at our website at the same time. Designing the website to have concurrency control is an important task we should work on.



----
## 10. Describe the final division of labor and how well you managed teamwork.

Full stack: Lai, Yu-Wei, Chang, Tessa, Lin, Chung-Kuang, Chen, Yuan-Chih


# Video
#### Travelassistant [video](https://youtu.be/FSpMWUI5DEw)

