import streamlit as st


def summary_box(total_calories, total_protein, total_carbs, total_fats, total_cost):
    with st.container():
        st.subheader("Weekly Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Calories", f"{total_calories} kcal")
        col2.metric("Protein", f"{total_protein} g")
        col3.metric("Carbs", f"{total_carbs} g")
        col4.metric("Fats", f"{total_fats} g")
        col5.metric("Total Cost", f"${total_cost:.2f}")
