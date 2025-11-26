import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_ingredients(csv_path="ingredients.csv"):
    
    full_path = os.path.join(BASE_DIR, csv_path)
    
    try:
        df = pd.read_csv(full_path)
    except FileNotFoundError:
        # Provide a helpful error message if the file is still not found
        raise FileNotFoundError(f"CRITICAL ERROR: Could not find file at: {full_path}. Ensure {csv_path} is in the backend folder.")
    
    ingredients = {}

    for _, row in df.iterrows():
        name = row["ingredient"].strip().lower()
        ingredients[name] = {
            "price": float(row["price"]),
            "calories": float(row["calories"]),
            "protein": float(row["protein"]),
            "carbs": float(row["carbs"]),
            "fat": float(row["fat"]),
        }

    return ingredients


def parse_ingredient_amount(amount_str):
    amount_str = amount_str.strip().lower()

    if amount_str.endswith("g"):
        return {
            "amount": float(amount_str.replace("g", "")),
            "unit": "g"
        }

 
    elif "unit" in amount_str:
        num = amount_str.replace("units", "").replace("unit", "").strip()
        return {
            "amount": float(num),
            "unit": "unit"
        }

    else:
        raise ValueError(f"Unsupported ingredient amount format: {amount_str}")


def load_recipes(csv_path="recipes.csv"):

    full_path = os.path.join(BASE_DIR, csv_path)
    
    try:
        df = pd.read_csv(full_path)
    except FileNotFoundError:
        # Raise a clear error if the file isn't found
        raise FileNotFoundError(f"CRITICAL ERROR: Could not find file at: {full_path}. Ensure {csv_path} is in the backend folder.")

    recipes = []

    for _, row in df.iterrows():

        raw_ingredients = row["ingredients"].split(";")
        ing_list = []

        for item in raw_ingredients:
            name, amt = item.split(":")
            parsed = parse_ingredient_amount(amt)

            ing_list.append({
                "ingredient": name.strip().lower(),
                "amount": parsed["amount"],
                "unit": parsed["unit"]
            })

        recipe = {
            "id": row["id"].strip().lower(),
            "name": row["name"],
            "meal_type": row["meal_type"].strip().lower(),
            "diet": row["diet"].strip().lower(),
            "ingredients": ing_list
        }

        recipes.append(recipe)

    return recipes


# Debug Test
if __name__ == "__main__":
    ingredients = load_ingredients()
    recipes = load_recipes()

    print("\n=== INGREDIENTS (first 3) ===")
    for k in list(ingredients.keys())[:3]:
        print(k, ingredients[k])

    print("\n=== FIRST RECIPE ===")
    print(recipes[0])
