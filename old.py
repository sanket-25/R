from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Alpha Vantage API key and base URL
ALPHA_VANTAGE_API_KEY = 'demo'  # Replace with your actual API key
BASE_URL = 'https://www.alphavantage.co/query'

@app.route('/stock-data', methods=['GET'])
def get_stock_data():
    # Get query parameters for filters
    symbol = request.args.get('symbol', 'RELIANCE.BSE')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    year = request.args.get('year')
    month = request.args.get('month')

    # Alpha Vantage API request
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',  # Added outputsize parameter
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Extracting time series data
    time_series = data.get('Time Series (Daily)', {})

    # Filter data based on provided parameters
    filtered_data = {}
    for date, info in time_series.items():
        if start_date and date < start_date:
            continue
        if end_date and date > end_date:
            continue
        if year and date[:4] != year:
            continue
        if month and date[5:7] != month:
            continue
        filtered_data[date] = info

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
