from src.utils.fetch_data import fetch_data
from src.utils.config import STOCK_API_KEY

def lambda_handler(event, context):
    try:
        body = event.get('body', '{}')
        stock_symbols = body.get('stockSymbols', [])

        if not stock_symbols:
            return {
                "statusCode": 400,
                "body": {"message": "Please provide at least one stock symbol."}
            }

        stock_prices = []
        for symbol in stock_symbols:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={STOCK_API_KEY}"
            response = fetch_data(url)
            price = response.get("Global Quote", {}).get("05. price")
            stock_prices.append({"symbol": symbol, "price": price, "currency": "USD"})

        return {
            "statusCode": 200,
            "body": {"stockPrices": stock_prices}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"message": f"Error fetching stock prices: {str(e)}"}
        }
