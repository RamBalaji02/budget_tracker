import streamlit as st
from utils.api import post

st.title("💰 Add Income")

token = st.session_state.get("token")

amount = st.number_input("Amount")
source = st.text_input("Source")
date = st.date_input("Date")

if st.button("Add Income"):

    res = post("/income/", {
        "amount": amount,
        "source": source,
        "inc_date": str(date)
    }, token)

    if res.status_code == 200:
        st.success("Income added")
    else:
        st.error(res.text)