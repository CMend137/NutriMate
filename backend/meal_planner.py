import random
from backend.datasets import load_ingredients, load_recipes

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

        # Cost calculation
        if unit == "g":
            cost = ing_info["price"] * (amount / 10) 
        else:
            cost = ing_info["price"] * amount

        total_cost += cost

        # Nutrition calculation
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
        raise ValueError(f"No recipes found for meal type: {meal_type}. (A critical error occurred after budget filtering.)")
        
    return random.choice(options)

# -------------------------------------------------------------
# BUILD WEEKLY PLAN
# -------------------------------------------------------------
def build_weekly_plan(budget): 
    ingredients_db = load_ingredients()
    recipes_db = load_recipes()

    # ------------------------------------------------------------------
    # 1. PRE-CALCULATE COST, FILTER, AND CREATE A NEW LIST
    # ------------------------------------------------------------------
    max_meal_cost = (budget / 7) / 3 
    
    filtered_recipes = []
    
    for original_recipe in recipes_db:
        
        data = calculate_meal_nutrition_cost(original_recipe, ingredients_db)
        
        if data['cost'] <= max_meal_cost:
            
            new_recipe = original_recipe.copy()
            new_recipe.update(data)
            filtered_recipes.append(new_recipe)
    
    recipes_to_use = filtered_recipes

    # ------------------------------------------------------------------
    # 2. ENHANCED BUDGET VALIDATION (The Fix for the Ambiguous Error)
    # ------------------------------------------------------------------
    has_breakfast = any(r["meal_type"] == "breakfast" for r in recipes_to_use)
    has_lunch = any(r["meal_type"] == "lunch" for r in recipes_to_use)
    has_dinner = any(r["meal_type"] == "dinner" for r in recipes_to_use)

    missing_meals = []
    if not has_breakfast: missing_meals.append("Breakfast")
    if not has_lunch: missing_meals.append("Lunch")
    if not has_dinner: missing_meals.append("Dinner")

    if missing_meals:
        raise ValueError(
            f"Budget Error: No affordable recipes found for the following meals: {', '.join(missing_meals)}. "
            f"Please increase your weekly budget to afford meals under ${max_meal_cost:.2f} per serving."
        )
    
    # ------------------------------------------------------------------
    # 3. PLAN GENERATION (Uses the filtered list)
    # ------------------------------------------------------------------

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_plan = []
    weekly_cost = 0

    for day in days:

        Breakfast = pick_daily_meals(recipes_to_use, "breakfast")
        Lunch = pick_daily_meals(recipes_to_use, "lunch")
        Dinner = pick_daily_meals(recipes_to_use, "dinner")

        daily_cost = Breakfast["cost"] + Lunch["cost"] + Dinner["cost"]
        weekly_cost += daily_cost

        day_plan = {
            "day": day,
            "Breakfast": {"name": Breakfast["name"], "data": Breakfast},
            "Lunch": {"name": Lunch["name"], "data": Lunch},
            "Dinner": {"name": Dinner["name"], "data": Dinner},
            "daily_cost": daily_cost,
            "daily_calories": (
                Breakfast["calories"] +
                Lunch["calories"] +
                Dinner["calories"]
            )
        }

        weekly_plan.append(day_plan)

    final_weekly_cost = round(weekly_cost, 2)

    return {
        "weekly_plan": weekly_plan,
        "total_weekly_cost": final_weekly_cost,
        "within_budget": final_weekly_cost <= budget
    }

# -------------------------------------------------------------
# GENERATE SHOPPING LIST
# -------------------------------------------------------------
def generate_shopping_list(weekly_plan):

    shopping_totals = {}

    for day_plan in weekly_plan["weekly_plan"]:
        for meal_key in ["Breakfast", "Lunch", "Dinner"]:
            recipe_data = day_plan[meal_key]["data"] 
            
            for item in recipe_data["ingredients"]:
                name = item["ingredient"].replace('_', ' ').title()
                amount = item["amount"]
                unit = item["unit"]
                
                key = f"{name}_{unit}"
                
                if key not in shopping_totals:
                    shopping_totals[key] = {"name": name, "unit": unit, "amount": 0.0}
                
                shopping_totals[key]["amount"] += amount

    shopping_list_md = "#### Shopping List\n"
    
    sorted_items = sorted(shopping_totals.values(), key=lambda x: x["name"])

    for item in sorted_items:
        if item["unit"] == "unit":
            amount_str = f"{int(round(item['amount']))} units"
        else:
            amount_str = f"{item['amount']:.1f}{item['unit']}"
            
        shopping_list_md += f"- **{item['name']}**: {amount_str}\n"

    return shopping_list_md