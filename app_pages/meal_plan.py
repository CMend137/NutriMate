import streamlit as st
from assets import colors
from app_navigation import card, summary
from backend import llm_recommender
from backend.meal_planner import generate_shopping_list

def show():
    st.set_page_config(page_title="NutriMate - Meal Plan", page_icon="assets/logo.png")

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {colors.LIME_GREEN} 0%, {colors.GREEN} 100%);
            color: {colors.BLACK};
        }}

        .stButton>button {{
            background-color: {colors.DARK_PURPLE}; 
            color: white !important; 
            height: 45px;
            width: 200px;
            font-size: 20px;
            border-radius: 10px;
            transition: all 0.3s ease-in-out;
            margin-top: 10px;
        }}

        .stButton>button:hover {{
            background-color: {colors.BACKGROUND}; 
            color: black !important; 
            transform: scale(1.05);
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

        [data-testid="stTextarea"] {{
            background-color: {colors.DARK_PURPLE}; 
            border-radius: 10px;
            padding: 10px;
            border: 1px solid {colors.DARK_PURPLE}; 
        }}
    
        [data-testid="stTabs"] button {{
            color: black;
        }}
        
        </style>
        """,
        unsafe_allow_html=True
    )

    # Retrieve data
    plan_data = st.session_state.get("generated_plan")
    user_profile = st.session_state.get("user_profile")

    if not plan_data:
        st.warning("No plan generated yet. Please go back.")
        if st.button("Go Back"):
            st.session_state.current_page = "user_input"
            st.rerun()
        return

    full_plan = plan_data["weekly_plan"] # List of days

    # --- Sidebar ---
    st.sidebar.image("assets/logo.png", width=200)
    st.sidebar.title(f"Hi {user_profile.get('name', 'There')}!")

    # Sidebar LLM Chat
    st.sidebar.subheader("Ask NutriMate AI")
    user_q = st.sidebar.text_input("Questions about your plan?")
    if st.sidebar.button("Ask"):
        if user_q:
            with st.spinner("Thinking..."):
                # Convert list format to dict for LLM compatibility
                plan_dict_for_llm = {d['day']: d for d in full_plan}
                answer = llm_recommender.answer_user_question(plan_dict_for_llm, user_q, user_profile)
                st.sidebar.markdown(answer)
                
    # --- Main Content ---
    st.title("Your Personalized Meal Plan")

    tab1, tab2, tab3 = st.tabs(["Weekly Menu", "AI Insights", "Shopping List"])
    with tab1:
        # Totals for the summary box
        total_cals = sum(d['daily_calories'] for d in full_plan)
        total_prot = sum(d['Breakfast']['data']['protein'] + d['Lunch']['data']['protein'] + d['Dinner']['data']['protein'] for d in full_plan)
        total_carbs = sum(d['Breakfast']['data']['carbs'] + d['Lunch']['data']['carbs'] + d['Dinner']['data']['carbs'] for d in full_plan)
        total_fat = sum(d['Breakfast']['data']['fat'] + d['Lunch']['data']['fat'] + d['Dinner']['data']['fat'] for d in full_plan)
        
        summary.summary_box(
            int(total_cals), 
            int(total_prot), 
            int(total_carbs), 
            int(total_fat), 
            plan_data["total_weekly_cost"]
        )
        
        st.markdown("---")

        for day_data in full_plan:
            st.header(day_data['day'])
            
            def render_meal(meal_type_key):
                meal = day_data[meal_type_key]
                data = meal['data']
                card.meal_card(
                    day=day_data['day'],
                    meal_type=meal_type_key,
                    recipe_name=meal['name'],
                    calories=data['calories'],
                    protein=data['protein'],
                    carbs=data['carbs'],
                    fats=data['fat'],
                    cost=data['cost']
                )
            
            render_meal("Breakfast")
            render_meal("Lunch")
            render_meal("Dinner")

    with tab2:
        st.subheader("AI-Powered Analysis")
        
        plan_dict_for_llm = {d['day']: d for d in full_plan}

        if st.button("Generate Executive Summary"):
            with st.spinner("Analyzing nutrients..."):
                text = llm_recommender.summarize_weekly_plan(plan_dict_for_llm, user_profile)
                st.markdown(text)
        
        if st.button("Analyze Budget & Calories"):
            with st.spinner("Checking budget..."):
                text = llm_recommender.analyze_budget_and_calories(plan_dict_for_llm, user_profile)
                st.markdown(text)

        if st.button("Suggest Alternatives"):
            with st.spinner("Finding swaps..."):
                text = llm_recommender.suggest_alternatives(plan_dict_for_llm, user_profile)
                st.markdown(text)

    with tab3:        
        shopping_list_md = generate_shopping_list(plan_data)
        st.markdown(shopping_list_md)
