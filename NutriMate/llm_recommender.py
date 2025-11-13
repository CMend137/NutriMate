import google.generativeai as genai
import json
from nutrition_api import get_recipes_by_calories
from grocery_price_api import get_grocery_prices


API_KEY = "AIzaSyD7XRnKGsjoqY9RZ4clGibD8CV7jcVRet0"

genai.configure(api_key = API_KEY)

def collect_user_meals(daily_calories: int, num_recipes: int = 9):
    recipes = get_recipes_by_calories(daily_calories, number = num_recipes)
    user = []

    if not recipes:
        print("No recipes could be found.")
        return user
    
    for r in recipes:
        title = r.get("title", "Unknown meal")
        cals = r.get("calories", daily_calories)

        offers = get_grocery_prices(title, number = 3)

        best_price = None
        best_store = None
        best_link = None

        for o in offers:
            raw_price = o.get("price", "N/A")
            try:
                price_float = float(raw_price)
            except (TypeError, ValueError):
                continue

            if best_price is None or price_float < best_price:
                best_price = price_float
                best_store = o.get("store", "Unknown")
                best_link = o.get("link", "N/A")

        user.append({
            "title": title,
            "calories": cals,
            "price": best_price,
            "store": best_store,
            "link": best_link
        })

    return user 


def create_prompt(user_profile: dict, daily_calories: int, weekly_budget: float, user_meals: list):
    goal = user_profile.get("goal", "maintain weight")
    activity_level = user_profile.get("activity_level", "moderate")
    restrictions = user_profile.get("restrictions", "none")

    user_json = json.dumps(user_meals, indent = 2)
        
    daily_budget = weekly_budget / 7.0 if weekly_budget else None

    calorie_goal_type = "calorie surplus for muscle gain" if "gain" in goal.lower() or "muscle" in goal.lower() \
        else "calorie deficit for fat loss" if "lose" in goal.lower() or "loss" in goal.lower() \
        else "maintenance calories"

    prompt = f""" 
You are NutriMate, an AI meal planner in a multi-agent system. 

Upstream agents have already done the following: 
- A Nutrition Agent calculated the user's daily calorie target. 
- A Recipe Agent fetched real recipes from Spoonacular based on that calorie target. 
- A Budget Agent fetched real grocery prices for those recipes using a product search API. 

Your job as the Planner/Evaluator Agent is to:
- Use only the provided user meals.
- Build a realistic 7-day meal plan with 3 meals per day: 
    Breakfast, Lunch, and Dinner. 
- Respect the user's goal and budget. 

USER PROFILE:
- Goal: {goal}
- Activity level: {activity_level}
- Dietary restrictions: {restrictions}
- Daily calorie target (approx): {daily_calories} kcal
- Weekly budget: ${weekly_budget:.2f} (daily budget = ${daily_budget:.2f} if not None)

USER MEALS (from other agents):
Each meal contains: title, calories, price, store, link. 
Use only these meals in the final plan. You may reuse meals across multiple days. 

{user_json}

CONSTRAINTS: 
1.) Use only meals from the user list above. Do not invent new meals. 
2.) Each day must have exactly: 
    - "Breakfast"
    - "Lunch"
    - "Dinner" 
3.) Try to keep the total daily cost (Breakfast + Lunch + Dinner) at or below the daily budget 
    (= ${daily_budget:.2f}). If prices are "N/A", you can use the meal but try to balance with cheaper ones.
4.) Calorie-wise:
    - Aim for {calorie_goal_type}.
    - Daily total calories should be reasonably close to the daily target {daily_calories} kcal (within ±15% is acceptable).
5.) Respect dietary restrictions if specified (e.g. no gluten, no dairy, etc.).
6.) Make the plan varied across the week (don't always repeat the exact same three meals). 
7.) IMPORTANT: Output must be VALID JSON ONLY. No explanations, no markdown. 

OUTPUT STRUCTURE (EXAMPLE SHAPE): 
{{
  "Monday": {{
    "Breakfast": {{
      "Meal": "Chicken and Rice",
      "Calories": 550,
      "Price": 6.49,
      "Store": "Walmart",
      "Link": "https://example.com/product"
    }},
    "Lunch": {{
      "Meal": "Salmon and Quinoa",
      "Calories": 650,
      "Price": 7.99,
      "Store": "Target",
      "Link": "https://example.com/product2"
    }},
    "Dinner": {{
      "Meal": "Oatmeal and Banana",
      "Calories": 400,
      "Price": 2.25,
      "Store": "Aldi",
      "Link": "https://example.com/product3"
    }}
  }},
  "Tuesday": {{
    "Breakfast": {{ ... }},
    "Lunch": {{ ... }},
    "Dinner": {{ ... }}
  }},
  ...
  "Sunday": {{
    "Breakfast": {{ ... }},
    "Lunch": {{ ... }},
    "Dinner": {{ ... }}
  }}
}}

Now, generate ONLY the JSON object for the full 7-day meal plan.
"""
    return prompt.strip()


def call_llm(prompt: str): 
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    try:
        response = model.generate_content(prompt)
        print("🔍 DEBUG: Gemini response received.")
        text = getattr(response, "text", None)

        if not text:
            print("⚠️ Gemini returned no text. Possibly invalid API key or rate limit reached.")
            return {"error": "No response from Gemini. Check API key or quota."}

        text = text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(text)
            return parsed
        except json.JSONDecodeError:
            print("⚠️ JSON parsing failed. Attempting cleanup...")
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                cleaned = text[start:end+1]
                return json.loads(cleaned)
            else:
                print("❌ Gemini output malformed.")
                return {"error": "Malformed Gemini output"}

    except Exception as e:
        print(f"❌ LLM call failed: {e}")
        return {"error": str(e)}


def generate_meal_plan(user_profile: dict, daily_calories: int, weekly_budget: float): 
    user = collect_user_meals(daily_calories, num_recipes = 9)

    if not user:
        print("No user meals available. Cannot generate plan.")
        return {}

    prompt = create_prompt(user_profile, daily_calories, weekly_budget, user)

    plan = call_llm(prompt)

    return plan


#DELETE THIS WHEN FRONTEND IS READY
# ------------------------------------------------------------
if __name__ == "__main__":
    # Example user profile for quick testing.
    # In your real app, you'll pass the one created in main.py.
    test_user = {
        "name": "Test User",
        "age": 25,
        "gender": "M",
        "height_ft": 5,
        "height_in": 8,
        "weight_lbs": 180,
        "goal": "gain weight (muscle gain)",
        "activity_level": "moderate",
        "restrictions": "none"
    }

    # Example daily calories and weekly budget
    example_daily_calories = 2600
    example_weekly_budget = 120.0  # $120/week

    weekly_plan = generate_meal_plan(test_user, example_daily_calories, example_weekly_budget)
    print("\n✅ Gemini Meal Plan Generated Successfully!\n")
    print(json.dumps(weekly_plan, indent=2))