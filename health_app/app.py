# app.py

import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv

from utils.data_fetcher import get_organic_locations, fetch_business_info
from utils.ai_utils import get_personalized_recommendations, parse_recommendations
from utils.diversity_index import analyze_diversity_inclusion, parse_analysis, compute_diversity_index
from utils.location_utils import get_location_by_place_id, save_user_feedback, update_diversity_index

app = Flask(__name__)
load_dotenv()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-organic-locations', methods=['POST'])
def get_locations():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    user_preferences = data.get('preferences', '')

    # Fetch organic locations
    organic_locations = get_organic_locations(latitude, longitude)

    # For each location, fetch and analyze diversity information
    for location in organic_locations:
        website_url = location.get('website')
        if website_url:
            text = fetch_business_info(website_url)
            if text:
                analysis = analyze_diversity_inclusion(text)
                if analysis:
                    ratings = parse_analysis(analysis)
                    if ratings:
                        diversity_index = compute_diversity_index(ratings)
                        location['diversity_index'] = diversity_index
                        location['diversity_ratings'] = ratings
                    else:
                        location['diversity_index'] = None
                        location['diversity_ratings'] = None
                else:
                    location['diversity_index'] = None
                    location['diversity_ratings'] = None
            else:
                location['diversity_index'] = None
                location['diversity_ratings'] = None
        else:
            location['diversity_index'] = None
            location['diversity_ratings'] = None

    # Get AI-powered recommendations
    recommendations_json = get_personalized_recommendations(user_preferences, organic_locations)
    recommendations = parse_recommendations(recommendations_json)

    # Map recommendations to include place_ids
    recommendations_list = []
    for rec in recommendations:
        # Find the corresponding location
        for loc in organic_locations:
            if loc['name'] == rec['name']:
                rec['place_id'] = loc['place_id']
                rec['diversity_index'] = loc.get('diversity_index')
                recommendations_list.append(rec)
                break

    return render_template('recommendations.html', recommendations=recommendations_list)

@app.route('/location/<place_id>')
def location_details(place_id):
    location = get_location_by_place_id(place_id)
    return render_template('details.html', location=location)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    place_id = request.form.get('place_id')
    diversity_rating = int(request.form.get('diversity_rating'))
    comments = request.form.get('comments')

    # Save feedback to the database or data storage
    save_user_feedback(place_id, diversity_rating, comments)

    # Optionally, update the diversity index based on user feedback
    update_diversity_index(place_id)

    return redirect(url_for('location_details', place_id=place_id))

if __name__ == '__main__':
    app.run(debug=True)
