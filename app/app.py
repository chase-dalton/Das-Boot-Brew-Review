from flask import Flask
from flask import render_template, redirect, jsonify

import os

# sql_u = os.environ.get("sql_user", None)
# sql_pw = os.environ.get("sql_pw", None)
# sql_host = os.environ.get("sql_host", None)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)