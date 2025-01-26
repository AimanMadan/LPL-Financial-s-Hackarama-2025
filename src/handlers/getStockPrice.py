import json
import requests
import os


def lambda_handler(event, context):
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    base_url = "https://www.alphavantage.co/query"
    symbol = event.get("queryStringParameters", {}).get("symbol", "TSLA")

    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()

        time_series = data.get("Time Series (5min)", {})

        latestTime = sorted(time_series.keys())[0]
        latestPrice = time_series[latestTime]["4. close"]
        high = time_series[latestTime]["2. high"]
        low = time_series[latestTime]["3. low"]
        openPrice = time_series[latestTime]["1. open"]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "title": symbol,
                "details": [
                    {"value": latestPrice, "label": "Price"},
                    {"value": high, "label": "high"},
                    {"value": low, "label": "low"},
                    {"value": openPrice, "label": "Open"}
                ]
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }


def lambda_handler(event, context):
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "API key is not configured."})
        }

    symbol = event.get("queryStringParameters", {}).get("symbol", "TSLA")
    if not symbol:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required query parameter: symbol"})
        }

    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()

        # Check for API errors
        if "Note" in data:
            return {
                "statusCode": 429,
                "body": json.dumps({"error": "API rate limit exceeded. Try again later."})
            }
        if "Error Message" in data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Invalid symbol: {symbol}"})
            }
        if "Time Series (5min)" not in data:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"No data available for symbol: {symbol}"})
            }

        # Extract time series data
        time_series = data.get("Time Series (5min)", {})
        if not time_series:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "No time series data found."})
            }

        # Safely get the latest time
        sorted_times = sorted(time_series.keys())
        if not sorted_times:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Time series is empty."})
            }
        latest_time = sorted_times[0]
        latest_data = time_series[latest_time]

        # Extract stock details
        latest_price = latest_data.get("4. close", "N/A")
        high = latest_data.get("2. high", "N/A")
        low = latest_data.get("3. low", "N/A")
        open_price = latest_data.get("1. open", "N/A")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "title": symbol,
                "details": [
                    {"value": latest_price, "label": "Price"},
                    {"value": high, "label": "High"},
                    {"value": low, "label": "Low"},
                    {"value": open_price, "label": "Open"}
                ]
            })
        }
    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Request failed: {str(e)}"})
        }
    except KeyError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Unexpected response format: Missing key {str(e)}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
