from curl_cffi import requests as cffi_requests
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_listings(category_id, page=1):
    """
    Fetch one page of product listings from Tiki's internal API.

    Returns:
        dict with keys "products", "current_page", "last_page" on success.
        None if the request fails or the response format is unexpected.
    """
    url = "https://tiki.vn/api/personalish/v1/blocks/listings"

    # Query params reverse-engineered from Chrome DevTools (Network tab).
    params = {
        "limit": 40,
        "category": category_id,
        "page": page,
        "urlKey": "nha-sach-tiki",
        "sort": "top_seller",
        "include": "advertisement",
        "aggregations": 2,
        "version": "home-persionalized",
        "trackity_id": "f5734d7a-e114-e105-0437-1acea0d55f9e",
    }

    if not os.getenv("TIKI_GUEST_TOKEN"):
        raise EnvironmentError("Missing TIKI_GUEST_TOKEN in .env")
    
    if not os.getenv("TIKI_COOKIE"):
        raise EnvironmentError("Missing TIKI_COOKIE in .env")
    
    # Headers required to mimic a real browser request, including
    # the guest token and cookie Tiki expects.
    headers = {
        "accept": "application/json, text/plain, */*",
        "referer": "https://tiki.vn/nha-sach-tiki/c8322",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-guest-token": os.getenv("TIKI_GUEST_TOKEN"),
        "cookie": os.getenv("TIKI_COOKIE"),
    }
    # curl_cffi with impersonate="chrome" bypasses Tiki's TLS fingerprint
    # detection, which blocks plain `requests` with a 403.
    try:
        response = cffi_requests.get(
            url,
            params=params,
            headers=headers,
            impersonate="chrome",
            timeout=15,
        )
        response.raise_for_status()

    # Each exception type is caught separately so the error message
    # printed is specific to what actually went wrong.
    except cffi_requests.exceptions.Timeout:
        print("Request timed out.")
        return None
    except cffi_requests.exceptions.ConnectionError:
        print("Connection failed.")
        return None
    except cffi_requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
    except cffi_requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    # Response might not be valid JSON (e.g. an HTML error page).
    try:
        data = response.json()
    except ValueError:
        print("Response is not valid JSON.")
        return None

    # Guard against Tiki changing their response schema silently.
    if "data" not in data:
        print("Unexpected response format.")
        return None

    results = []
    for product in data["data"]:
        product_id = product.get("id")

        # product_id is the only mandatory field: it's the primary key
        # in our DB and the foreign key linking snapshots to products.
        # Every other field can be missing (stored as NULL), but without
        # an id there's no way to track this product over time.
        if product_id is None:
            print("Skipping product because product_id is missing.")
            continue

        # Tiki sometimes returns quantity_sold as a plain number/None,
        # and sometimes as a dict like {"text": "Đã bán 11", "value": 11}.
        # Normalize to just the numeric value (or None).
        sold_count_raw = product.get("quantity_sold")
        if isinstance(sold_count_raw, dict):
            sold_count = sold_count_raw.get("value")
        else:
            sold_count = sold_count_raw
        
        impression_info = product.get('visible_impression_info')
        if impression_info:
            amplitude = impression_info.get('amplitude')
            seller_type = amplitude.get('seller_type') if amplitude else None
        else:
            seller_type = None

        results.append({
            "product_id": product_id,
            "name": product.get("name"),
            "price": product.get("price"),
            "original_price": product.get("original_price"),
            "discount_rate": product.get("discount_rate"),
            "rating": product.get("rating_average"),
            "sold_count": sold_count,
            "url": "https://tiki.vn/" + product.get("url_key", ""),
            'author_name': product.get('author_name'),
            'seller_id': product.get('seller_id'),
            'seller_type': seller_type,
            'category_path': product.get('primary_category_path'),
        })

    # Fail fast if paging info is missing, rather than letting the caller
    # crash later on a None comparison (current_page >= last_page).
    if "paging" not in data:
        print("Unexpected response format: missing paging.")
        return None

    paging = data["paging"]

    return {
        "products": results,
        "current_page": paging.get("current_page"),
        "last_page": paging.get("last_page"),
    }