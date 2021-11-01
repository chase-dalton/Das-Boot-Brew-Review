from flask import Flask
from flask import render_template, redirect, jsonify
import pickle
import numpy as np
import os

# sql_u = os.environ.get("sql_user", None)
# sql_pw = os.environ.get("sql_pw", None)
# sql_host = os.environ.get("sql_host", None)

app = Flask(__name__)

# def recipeRater(test_recipe):
    # testRecipe = np.array(test_recipe).reshape(1, 5)
    # loaded_model = pickle.load(open("final_ML_model.pkl", "rb"))
    # result = loaded_model.predict(testRecipe)
    # return result[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testBeerRecipe')
def testBeerRecipe():

    # result = recipeRater(test_recipe)
    # print result to a textbox
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)