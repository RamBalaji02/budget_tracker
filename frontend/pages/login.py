import streamlit as st
from utils.api import post

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    res = post("/login", {
        "username": username,
        "password": password
    })

    data = res.json()

    if "access_token" in data:
        st.session_state["token"] = data["access_token"]
        st.success("Login successful 🎉")
        st.switch_page("pages/dashboard.py")
    else:
        st.error("Invalid login")