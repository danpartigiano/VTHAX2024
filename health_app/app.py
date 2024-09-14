#The main application file where Flask routes and views are defined.

from flask import Flask, render_template, request
from utils.input_parser import parse_user_input
from utils.ai_utils import get_meal_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        user_data = parse_user_input(user_input)
        restaurant_data = load_restaurant_data()
        recommendations = get_meal_recommendations(user_data, restaurant_data)
        return render_template('results.html', recommendations=recommendations)
    return render_template('index.html')