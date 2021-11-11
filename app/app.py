# Import dependencies
from flask import Flask, render_template, redirect, request
# import pickle
# import numpy as np
import os
from flask.wrappers import Request
import psycopg2
from psycopg2.extras import RealDictCursor
# import json
# import sys


# for local:
# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

import config

sql_u = config.sql_u
sql_pw = config.sql_pw
sql_host = config.sql_host

# for heroku
# sql_u = os.environ.get("sql_user", None)
# sql_pw = os.environ.get("sql_pw", None)
# sql_host = os.environ.get("sql_host", None)


def awsDB(sql_query):
    # connect to DB
    conn = psycopg2.connect(
        host=sql_host,
        port='5432',
        database='postgres',
        user=sql_u,
        password=sql_pw)

    #create cursor
    cur = conn.cursor(cursor_factory= RealDictCursor)
    # run query
    cur.execute(sql_query)
    # get headers
    headers=list([x[0] for x in cur.description]) 
    queryResults = cur.fetchall()
    

    # close sql connection
    cur.close()
    conn.close()

    return queryResults, headers



app = Flask(__name__)

def recipeRater(test_recipe):
    print('This is where we will test user input in ML.')
    return 0

@app.route('/')
def index():
    error_message = ''
    # create query
    sql_query = '''SELECT 
            beer_name as "Beer",
            brewery_name as "Brewery",
            beer_style as "Style",
            CAST(ROUND(review_overall::numeric,2) AS FLOAT) as "Overall Rating",
            CAST(ROUND(review_aroma::numeric,2) AS FLOAT) as "Aroma",
            CAST(ROUND(review_appearance::numeric,2) AS FLOAT) as "Appearance",
            CAST(ROUND(review_palate::numeric,2) AS FLOAT) as "Palate",
            CAST(ROUND(review_taste::numeric,2) AS FLOAT) as "Taste",
            beer_abv::float AS "ABV %"
            FROM reviews
            LIMIT 50;
        '''
    result = awsDB(sql_query)
    data = result[0]
    headers = result[1]

    return render_template('index.html',records = data, colnames = headers, err_message = error_message)

@app.route('/testBeerRecipe')
def testBeerRecipe():
    print('Here we will predict if a beer is good based on user input.')
    # result = recipeRater(test_recipe)
    # print result to a textbox -- "There is a ##% probability your recipe will make a good tasting beer."
    return redirect('index.html')

@app.route('/visuals')
def visuals():
    
    return render_template('visuals.html')

@app.route('/', methods=['POST'])
def beerFilter():
    error_message = ''
    sql_select = '''SELECT 
               beer_name as "Beer",
               brewery_name as "Brewery",
               beer_style as "Style",
               CAST(ROUND(review_overall::numeric,2) AS FLOAT) as "Overall Rating",
               CAST(ROUND(review_aroma::numeric,2) AS FLOAT) as "Aroma",
               CAST(ROUND(review_appearance::numeric,2) AS FLOAT) as "Appearance",
               CAST(ROUND(review_palate::numeric,2) AS FLOAT) as "Palate",
               CAST(ROUND(review_taste::numeric,2) AS FLOAT) as "Taste",
               beer_abv::float AS "ABV %"
               FROM reviews
            '''
    user_input = {'beer_name':request.form.get("beer_name"), 'brewery_name':request.form.get("brewery_name"), 'beer_style': request.form.get("beer_style"),
    'review_overall':request.form.get("review_overall"), 'review_aroma':request.form.get("review_aroma"), 'review_appearance': request.form.get("review_appearance"),
    'review_palate':request.form.get("review_palate"), 'review_taste':request.form.get("review_taste"), 'beer_abv':request.form.get("beer_abv")}

    sql_where = ''

    for key, value in user_input.items():
            if value != '':
                if sql_where == '':
                    sql_where = f"WHERE {key} = '{value}'"
                else:
                    sql_where = sql_where + f" AND {key} = '{value}'"

    sql_query = sql_select + sql_where

    print (sql_query)
    try:
        result = awsDB(sql_query)

    except: 
        error_message = 'An invalid parameter was entered.  Please try again.'
        sql_query = '''SELECT 
            beer_name as "Beer",
            brewery_name as "Brewery",
            beer_style as "Style",
            CAST(ROUND(review_overall::numeric,2) AS FLOAT) as "Overall Rating",
            CAST(ROUND(review_aroma::numeric,2) AS FLOAT) as "Aroma",
            CAST(ROUND(review_appearance::numeric,2) AS FLOAT) as "Appearance",
            CAST(ROUND(review_palate::numeric,2) AS FLOAT) as "Palate",
            CAST(ROUND(review_taste::numeric,2) AS FLOAT) as "Taste",
            beer_abv::float AS "ABV %"
            FROM reviews
            LIMIT 50;
        '''
        result = awsDB(sql_query)

    data = result[0]
    headers = result[1]

    return render_template('index.html',records = data, colnames = headers, err_message = error_message)

if __name__ == '__main__':
    app.run(debug=True)