from curl_cffi import requests as cffi_requests


def fetch_listings(category_id, page = 1):
    url = "https://tiki.vn/api/personalish/v1/blocks/listings"
    params = {
        "limit": 40,
        "category": category_id,
        "page": page,
        "urlKey": 'laptop',
        "sort": "top_seller",
        'include': "advertisement",
        'aggregations': 2,
        'version': 'home-persionalized',
        'trackity_id': 'b0256c5e-7956-331e-052a-172282a630d5'
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "referer": "https://tiki.vn/laptop/c8095",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-guest-token": "***REMOVED***",
        "cookie": "TOKENS={%22access_token%22:%22***REMOVED***%22}; _trackity=b0256c5e-7956-331e-052a-172282a630d5; delivery_zone=Vk4wMzkwMDYwMDE=",
    }
    response = cffi_requests.get(url, params=params, headers=headers, impersonate="chrome")

    results = []
    data = response.json()

    for product in data['data']:
        
        results.append(
        {
            'product_id' : product['id'],
            'name' :product['name'],
            'price': product['price'],
            'original_price': product['original_price'],
            'discount_rate': product['discount_rate'],
            'rating': product['rating_average'],
            'sold_count': product['quantity_sold'],
            'url': "https://tiki.vn/" + product['url_key']
        }
    )
    return results

if __name__ == "__main__":
    data = fetch_listings(8095)
    print(data[0])

