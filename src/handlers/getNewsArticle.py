import json
import requests
import os

def lambda_handler(event, context):
    base_url = "https://newsapi.org/v2/everything"
    api_key = os.getenv('NEWS_API_KEY')

    try:
        # Parse query parameters
        symbols = event.get('queryStringParameters', {}).get('symbols', 'TSLA').split(',')

        if not symbols:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Please provide at least one stock symbol."})
            }

        news_data = {}

        for symbol in symbols:
            headers = {"X-Api-Key": api_key}
            url = f"{base_url}?q={symbol}"

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            articles = data.get("articles", [])
            totalResults = data.get("totalResults")
            news_data[symbol] = [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                } for article in articles
            ]

        return {
            "statusCode": 200,
            "totalResults": totalResults,
            "body": json.dumps({"news": news_data})
        }

    except Exception as e:
        print(f"Error: {e}")  # Log the exception
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error fetching news articles: {str(e)}"})
        }
