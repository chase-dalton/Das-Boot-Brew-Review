# Das Boot Brew Review

## **Topic**
Since we all enjoy a frosty pint, we want to know what factors contribute to the best glass of beer.  We will answer the question: *What features in a beer's recipe contribute most to a highly-reviewed glass of beer?*


## **Data**

Our data source is 1.5 million reviews on beers, with the ratings of look, taste, mouthfeel, and smell. We also have data on homebrew recipes, many of which are 'copycat' recipes of well-known, commercially distributed beers for which we have review information.


## **Communication**

Our group is communicating primarily through Discord and Slack.  We created a Google Drive folder to house shared files, and also a trello board to manage our project.
With each commit, we communcate with each member to check the information and review the code.

## **Project Outline**

### **Formulate a Question**
- We spent the first couple of classes really diving in and figuring out what question we would like to answer. We knew setting a solid foundation is key and created this our first priority.

### **Source Data**
- Once we had a question set, we researched some data sources that can help answer our question.

### **Initialize a Database**
 - We created an AWS database to house our data.  Our heroku site pulls live data from the database to populate our filterable tables.

### **Create a Machine Learning Algorithm**
- We have done preliminary linear regression on beer review data to identify which attributes of a beer contribute most to the overall review score.  We discovered that a beer's overall review score is most closely correlated to taste score.  So our ML model focuses on predicting whether or not a beer's taste score will be above (a good beer) or below (a not good beer) 4.0.  We tried a variety of Machine Learning models, and found that a Gradient Boosting Classifier resulted in a prediction model with the highest level of accuracy.

### **Presentation**
- Our team deployed a [heroku site](https://das-boot-brew-review-app.herokuapp.com/) that houses a filterable table of our beer review data, as well as many of the visuals we created using Machine Learning, and during the data cleaning process.  In addition, we have an interactive "Test Your Beer" page that allows a user to input beer recipe metrics and use our ML algorithm to determine if the reciple will proudce a 'good' or 'bad' beer.  

### **The Pitch**
- We will film a virtual 'pitch' for breweries who would like to use our team's talents and expertise, and our innovative Machine Learning algorithm to help make data-driven decisions.  A link to our static [Google Slide Deck](https://docs.google.com/presentation/d/1bLgCaShy3VGehPZgpbyOCZr1AdiEvK3gFdSeHPxAY3Y/edit?usp=sharing) is also available.


