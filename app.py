from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('Home.html')

@app.route("/book", methods=['POST', 'GET'])
def book():
    if request.method == 'POST':
        print(request.form["story"])
    return render_template('index.html')

@app.route('/get_story')
def get_story():
    story = "what da heck"
    option1 = "do this ___"
    option2 = "or do this ___"
    option3 = "or do this ___?"
    return jsonify(story=story, option1=option1, option2=option2, option3=option3)

@app.route('/process_choice', methods=['POST'])
def process_data():
    data_from_js = request.json  # Assuming the data is sent as JSON
    # Process the data as needed
    print(data_from_js["option"])
    result = {'status': 'success', 'message': 'Data received successfully'}
    return jsonify(result)