# Import dependencies
from flask import Flask, render_template, redirect, jsonify
import pickle
import numpy as np
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import sys
import pandas as pd

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import config

sql_u = config.sql_u
sql_pw = config.sql_pw
sql_host = config.sql_host


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
    # queryResults = pd.DataFrame(cur.fetchall(),columns=[headers])
    # queryData = queryResults.to_dict('records')
    # columnNames = queryResults.columns.values
    

    # close sql connection
    cur.close()
    conn.close()
    print(f"queryResults: {queryResults}")
    print("")
    print("")
    # print(f"queryData: {queryData}")
    print("")
    print("")
    print(f"These are the headers: {headers}")
    return queryResults, headers

# def createJSON(data, headers):
#     jsonData=[]
#     for rec in data:
#         jsonData.append(dict(zip(headers,rec)))
#     return json.dumps(jsonData)

app = Flask(__name__)

def recipeRater(test_recipe):
    print('This is where we will test user input in ML.')
    return 0

@app.route('/')
def index():
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
            LIMIT 3;
        '''
    # run query
    results = awsDB(sql_query)
    # convert query results to json
    jsonData = createJSON(results[0], results[1])

    return render_template('index.html', data=jsonData)

@app.route('/testBeerRecipe')
def testBeerRecipe():
    print('Here we will predict if a beer is good based on user input.')
    # result = recipeRater(test_recipe)
    # print result to a textbox -- "There is a ##% probability your recipe will make a good tasting beer."
    return redirect('index.html')

@app.route('/visuals')
def visuals():
    
    return render_template('visuals.html')

@app.route('/API/<beerinfo>')
def beerFilter(beerinfo):
    beerinfo = str(beerinfo)
    # query = """SELECT * FROM reviews WHERE review_taste = '{beer}'""".format(beer = beerinfo)

    query = '''SELECT 
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
               WHERE review_taste = {beer}
               LIMIT 3;
            '''.format(beer = beerinfo)

    result = awsDB(query)
    data = result[0]
    headers = result[1]

    # print(f"Headers: {headers}")
    # print("")
    # print(f"data: {data}")

    # with open('data.js','w') as f:
    #     json.dump(resultJSON,f)

    return render_template('index.html',records = data, colnames = headers)

if __name__ == '__main__':
    app.run(debug=True)