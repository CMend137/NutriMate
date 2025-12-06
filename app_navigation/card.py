import streamlit as st


def meal_card(day, meal_type, recipe_name, calories, protein, carbs, fats, cost):
    with st.container():
        st.markdown(
            f"""
            <div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px;">
                <h4 style="margin:0; color:#463e7a;">{meal_type}</h4>
                <p style="font-size: 18px; font-weight: bold; margin: 5px 0;">{recipe_name}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Kcal", f"{calories}")
        col2.metric("Prot", f"{protein}g")
        col3.metric("Carb", f"{carbs}g")
        col4.metric("Fat", f"{fats}g")
        col5.metric("Cost", f"${cost:.2f}")

