import streamlit as st


def meal_card(day, meal_type, recipe_name, calories, protein, carbs, fats, cost):
    with st.container():
        st.markdown(f"### {day} - {meal_type}")
        st.write(f"**Recipe:** {recipe_name}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{calories} kcal")
        col2.metric("Protein", f"{protein} g")
        col3.metric("Carbs", f"{carbs} g")
        col4.metric("Fats", f"{fats} g")
        st.write(f"**Cost:** ${cost:.2f}")
        st.markdown("---")