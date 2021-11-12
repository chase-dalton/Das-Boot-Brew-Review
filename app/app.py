# Import dependencies
from flask import Flask, render_template, redirect, request
import pickle
import os
from flask.wrappers import Request
import psycopg2
from psycopg2.extras import RealDictCursor

# creditials foir local testing
# import config
# sql_u = config.sql_u
# sql_pw = config.sql_pw
# sql_host = config.sql_host

# for heroku
sql_u = os.environ.get("sql_user", None)
sql_pw = os.environ.get("sql_pw", None)
sql_host = os.environ.get("sql_host", None)

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

def goodBeerTest(test_recipe):

    print(f'!! START GOOD BEER TEST !!')
    model_fn = './static/ml/final_ML_model.pkl'
    scaler_fn = './static/ml/beer_scaler.pkl'

    try: 
        # load the model
        print(f'!! TRY TO LOAD Final_ML_Model  !!')
        loaded_model = pickle.load(open(model_fn, 'rb'))
        print(f'!! LOADED Final_ML_Model  !!')
        # load Scaler
        print(f'!! TRY TO LOAD beer_scaler  !!')
        loaded_scaler = pickle.load(open(scaler_fn, 'rb'))
        print(f'!! LOADED beer_scaler  !!')
    except Exception as e: print(e)

    print(f'!! TEST_RECIPE = {test_recipe} !!')

    # Scale User input
    scaler = loaded_scaler
    X_test_scaled = scaler.transform(test_recipe)

    # make prediction on user input
    predict = loaded_model.predict(X_test_scaled)
    print(f'!! PREDICT = {predict} !!')
    return predict

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
            CAST(ROUND(beer_abv::numeric,2) AS FLOAT) as "ABV %"
            FROM reviews
            LIMIT 20;
        '''
    result = awsDB(sql_query)
    data = result[0]
    headers = result[1]

    return render_template('index.html',records = data, colnames = headers, err_message = error_message)

@app.route('/testBeerRecipe')
def testBeerRecipeStart():
    result_img = '/static/images/test_beer.png'
    error_message = ''
    result_message = ''
    return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

@app.route('/testBeerRecipe', methods=['POST'])
def testBeerRecipe():
    error_message = ''
    result_img = '/static/images/test_beer.png'
    result_message = ''

    # convert combobox selection to list
    brew_meth = []
    if request.form.get("brew_method") == 'all_grain':
        brew_meth = [1,0,0,0]
    elif request.form.get("brew_method") == 'biab':
        brew_meth = [0,1,0,0]
    elif request.form.get("brew_method") == 'partial_mash':
        brew_meth = [0,0,1,0]
    else:
        brew_meth = [0,0,0,1]

    og = float(request.form.get("og"))
    fg = float(request.form.get("fg"))
    ibu = float(request.form.get("ibu"))
    color = float(request.form.get("color"))
    beer_abv = float(request.form.get("beer_abv"))

    # confirm values are within proper ranges
    if og < 1 or og > 1.183:
        error_message = 'An invalid parameter was entered.  Please try again.'
        result_message = ''
        result_img = '/static/images/error_beer.png'
        return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

    if fg < 0.998 or fg > 1.039:
        error_message = 'An invalid parameter was entered.  Please try again.'
        result_message = ''
        result_img = '/static/images/error_beer.png'
        return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

    if ibu < 0 or ibu > 124.15:
        error_message = 'An invalid parameter was entered.  Please try again.'
        result_message = ''
        result_img = '/static/images/error_beer.png'
        return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

    if color < 0 or color > 50:
        error_message = 'An invalid parameter was entered.  Please try again.'
        result_message = ''
        result_img = '/static/images/error_beer.png'
        return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

    if beer_abv < 0.5 or beer_abv > 29:
        error_message = 'An invalid parameter was entered.  Please try again.'
        result_message = ''
        result_img = '/static/images/error_beer.png'
        return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

    # create user_input list to send to ML
    U_input = [og, fg, ibu, color, beer_abv]

    # append brew_method to U_input
    for i in brew_meth:
        U_input.append(i)

    # create a 2D list
    user_input = []
    user_input.append(U_input)
    print(f'!! USER_INPUT: {user_input} !!')
    try:
        result = goodBeerTest(user_input)
    except:
        print('!! ERROR RUNNING goodBeerTest FUNCTION !!')
        error_message = 'An invalid parameter was entered.  Please try again.'
        result_message = ''
        result_img = '/static/images/error_beer.png'
        return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

    if result == 0:
        error_message = ''
        result_message = 'Bad Beer!'
        result_img = '/static/images/bad_beer.png'
    else:
        error_message = ''
        result_img = '/static/images/good_beer.png'
        result_message = 'Good Beer!'
        
    return render_template('testYourBeer.html', result_image = result_img, err_message = error_message, rst_message = result_message)

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
               CAST(ROUND(beer_abv::numeric,2) AS FLOAT) as "ABV %"
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
            CAST(ROUND(beer_abv::numeric,2) AS FLOAT) as "ABV %"
            FROM reviews
            LIMIT 20;
        '''
        result = awsDB(sql_query)

    data = result[0]
    headers = result[1]

    return render_template('index.html',records = data, colnames = headers, err_message = error_message)

if __name__ == '__main__':
    app.run(debug=True)