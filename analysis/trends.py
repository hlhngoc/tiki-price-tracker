import pandas as pd

def most_volatile_products(df):
    volatility = df.groupby('product_id')['price'].std()
    volatility = volatility.to_frame()
    return volatility.sort_values(by='price', ascending=False)

def price_history(df, product_id):
    filtered = df[df['product_id'] == product_id]
    filtered = filtered.sort_values(by='timestamp', ascending=True)
    return filtered

def price_drop_alert(df, threshold):
    discount = []

    for pid in df['product_id'].unique():
        filtered = df[df['product_id'] == pid]
        filtered = filtered.sort_values(by='timestamp', ascending=True)

        first_price = filtered['price'].iloc[0]
        last_price = filtered['price'].iloc[-1]
        discount.append({'product_id': pid, 'drop_pct': ((first_price - last_price) / first_price) * 100})
    
    result = pd.DataFrame(discount)
    return result[result['drop_pct'] >= threshold]
