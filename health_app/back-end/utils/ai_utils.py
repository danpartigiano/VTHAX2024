import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_meal_recommendations(user_data, restaurant_data):
    prompt = f"User goals: {user_data}\nAvailable meals: {restaurant_data}\nRecommend meals that help achieve the user's goals."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    recommendations = response.choices[0].text.strip()
    return recommendations