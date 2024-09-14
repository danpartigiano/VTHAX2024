# utils/diversity_index.py

import openai
import os
import json

openai.api_key = os.getenv('OPENAI_API_KEY')

def analyze_diversity_inclusion(text):
    prompt = f"""
You are an expert in evaluating business practices related to diversity and inclusion.

Based on the following information, evaluate the business's practices and provide ratings on a scale from 1 to 5 (1 being very low and 5 being excellent) for each of the following categories:

- Ownership Diversity
- Staff Diversity
- Inclusivity Practices
- Community Engagement

Return the ratings and brief justifications as a JSON object in the following format:

{{
  "Ownership Diversity": {{
    "rating": <number>,
    "justification": "<text>"
  }},
  "Staff Diversity": {{
    "rating": <number>,
    "justification": "<text>"
  }},
  "Inclusivity Practices": {{
    "rating": <number>,
    "justification": "<text>"
  }},
  "Community Engagement": {{
    "rating": <number>,
    "justification": "<text>"
  }}
}}

Ensure the JSON is properly formatted.

Information to analyze:
{text}
"""
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        analysis = response['choices'][0]['message']['content'].strip()
        return analysis
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def parse_analysis(analysis_text):
    try:
        # Clean up the response in case there is text before or after the JSON
        json_start = analysis_text.find('{')
        json_end = analysis_text.rfind('}') + 1
        json_str = analysis_text[json_start:json_end]
        ratings = json.loads(json_str)
        return ratings
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None

def compute_diversity_index(ratings):
    weights = {
        'Ownership Diversity': 0.25,
        'Staff Diversity': 0.25,
        'Inclusivity Practices': 0.25,
        'Community Engagement': 0.25
    }
    total_score = 0
    for category, data in ratings.items():
        rating = data.get('rating', 0)
        total_score += rating * weights.get(category, 0)
    diversity_index = total_score
    return round(diversity_index, 2)
