import streamlit as st
from assets import colors


def show():
    st.set_page_config(
        page_title="NutriMate - Meal Plan",
        page_icon="assets/logo.png",
    )

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {colors.LIME_GREEN} 0%, {colors.GREEN} 100%);
            color: {colors.BLACK};
        }}

        .stButton>button {{
            background-color: {colors.BACKGROUND};
            color: black;
            height: 45px;
            width: 180px;
            font-size: 20px;
            border-radius: 10px;
            transition: all 0.3s ease-in-out;
            margin-top: 10px;
        }}

        .stButton>button:hover {{
            background-color: {colors.DARK_PURPLE};
            color: white;
            transform: scale(1.05);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background-color: {colors.BACKGROUND};
        }}

        [data-testid="stSidebar"] * {{
            color: black;
        }}

        .meal-card {{
            background-color: {colors.BACKGROUND};
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            margin-bottom: 20px;
        }}

        .meal-card h4 {{
            color: {colors.DARK_PURPLE};
            margin-bottom: 8px;
        }}

        .meal-card p {{
            margin: 0;
            font-size: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Sidebar ---
    st.sidebar.image("assets/logo.png", width=200)
    st.sidebar.title("Menu")
    menu_choice = st.sidebar.radio(
        "Navigate",
        ["Weekly Plan", "Nutrition Summary", "Shopping List"]
    )

    st.title("Your Personalized Meal Plan")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # --- Sample Data ---
    sample_meals = [
        {"Breakfast": "Oatmeal with Berries", "Lunch": "Grilled Chicken Salad", "Dinner": "Salmon with Veggies"},
        {"Breakfast": "Avocado Toast", "Lunch": "Turkey Wrap", "Dinner": "Beef Stir Fry"},
        {"Breakfast": "Smoothie Bowl", "Lunch": "Quinoa Salad", "Dinner": "Chicken Fajitas"},
        {"Breakfast": "Egg Whites & Toast", "Lunch": "Shrimp Tacos", "Dinner": "Pasta Primavera"},
        {"Breakfast": "Greek Yogurt & Fruit", "Lunch": "Burrito Bowl", "Dinner": "Grilled Steak"},
        {"Breakfast": "Pancakes", "Lunch": "Tuna Sandwich", "Dinner": "Veggie Curry"},
        {"Breakfast": "Scrambled Eggs", "Lunch": "Chicken Caesar Salad", "Dinner": "Sushi Night"},
    ]

    nutrition_summary = [
        {"Calories": 1800, "Protein": 95, "Carbs": 200, "Fat": 60},
        {"Calories": 1900, "Protein": 100, "Carbs": 210, "Fat": 65},
        {"Calories": 1750, "Protein": 90, "Carbs": 190, "Fat": 55},
        {"Calories": 1850, "Protein": 95, "Carbs": 205, "Fat": 60},
        {"Calories": 2000, "Protein": 110, "Carbs": 220, "Fat": 70},
        {"Calories": 1950, "Protein": 85, "Carbs": 230, "Fat": 65},
        {"Calories": 1800, "Protein": 95, "Carbs": 200, "Fat": 60},
    ]

    ingredients = {
        "Oatmeal with Berries": ["Oats", "Blueberries", "Almond milk", "Honey"],
        "Grilled Chicken Salad": ["Chicken breast", "Lettuce", "Tomato", "Cucumber", "Olive oil"],
        "Salmon with Veggies": ["Salmon", "Broccoli", "Carrots", "Olive oil", "Garlic"],
        "Avocado Toast": ["Avocado", "Whole grain bread", "Lime", "Salt", "Pepper"],
        "Turkey Wrap": ["Turkey slices", "Tortilla", "Lettuce", "Cheese"],
        "Beef Stir Fry": ["Beef strips", "Soy sauce", "Bell peppers", "Rice"],
        "Smoothie Bowl": ["Banana", "Spinach", "Protein powder", "Almond milk"],
        "Quinoa Salad": ["Quinoa", "Tomatoes", "Cucumber", "Feta cheese"],
        "Chicken Fajitas": ["Chicken breast", "Bell peppers", "Onion", "Tortilla"],
        "Egg Whites & Toast": ["Egg whites", "Whole grain bread", "Spinach"],
        "Shrimp Tacos": ["Shrimp", "Cabbage", "Tortilla", "Lime"],
        "Pasta Primavera": ["Pasta", "Zucchini", "Tomatoes", "Parmesan"],
        "Greek Yogurt & Fruit": ["Greek yogurt", "Strawberries", "Granola"],
        "Burrito Bowl": ["Rice", "Black beans", "Chicken", "Corn", "Avocado"],
        "Grilled Steak": ["Steak", "Asparagus", "Olive oil"],
        "Pancakes": ["Flour", "Eggs", "Milk", "Maple syrup"],
        "Tuna Sandwich": ["Tuna", "Bread", "Lettuce", "Mayo"],
        "Veggie Curry": ["Chickpeas", "Coconut milk", "Curry paste", "Spinach"],
        "Scrambled Eggs": ["Eggs", "Butter", "Milk"],
        "Chicken Caesar Salad": ["Chicken", "Romaine lettuce", "Caesar dressing", "Croutons"],
        "Sushi Night": ["Rice", "Seaweed", "Salmon", "Soy sauce"]
    }

    # --- PAGE LOGIC ---
    if menu_choice == "Weekly Plan":
        st.markdown("Here’s your weekly meal plan with nutrition info for each day.")
        for i, day in enumerate(days):
            with st.container():
                st.markdown(f"<div class='meal-card'><h4>{day}</h4>", unsafe_allow_html=True)
                st.markdown(f"""
                <p><strong>Breakfast:</strong> {sample_meals[i]['Breakfast']}</p>
                <p><strong>Lunch:</strong> {sample_meals[i]['Lunch']}</p>
                <p><strong>Dinner:</strong> {sample_meals[i]['Dinner']}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class='nutrition'>
                    <strong>Nutrition Summary:</strong><br>
                    Calories: {nutrition_summary[i]['Calories']} kcal |
                    Protein: {nutrition_summary[i]['Protein']} g |
                    Carbs: {nutrition_summary[i]['Carbs']} g |
                    Fat: {nutrition_summary[i]['Fat']} g
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    elif menu_choice == "Nutrition Summary":
        st.subheader("Nutrition Summary")
        avg_calories = sum(d["Calories"] for d in nutrition_summary) // len(nutrition_summary)
        avg_protein = sum(d["Protein"] for d in nutrition_summary) // len(nutrition_summary)
        avg_carbs = sum(d["Carbs"] for d in nutrition_summary) // len(nutrition_summary)
        avg_fat = sum(d["Fat"] for d in nutrition_summary) // len(nutrition_summary)

        st.markdown(f"""
        **Average Daily Intake:**
        - Calories: {avg_calories} kcal  
        - Protein: {avg_protein} g  
        - Carbs: {avg_carbs} g  
        - Fat: {avg_fat} g  
        """)

    elif menu_choice == "Shopping List":
        st.subheader("Shopping List")
        all_items = set()
        for day_meals in sample_meals:
            for meal_name in day_meals.values():
                all_items.update(ingredients.get(meal_name, []))

        st.markdown("<div class='shopping-list'>", unsafe_allow_html=True)
        for item in sorted(all_items):
            st.markdown(f"- {item}")
        st.markdown("</div>", unsafe_allow_html=True)
