import streamlit as st
from utils.api import post

st.title("🔐 Expense Tracker Access")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("Login to your account")
    login_user = st.text_input("Username", key="login_user")
    login_pass = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Log In", use_container_width=True):
        if not login_user or not login_pass:
            st.error("Please fill in all fields")
        else:
            res = post("/auth/login", {
                "username": login_user,
                "password": login_pass
            })
            if res.status_code == 200:
                data = res.json()
                st.session_state["token"] = data["access_token"]
                st.success("Login successful 🎉")
                st.rerun()
            else:
                try:
                    err_msg = res.json().get("detail", "Invalid login credentials")
                except:
                    err_msg = "Invalid login credentials"
                st.error(err_msg)

with tab2:
    st.subheader("Create a new account")
    reg_user = st.text_input("Username", key="reg_user")
    reg_pass = st.text_input("Password", type="password", key="reg_pass")
    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
    
    if st.button("Register", use_container_width=True):
        if not reg_user or not reg_pass or not reg_confirm:
            st.error("Please fill in all fields")
        elif reg_pass != reg_confirm:
            st.error("Passwords do not match")
        else:
            res = post("/auth/register", {
                "username": reg_user,
                "password": reg_pass
            })
            if res.status_code in [200, 201]:
                st.success("Registration successful! You can now log in.")
            else:
                try:
                    err_msg = res.json().get("detail", "Registration failed")
                except:
                    err_msg = "Registration failed"
                st.error(err_msg)