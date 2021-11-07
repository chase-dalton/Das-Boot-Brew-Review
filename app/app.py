# Import dependencies
from flask import Flask, render_template, redirect, jsonify
import pickle
import numpy as np
import os
import psycopg2
import json
import sys

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
    cur = conn.cursor()
    # run query
    cur.execute(sql_query)
    queryResults = cur.fetchall()
    # get headers
    headers=[x[0] for x in cur.description] 

    # close sql connection
    cur.close()
    conn.close()
    return queryResults, headers

def createJSON(data, headers):
    jsonData=[]
    for rec in data:
        jsonData.append(dict(zip(headers,rec)))
    return json.dumps(jsonData)

app = Flask(__name__)

def recipeRater(test_recipe):
    print('This is where we will test user input in ML.')
    return 0

@app.route('/')
def index():
    # create query
    sql_query = '''SELECT *
                FROM styles;
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
               WHERE review_taste = {beer}
               LIMIT 5;
            '''.format(beer = beerinfo)

    result = awsDB(query)
    # data = [beer for beer in result if beer[0][0][0] == beerinfo]
    # print(result)
    # testlist = []
    # for x in result:
    #     testlist.append(x)

    # return jsonify(testlist[0])
    print(jsonify(result))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)