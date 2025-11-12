import streamlit as st
from assets import colors

def show():
    st.set_page_config(
        page_title="NutriMate",
        page_icon="assets/logo.png",
    )

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

        [data-testid="stSidebar"] > div:first-child {{
            background-color: {colors.BACKGROUND};
        }}

        [data-testid="stSidebar"] * {{
            color: black;
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
        ["How it Works", "About Us", "Contact Us"]
    )

    if menu_choice == "How it Works":
        st.sidebar.markdown("""
        1. Enter your profile information and preferences.
        2. AI agents calculate weekly calorie needs and filter recipes.
        3. View your weekly meal plan with nutritional breakdowns and total cost.
        """)
    elif menu_choice == "About Us":
        st.sidebar.markdown("""
        **NutriMate** is a lightweight AI-driven app that generates personalized, budget-friendly weekly meal plans.

        Our mission is to make healthy eating accessible to everyone!
        """)
    elif menu_choice == "Contact Us":
        st.sidebar.markdown("""
        Email: support@nutrimate.com  
        Phone: +1 305 123 4567  
        Website: www.nutrimate.com
        """)

    # -----------------------
    st.subheader("Tell Us About Yourself")

    st.text_input("First Name", key="first_name")
    st.text_input("Last Name", key="last_name")
    st.number_input("Age", min_value=1, max_value=120, key="age")
    st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")

    # Weight + units
    st.selectbox("Weight Unit", ["kg", "lbs"], key="weight_unit")
    st.number_input("Weight", min_value=1.0, key="weight")

    # Height + units
    st.selectbox("Height Unit", ["cm", "inch"], key="height_unit")
    st.number_input("Height", min_value=1.0, key="height")

    st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"], key="activity")
    st.selectbox("Dietary Goal", ["Weight Loss", "Weight Gain", "Maintenance"], key="goal")
    st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Lactose Intolerant"], key="restrictions")

    # Submit button
    if st.button("Submit"):
        st.session_state.current_page = "meal_plan"
