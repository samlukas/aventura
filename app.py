from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('Home.html')

@app.route("/book", methods=['POST', 'GET'])
def book():
    if request.method == 'POST':
        print(request.form["story"])
    return render_template('index.html')
