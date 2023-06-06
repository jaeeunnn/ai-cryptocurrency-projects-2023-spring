import pandas as pd

# 기존파일
original_file_path = r'C:\Users\LG\Desktop\oderbookk\2023-05-10-upbit-BTC-book.csv'

# CSV 파일 불러오기
df = pd.read_csv(original_file_path)

# 함수정의
def calculate_mid_price(row):
    asks = df.loc[(df['timestamp'] == row['timestamp']) & (df['type'] == 1), 'price']
    bids = df.loc[(df['timestamp'] == row['timestamp']) & (df['type'] == 0), 'price']
    if asks.empty or bids.empty:
        return None
    best_ask = asks.iloc[0]
    best_bid = bids.iloc[0]
    return (best_ask + best_bid) / 2

def calculate_book_imbalance(row):
    asks = df.loc[(df['timestamp'] == row['timestamp']) & (df['type'] == 1), 'quantity']
    bids = df.loc[(df['timestamp'] == row['timestamp']) & (df['type'] == 0), 'quantity']
    if asks.empty or bids.empty:
        return None
    total_ask_quantity = asks.sum()
    total_bid_quantity = bids.sum()
    return (total_ask_quantity - total_bid_quantity) / (total_ask_quantity + total_bid_quantity)

def calculate_book_delta(row):
    asks = df.loc[(df['timestamp'] == row['timestamp']) & (df['type'] == 1), 'quantity']
    bids = df.loc[(df['timestamp'] == row['timestamp']) & (df['type'] == 0), 'quantity']
    if asks.empty or bids.empty:
        return None
    best_ask_quantity = asks.iloc[0]
    best_bid_quantity = bids.iloc[0]
    return (best_ask_quantity - best_bid_quantity) / (best_ask_quantity + best_bid_quantity)

# 데이터프레임에 새로운 열 추가
df['mid price'] = df.apply(calculate_mid_price, axis=1)
df['book imbalance'] = df.apply(calculate_book_imbalance, axis=1)
df['book delta'] = df.apply(calculate_book_delta, axis=1)

# 새로운 파일명 생성
date = df['timestamp'].values[0][:10]
exchange = "upbit"
market = "BTC"
feature = "feature"
new_filename = f"{date}-{exchange}-{market}-{feature}.csv"

# 저장 경로 설정
save_path = r"C:\Users\LG\Desktop\oderbookk\polder"

# 전체 저장 경로
save_file_path = save_path + new_filename

# 새로운 CSV 파일로 저장
df.to_csv(save_file_path, index=False)

print("새로운 CSV 파일이 생성되었습니다.")
