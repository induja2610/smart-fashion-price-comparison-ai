import os
import requests
from dotenv import load_dotenv

load_dotenv()
CATEGORY_QUERIES = {
    "shirt_men": "men shirts",
    "shirt_women": "women shirts",
    "tshirt_men": "men tshirts",
    "tshirt_women": "women tshirts",
    "tshirt_kids_boy": "boys tshirts",
    "tshirt_kids_girl": "girls tshirts",
    "footwear": "shoes",
    "skincare": "skincare products"
}


def get_live_prices(category):
    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise RuntimeError("SerpApi API key is not set.")

    query = CATEGORY_QUERIES.get(category)

    if not query:
        return []

    response = requests.get(
        "https://serpapi.com/search.json",
        params={
            "engine": "google_shopping",
            "q": query,
            "location": "India",
            "hl": "en",
            "gl": "in",
            "api_key": api_key
        },
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"])

    products = data.get("shopping_results", [])
    prices = []

    for item in products[:10]:
        prices.append({
            "store": item.get("source", "Unknown store"),
            "price": item.get("price", "Price unavailable"),
            "url": (
                item.get("product_link")
                or item.get("link")
                or ""
            ),
            "title": item.get("title", "Fashion product")
        })

    return prices