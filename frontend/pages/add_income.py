import streamlit as st
from utils.api import post

st.title("💰 Add Income")

token = st.session_state.get("token")
if not token:
    st.warning("Please login first 🔐")
    st.stop()

amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
source = st.text_input("Source", placeholder="e.g. Salary, Freelance")
date = st.date_input("Date")

if st.button("Add Income", use_container_width=True):
    if amount <= 0:
        st.error("Amount must be greater than zero")
    else:
        res = post("/income/", {
            "amount": amount,
            "source": source,
            "date": str(date)
        }, token)

        if res.status_code in [200, 201]:
            st.success("Income added 🎉")
        else:
            st.error("Failed to add income: " + res.text)