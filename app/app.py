# Import dependencies
from flask import Flask, render_template, redirect, jsonify
# import pickle
# import numpy as np
import os
import psycopg2
<<<<<<< HEAD
from psycopg2.extras import RealDictCursor
# import json
# import sys


# for local:
# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# import config

# sql_u = config.sql_u
# sql_pw = config.sql_pw
# sql_host = config.sql_host

# for heroku
sql_u = os.environ.get("sql_user", None)
sql_pw = os.environ.get("sql_pw", None)
sql_host = os.environ.get("sql_host", None)
=======
import json
import sys

# sql credentials stored on heroku
# sql_u = os.environ.get("sql_user", None)
# sql_pw = os.environ.get("sql_pw", None)
# sql_host = os.environ.get("sql_host", None)

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import config

sql_u = config.sql_u
sql_pw = config.sql_pw
sql_host = config.sql_host
>>>>>>> 498bcb0 (update sql to cast numeric fields as float to remove 'Decimal' from results)


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
<<<<<<< HEAD
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
            LIMIT 5;
        '''
    result = awsDB(sql_query)
    data = result[0]
    headers = result[1]

    return render_template('index.html',records = data, colnames = headers)
=======
    # # create query
    # sql_query = '''SELECT *
    #             FROM styles;
    #             '''
    # # run query
    # results = awsDB(sql_query)
    # # convert query results to json
    # jsonData = createJSON(results[0], results[1])

    # return render_template('index.html', data=jsonData)
    return render_template('index.html')
>>>>>>> 498bcb0 (update sql to cast numeric fields as float to remove 'Decimal' from results)

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
<<<<<<< HEAD

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
               WHERE review_taste = {beer}
               LIMIT 3;
            '''.format(beer = beerinfo)

    result = awsDB(sql_query)
    data = result[0]
    headers = result[1]

    return render_template('index.html',records = data, colnames = headers)
=======
    # query = """SELECT * FROM reviews WHERE review_taste = '{beer}'""".format(beer = beerinfo)

    query = '''SELECT id::float AS id,
               brewery_name,
               beer_style,
               brewery_id::float AS brewery_id,
               review_overall::float AS review_overall,
               review_aroma::float AS review_aroma,
               review_appearance::float AS review_appearance,
               review_palate::float AS review_palate,
               review_taste::float AS review_taste,
               beer_abv::float AS beer_abv,
               beer_beerid,
               beer_name,
               review_count::float AS review_count
               FROM reviews
               WHERE review_taste = {beer};
            '''.format(beer = beerinfo)

    result = awsDB(query)
    # data = [beer for beer in result if beer[0][0][0] == beerinfo]
    # print(result)
    testlist = []
    for x in result:
        testlist.append(str(x))

    return jsonify(testlist[0])
>>>>>>> 498bcb0 (update sql to cast numeric fields as float to remove 'Decimal' from results)

if __name__ == '__main__':
    app.run(debug=True)