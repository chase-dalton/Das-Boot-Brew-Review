# Das Boot Brew Review

## **Topic**
  - Our topic is about beer! We want to know what factors contribute to the best glass of beer.

## **Reason**
  - We chose our topic due to everyone loving beer!

## **Description of data source**

  - Our data source is 1.5 million reviews on beers, with the ratings of look, taste, mouthfeel, and smell. Other data sources we have include different breweries and their locations, and types of ingredients for beer.

## **Questions we hope to answer**

  - We want to know what goes into making the perfect beer? What has the highest weight for someone to like a beer based on factors such as look, taste, mouthfeel, alcohol content, bitterness, and smell?

## **Communication**

- Our group is communicating primarily through Discord and Slack.  We created a Google Drive folder to house shared files, and also a trello board to manage our project.
- With each commit, we communcate with each member to check the information and review the code.

## **Project Outline**

- Step 1 **Think of a Question**
- - We spent the first couple of classes really diving in and figuring out what question we would like to answer. We knew setting a solid foundation is key and created this our first priority.
- Step 2 **Found Data Sources**
- - Once we had a question set, we researched some data sources that can help answer our question.
- Step 3 **Initialize a Database**
- - We decided to create an AWS database to house our data.
- Step 4 **Create a Machine Learning Algorithm**
- - We wanted to know if a beer is going to be good or not, so we created a machine learning algorithm that is 77% accurate.
- Step 5 **Presentation**
- - We don't want to just create a Tableau dashboard. We want to create a functioning website that people can go to, and input certain criteria to see if a beer will be good or not. We are using Heroku to allow anyone to access the website.
- Step 6 **The Pitch**
- - We will be creating a google slides presentation, along with our website, to pitch to investors that we have a viable product.

## **Data Exploration**
- We wanted our data to help us not only tell us if a beer is good or not, but to also help us create a program that users can input certain criteria and see if they could make a good beer. The data exploration process was a crucial one, where we had to find reviews of different beers, a 1-5 rating for those beers focused on different features, the methods that the beers were brewed with the ingredients, etc. There is a lot that comes into play, and we focused in on finding the right data sources to help us tell our story.

## **Machine Learning**

- We have done preliminary linear regression on beer review data to identify which attributes of a beer contribute most to the overall review score.  We discovered that a beer's overall review score is most closely correlated to taste score.  So our ML model focuses on predicting whether or not a beer's taste score will be above (a good beer) or below (a not good beer) 4.0.  We tried a variety of Machine Learning models, and found that a Gradient Boosting Classifier resulted in a prediction model with the highest level of accuracy.


## **Database**

- We have set up a database through AWS to house our cleaned datasets.

## **Presentation**

- Here is the link to our presentation: [Google Slides Presentation](https://docs.google.com/presentation/d/1bLgCaShy3VGehPZgpbyOCZr1AdiEvK3gFdSeHPxAY3Y/edit?usp=sharing)
