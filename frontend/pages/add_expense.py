import streamlit as st
from utils.api import post

st.title("➕ Add Expense")

token = st.session_state.get("token")

amount = st.number_input("Amount")
category = st.text_input("Category")
note = st.text_input("Note")
date = st.date_input("Date")

if st.button("Add Expense"):

    res = post("/expenses/", {
        "amount": amount,
        "category": category,
        "note": note,
        "exp_date": str(date)
    }, token)

    if res.status_code == 200:
        st.success("Expense added")
    else:
        st.error(res.text)