from utils import calculate_calories, calculate_macros, parse_height 

def main(): 
    print("Welcome to NutriMate: Your AI Diet Assistant")

    height_str = input("Enter your height: ")
    height_ft, height_in = parse_height(height_str)

    user_profile = {
        "name": input("Enter your name: "),
        "age": int(input("Enter your age:")),
        "gender": input("Enter your gender: ").strip.upper(), 
        "height_ft": height_ft,
        "height_in": height_in, 
        "weight_lbs": float(input("Enter your weight (in pounds)")), 
        "goal": input("What's your goal? (Lose weight (fat loss)/ Maintain weight (muscle retention) / Gain weight (muscle gain))").lower(),
        "activity_level": input("Choose your activity level: Sedentary, Light, Moderate, Active, Very Active): ").lower(), 
    }

    print("\nCalculating your daily calorie and macro needs...")
    daily_calories = calculate_calories(user_profile)
    macros = calculate_macros(daily_calories)

    print(f"\n Daily Calorite Target: {daily_calories} kcal")
    print(f"Protien: {macros['protein_g']}g | Carbs: {macros['carbs_g']}g | Fats: {macros['fat_g']}g\n")