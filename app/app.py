# Import dependencies
from flask import Flask, render_template, redirect, jsonify
import pickle
import numpy as np
import os
import psycopg2
import json
from config import sql_host, sql_pw, sql_u

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

if __name__ == '__main__':
    app.run(debug=True)