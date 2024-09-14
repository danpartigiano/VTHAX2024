# utils/ai_utils.py

import openai
import os
import json

openai.api_key = os.getenv('OPENAI_API_KEY')

# utils/ai_utils.py

# utils/ai_utils.py

import openai
import os
import json

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_personalized_recommendations(user_preferences, organic_locations):
    location_names = [loc['name'] for loc in organic_locations]
    prompt = f"""
You are an assistant that provides personalized organic food recommendations.

Based on the user's preferences: {user_preferences}, recommend the best organic food locations from the following list:

{location_names}

Return the recommendations as a JSON array in the following format:

[
  {{
    "name": "Restaurant Name",
    "reason": "Reason for recommendation"
  }},
  ...
]

Only provide the JSON output.
"""
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        recommendations_json = response['choices'][0]['message']['content'].strip()
        return recommendations_json
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def parse_recommendations(recommendations_json):
    try:
        recommendations = json.loads(recommendations_json)
        return recommendations
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
