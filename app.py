import streamlit as st
from app_pages import user_input, meal_plan

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "user_input"

# -----------------------
# Navigation
if st.session_state.current_page == "user_input":
    user_input.show()
elif st.session_state.current_page == "meal_plan":
    meal_plan.show()
