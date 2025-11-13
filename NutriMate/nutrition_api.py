import requests

API_KEY = "447d426b22434bf5a431a599746d48f3"

def get_recipes_by_calories(target_calories, number=5):
    url = "https://api.spoonacular.com/recipes/findByNutrients"
    params = {
        "apiKey": API_KEY,
        "minCalories": 0,
        "maxCalories": target_calories + 2000,
        "minProtein": 5,
        "number": number,
        "random": True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return []

        data = response.json()
        if isinstance(data, dict) and "message" in data:
            print(f"Spoonacular error: {data['message']}")
            return []

        if not data:
            print("No recipes returned — try adjusting calorie range.")
            return []

        print(f"Retrieved {len(data)} recipes.")
        return data

    except Exception as e:
        print(f"Exception occurred while calling Spoonacular: {e}")
        return []
