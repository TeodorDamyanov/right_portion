import requests # pyright: ignore[reportMissingModuleSource]
from django.conf import settings

NUTRIENT_IDS = {
    "calories": 1008,
    "protein": 1003,
    "carbs": 1005,
    "fat": 1004
}

def fetch_usda_foods(query):
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": settings.USDA_API_KEY,
        "query": query,
        "pageSize": 10,
    }

    search_res = requests.get(search_url, params=params).json()


    foods = []
    if not search_res.get("foods"):
        return foods
    for f in search_res["foods"]:
        fdc_id = f["fdcId"]

        detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
        detail_res = requests.get(detail_url, params={"api_key": settings.USDA_API_KEY}).json()

        nutrients = {k: 0 for k in NUTRIENT_IDS}

        for nutr in detail_res.get("foodNutrients", []):
            nid = nutr.get("nutrient", {}).get("id")
            for macro, nid_match in NUTRIENT_IDS.items():
                if nid == nid_match:
                    nutrients[macro] = nutr.get("amount", 0)
        foods.append({
            "name": detail_res.get("description", f.get("description", query)),
            **nutrients
        })

    return foods