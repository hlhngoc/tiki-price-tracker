from curl_cffi import requests as cffi_requests
import time


def fetch_listings(category_id, page=1):
    url = "https://tiki.vn/api/personalish/v1/blocks/listings"
    
    params = {
        "limit": 40,
        "category": category_id,
        "page": page,
        "urlKey": "laptop",
        "sort": "top_seller",
        "include": "advertisement",
        "aggregations": 2,
        "version": "home-persionalized",
        "trackity_id": "b0256c5e-7956-331e-052a-172282a630d5",
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "referer": "https://tiki.vn/laptop/c8095",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-guest-token": "***REMOVED***",
        "cookie": "TOKENS={%22access_token%22:%22***REMOVED***%22}; _trackity=b0256c5e-7956-331e-052a-172282a630d5; delivery_zone=Vk4wMzkwMDYwMDE=",
    }

    # Handle network/timeout errors
    try:
        response = cffi_requests.get(
            url,
            params=params,
            headers=headers,
            impersonate="chrome",
            timeout=15,
        )
        response.raise_for_status()
    except cffi_requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    # Handle invalid JSON response
    try:
        data = response.json()
    except ValueError:
        print("Response is not valid JSON.")
        return []

    results = []
    for product in data.get("data", []):
        results.append(
            {
                "product_id": product.get("id", None),
                "name": product.get("name", None),
                "price": product.get("price", None),
                "original_price": product.get("original_price", None),
                "discount_rate": product.get("discount_rate", None),
                "rating": product.get("rating_average", None),
                "sold_count": product.get("quantity_sold", None),
                "url": "https://tiki.vn/" + product.get("url_key", ""),
            }
        )
    return results


if __name__ == "__main__":
    all_data = []
    for page in range(1, 6):
        data = fetch_listings(8095, page)
        all_data.extend(data)
        # Wait 1 second before the next request

        if page < 5:
            time.sleep(1)
    if all_data:
        print(all_data[0])