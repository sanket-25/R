import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import requests

# Fetch data from Alpha Vantage API
ALPHA_VANTAGE_API_KEY = 'demo'
symbol = 'RELIANCE.BSE'
BASE_URL = 'https://www.alphavantage.co/query'

params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': symbol,
    'outputsize': 'full',
    'apikey': ALPHA_VANTAGE_API_KEY
}
response = requests.get(BASE_URL, params=params)
data = response.json().get('Time Series (Daily)', {})

# Convert to DataFrame
df = pd.DataFrame.from_dict(data, orient='index')
df = df.rename(columns={
    '1. open': 'open', 
    '2. high': 'high', 
    '3. low': 'low', 
    '4. close': 'close', 
    '5. volume': 'volume'
})
df = df.astype(float)
df = df.sort_index()

# Prepare training data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))

X_train = []
y_train = []

for i in range(60, len(scaled_data)):
    X_train.append(scaled_data[i-60:i, 0])
    y_train.append(scaled_data[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Build the LSTM Model
model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))

model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50))
model.add(Dropout(0.2))

model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=20, batch_size=32)

# Save the model
model.save('model.h5')
