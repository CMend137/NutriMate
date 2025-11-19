import random
from datasets import load_ingredients, load_recipes

# -------------------------------------------------------------
# CALCULATE MEAL NUTRITION + COST
# -------------------------------------------------------------
def calculate_meal_nutrition_cost(recipe, ingredients_db): 
    total_cal = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_cost = 0

    for item in recipe["ingredients"]:
        name = item["ingredient"]
        amount = item["amount"]
        unit = item["unit"]

        if name not in ingredients_db:
            raise ValueError(f"Ingredient {name} not found in database.")
        
        ing_info = ingredients_db[name]

        # ---- COST FIX ----
        # price in CSV is per 100g or per unit
        if unit == "g":
            cost = ing_info["price"] * (amount / 100)
        else:
            cost = ing_info["price"] * amount

        total_cost += cost

        # ---- NUTRITION FIX ----
        # nutrition in CSV is per 100g or per unit
        if unit == "g":
            factor = amount / 100
        else:
            factor = amount

        total_cal += ing_info["calories"] * factor
        total_protein += ing_info["protein"] * factor
        total_carbs += ing_info["carbs"] * factor
        total_fat += ing_info["fat"] * factor

    return {
    "calories": round(total_cal, 1),
    "protein": round(total_protein, 1),
    "carbs": round(total_carbs, 1),
    "fat": round(total_fat, 1),
    "cost": round(total_cost, 2)
}


# -------------------------------------------------------------
# PICK DAILY MEALS
# -------------------------------------------------------------
def pick_daily_meals(recipes, meal_type):
    options = [r for r in recipes if r["meal_type"] == meal_type]
    if not options:
        raise ValueError(f"No recipes found for meal type: {meal_type}")
    return random.choice(options)


# -------------------------------------------------------------
# BUILD WEEKLY PLAN
# -------------------------------------------------------------
def build_weekly_plan(budget): 
    ingredients_db = load_ingredients()
    recipes_db = load_recipes()

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_plan = []
    weekly_cost = 0

    for day in days:

        # pick one meal of each type
        breakfast = pick_daily_meals(recipes_db, "breakfast")
        lunch = pick_daily_meals(recipes_db, "lunch")
        dinner = pick_daily_meals(recipes_db, "dinner")

        # calculate nutrition + cost
        breakfast_data = calculate_meal_nutrition_cost(breakfast, ingredients_db)
        lunch_data = calculate_meal_nutrition_cost(lunch, ingredients_db)
        dinner_data = calculate_meal_nutrition_cost(dinner, ingredients_db)

        daily_cost = breakfast_data["cost"] + lunch_data["cost"] + dinner_data["cost"]
        weekly_cost += daily_cost

        day_plan = {
            "day": day,
            "breakfast": {"name": breakfast["name"], "data": breakfast_data},
            "lunch": {"name": lunch["name"], "data": lunch_data},
            "dinner": {"name": dinner["name"], "data": dinner_data},
            "daily_cost": daily_cost,
            "daily_calories": (
                breakfast_data["calories"] +
                lunch_data["calories"] +
                dinner_data["calories"]
            )
        }

        weekly_plan.append(day_plan)

    return {
        "weekly_plan": weekly_plan,
        "total_weekly_cost": round(weekly_cost, 2),
        "within_budget": weekly_cost <= budget
    }


# -------------------------------------------------------------
# RUN TEST (THIS PRINTS YOUR PLAN)
# -------------------------------------------------------------
if __name__ == "__main__":
    plan = build_weekly_plan(50)
    print(plan)
