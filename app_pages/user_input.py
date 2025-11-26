import streamlit as st
from assets import colors
from backend import meal_planner

def calculate_calories(weight, height, age, gender, activity, goal):
    # BMR Calculation
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # Activity Multiplier
    multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    tdee = bmr * multipliers.get(activity, 1.2)

    # Goal Adjustment
    if goal == "Weight Loss":
        return int(tdee - 500)
    elif goal == "Weight Gain":
        return int(tdee + 500)
    else:
        return int(tdee)

def show():
    st.set_page_config(page_title="NutriMate", page_icon="assets/logo.png")

    # Custom CSS
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
            height: 50px;
            width: 200px;
            font-size: 24px;
            border-radius: 10px;
            transition: all 0.3s ease-in-out;
            margin-left: 0;
        }}
        
        .stButton>button:hover {{
            background-color: {colors.DARK_PURPLE};
            color: white;
            transform: scale(1.05);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar
    st.sidebar.image("assets/logo.png", width=200)
    st.sidebar.title("Menu")
    menu_choice = st.sidebar.radio(
        "Navigate",
        ["How It Works", "About Us", "Contact Us"]
    )

    if menu_choice == "How It Works":
        st.sidebar.markdown("""
        1.  **Profile Customization:** Establish your dietary and fitness parameters, including **activity level, calorie targets, and budget.**
        2.  **AI-Driven Optimization:** Our specialized **AI agents** process your profile against a verified recipe database to determine the optimal weekly meal schedule and calculate required nutritional values.
        3.  **Comprehensive Reporting:** Instantly visualize your complete **7-day meal plan**, detailed nutritional totals (Protein, Carbs, Fat, Calories), and the final **total cost** breakdown.
        """)
    elif menu_choice == "About Us":
        st.sidebar.markdown("""
        ### **Our Platform**
        
        **NutriMate** is a cutting-edge, **AI-driven optimization platform** designed to resolve nutritional planning complexities. We leverage proprietary algorithms and large language models to generate **personalized, cost-optimized,** weekly meal plans, driving efficiency and budget compliance for every user.
        """)
    elif menu_choice == "Contact Us":
        st.sidebar.markdown("""
        Email: support@nutrimate.com  
        Phone: +1 305 123 4567  
        Website: www.nutrimate.com
        """)

    # -----------------------
    st.subheader("Tell Us About Yourself")

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", key="first_name")
        age = st.number_input("Age", min_value=1, max_value=120, key="age")
        weight_val = st.number_input("Weight", min_value=1.0, key="weight")
        height_val = st.number_input("Height", min_value=1.0, key="height")
        
        
    with col2:
        last_name = st.text_input("Last Name", key="last_name")
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
        w_unit = st.selectbox("Weight Unit", ["kg", "lbs"], key="weight_unit")
        h_unit = st.selectbox("Height Unit", ["cm", "inch"], key="height_unit")

    st.subheader("Preferences")
    activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"], key="activity")
    goal = st.selectbox("Dietary Goal", ["Weight Loss", "Weight Gain", "Maintenance"], key="goal")
    
    # Budget Input
    weekly_budget = st.number_input("Weekly Budget ($)", min_value=70.0, step=5.0, key="budget")
    
    restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Lactose-Free"], key="restrictions")

    # Submit Logic
    if st.button("Generate Plan"):
        # Convert units to Metric
        weight_kg = weight_val * 0.453592 if w_unit == "lbs" else weight_val
        height_cm = height_val * 2.54 if h_unit == "inch" else height_val

        # Calculate Calories
        daily_cals = calculate_calories(weight_kg, height_cm, age, gender, activity, goal)

        # Create Profile Dict
        user_profile = {
            "name": first_name,
            "goal": goal,
            "activity_level": activity,
            "daily_calories": daily_cals,
            "weekly_budget": weekly_budget,
            "restrictions": restrictions
        }
        st.session_state.user_profile = user_profile

        # CALL BACKEND
        with st.spinner("AI Agents are crafting your menu..."):
            try:
                plan = meal_planner.build_weekly_plan(weekly_budget)
                st.session_state.generated_plan = plan
                st.session_state.current_page = "meal_plan"
                st.rerun()
            except Exception as e:
                st.error(f"Error generating plan: {e}")
