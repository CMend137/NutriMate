def parse_height(height_str):
    clean = (
        height_str.lower()
        .replace("ft", " ")
        .replace("in", " ")
        .replace("'", " ")
        .replace('"', " ")
    )
    parts = clean.split()
    try:
        feet = int(parts[0])
        inches = int(parts[1]) if len(parts) > 1 else 0
    except (IndexError, ValueError):
        feet, inches = 0, 0
    return feet, inches


def calculate_calories(user_profile):
    weight_lbs = user_profile["weight_lbs"]
    height_ft = user_profile["height_ft"]
    height_in = user_profile["height_in"]
    age = user_profile["age"]
    gender = user_profile["gender"].upper()
    goal = user_profile["goal"].lower()
    activity_level = user_profile["activity_level"].lower()

    total_inches = (height_ft * 12) + height_in

    if gender == "M":
        bmr = 66 + (6.23 * weight_lbs) + (12.7 * total_inches) - (6.8 * age)
    else:
        bmr = 655 + (4.35 * weight_lbs) + (4.7 * total_inches) - (4.7 * age)

    activity_multipliers = {
        "no exercise": 1.2,
        "light exercise": 1.375,
        "moderate exercise": 1.55,
        "active": 1.725,
        "very active": 1.9
    }

    tdee = bmr * activity_multipliers.get(activity_level, 1.55)

    if goal == "lose weight":
        tdee *= 0.8
    elif goal == "gain weight (muscle)":
        tdee *= 1.15

    return round(tdee, 2)


def calculate_macros(calories):
    protein_cal = calories * 0.30
    carb_cal = calories * 0.45
    fat_cal = calories * 0.25
    return {
        "protein_g": round(protein_cal / 4, 1),
        "carbs_g": round(carb_cal / 4, 1),
        "fat_g": round(fat_cal / 9, 1)
    }
