import requests

API_KEY = "e444b6af3bmshcfd08312747b6a4p18182cjsn4769cd3926fe" 

def get_grocery_prices(query, number=5):
    """
    Fetches real grocery/product prices using the Real-Time Product Search API (search-light-v2).
    Correctly parses the nested JSON structure (data -> products).
    """
    url = "https://real-time-product-search.p.rapidapi.com/search-light-v2"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "real-time-product-search.p.rapidapi.com"
    }
    params = {
        "q": query,
        "country": "us",
        "language": "en",
        "page": "1",
        "limit": str(number),
        "sort_by": "BEST_MATCH",
        "product_condition": "ANY",
        "return_filters": "false"
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        print("DEBUG status:", r.status_code)

        if r.status_code == 200:
            data = r.json()

            # ✅ Correct path: data → products
            products = data.get("data", {}).get("products", [])

            if not products:
                print("DEBUG: No products found, raw response:", data)
                return []

            results = []
            for p in products[:number]:
                results.append({
                    "names": p.get("product_title", "Unknown item"),
                    "price": p.get("price", "N/A"),
                    "store": p.get("store_name", "Unknown"),
                    "link": p.get("product_offer_page_url", "N/A")
                })

            return results

        else:
            print(f"Error {r.status_code}: Could not fetch grocery data.")
            print("DEBUG response:", r.text)
            return []

    except Exception as e:
        print("Request failed:", e)
        return []
