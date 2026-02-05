from typing import Dict, List, Optional
import requests
from django.conf import settings


def search_recipes(keyword: str, number: int = 10) -> List[Dict]:
    if not keyword:
        return []

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": settings.SPOONACULAR_API_KEY,
        "query": keyword,
        "number": number,
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException:
        return []

    return [
        {
            "title": r.get("title"),
            "id": r.get("id"),
            "image": r.get("image"),
        }
        for r in (data.get("results", []) or [])
    ]


def fetch_recipe_detail(recipe_id: int) -> Optional[Dict]:
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": settings.SPOONACULAR_API_KEY}

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException:
        return None
