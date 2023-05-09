import os
import requests
import time
import pandas as pd
from datetime import datetime, timedelta

def get_orderbook():
    url = 'https://api.bithumb.com/public/orderbook/BTC'
    response = requests.get(url)
    data = response.json()
    return data

def save_to_csv(orderbook, file_path):
    timestamp = datetime.now()
    date = timestamp.strftime('%Y-%m-%d')
    filename = f'{date}-bithumb-BTC-orderbook.csv'
    file = os.path.join(file_path, filename)

    bids = orderbook['data']['bids']
    asks = orderbook['data']['asks']

    df = pd.DataFrame({'Price': [], 'Quantity': [], 'Type': [], 'Timestamp': []})
    for bid in bids:
        df = df._append({'Price': bid['price'], 'Quantity': bid['quantity'], 'Type': 0, 'Timestamp': timestamp}, ignore_index=True)
    for ask in asks:
        df = df._append({'Price': ask['price'], 'Quantity': ask['quantity'], 'Type': 1, 'Timestamp': timestamp}, ignore_index=True)

    # 파일저장
    df.to_csv(file, mode='a', index=False, header=not os.path.exists(file))

file_path = r'C:\Users\신철우\Desktop\justtest'  

while True:
    orderbook = get_orderbook()
    save_to_csv(orderbook, file_path)
    print(orderbook)  

    time.sleep(1)

    # 24시간마다새로운파일에저장
    current_time = datetime.now()
    if current_time.hour == 0 and current_time.minute == 0 and current_time.second == 0:
        file_path = r'C:\Users\신철우\Desktop\justtest'  
