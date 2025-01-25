from src.utils.fetch_data import fetch_data
from src.utils.config import NEWS_API_KEY

def lambda_handler(event, context):
    try:
        body = event.get('body', '{}')
        stock_symbols = body.get('stockSymbols', [])

        if not stock_symbols:
            return {
                "statusCode": 400,
                "body": {"message": "Please provide at least one stock symbol."}
            }

        news_data = {}

        for symbol in stock_symbols:
            url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
            response = fetch_data(url)
            articles = response.get("articles", [])
            news_data[symbol] = [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                }
                for article in articles
            ]

        return {
            "statusCode": 200,
            "body": {"news": news_data}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"message": f"Error fetching news articles: {str(e)}"}
        }
