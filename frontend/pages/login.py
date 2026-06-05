import streamlit as st
from utils.api import post

st.title("🔐 Expense Tracker")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        res = post("/login", {"username": user, "password": pwd})

        if res and res.status_code == 200:
            st.session_state["token"] = res.json()["access_token"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Login failed")

with tab2:
    user = st.text_input("Username", key="r1")
    pwd = st.text_input("Password", type="password", key="r2")

    if st.button("Register"):
        res = post("/register", {"username": user, "password": pwd})

        if res and res.status_code == 200:
            st.success("Registered successfully")
        else:
            st.error("Registration failed")