from nutrition_api import get_recipes_by_calories
from grocery_price_api import get_grocery_prices

# === SPOONACULAR TEST ===
print("=== SPOONACULAR TEST ===")
target_calories = 500
recipes = get_recipes_by_calories(target_calories)

if recipes:
    for r in recipes[:5]:
        print(f"{r['title']} - {r['calories']} kcal")
else:
    print("No recipes found.")

# === GROCERY API TEST ===
print("\n=== GROCERY API TEST ===")
query = "chicken breast"
groceries = get_grocery_prices(query)

if groceries:
    for g in groceries[:5]:
        name = g.get("names", g.get("title", "Unknown item"))
        price = g.get("price", "N/A")
        store = g.get("store", "Unknown")
        link = g.get("link", "N/A")

        print(f"{name} - {price} - {store}")
        print(f"Link: {link}\n")
else:
    print("No grocery data found.")
