import streamlit as st

st.title("Expense Tracker")

page = st.sidebar.selectbox("Menu", ["Dashboard", "Add Expense", "History"])

if page == "Dashboard":
    st.write("Dashboard Page")

elif page == "Add Expense":
    st.write("Add Expense Page")

elif page == "History":
    st.write("History Page")