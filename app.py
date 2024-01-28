from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_file
import main
from PIL import Image
import os

app = Flask(__name__)

chat_history = []
story_lst = []
choice = 0
prompt = ''

@app.route("/")
def home_page():
    global chat_history
    main.setup(chat_history)
    return render_template('Home.html')

@app.route("/book", methods=['POST', 'GET'])
def book():
    if request.method == 'POST':
        global prompt
        prompt = request.form["story"]
    return render_template('index.html')

@app.route('/get_story')
def get_story():
    # story = "what da heck"
    # option1 = "do this ___"
    # option2 = "or do this ___"
    # option3 = "or do this ___?"
    global chat_history
    global story_lst
    global prompt
    global choice

    if choice == 0:
        story = main.story(chat_history, story_lst, prompt=prompt)
    else:
        story = main.story(chat_history, story_lst, choice=choice)

    option1, option2, option3 = main.options(chat_history, len(story_lst))
    return jsonify(story=story, option1=option1, option2=option2, option3=option3)

@app.route('/process_choice', methods=['POST'])
def process_data():
    data_from_js = request.json  # Assuming the data is sent as JSON
    # Process the data as needed
    global choice
    choice = data_from_js["option"]
    result = {'status': 'success', 'message': 'Data received successfully'}
    return jsonify(result)

@app.route('/combine_images')
def combine_images():
    image_folder = 'static/images/'  # Change this to your image folder
    output_path = 'static/combined_images/output.jpg'

    # List all files in the image folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

    if not image_files:
        return "No image files found."

    # Combine images horizontally
    images = [Image.open(os.path.join(image_folder, img)) for img in image_files]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    combined_image = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    # Save the combined image
    combined_image.save(output_path)

    return send_file(output_path, as_attachment=True)