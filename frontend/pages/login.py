import streamlit as st
from utils.api import post

st.title("🔐 Expense Tracker")

tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab1:
    st.subheader("Login")

    login_user = st.text_input("Username", key="login_user")
    login_pass = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        res = post("/login", {
            "username": login_user,
            "password": login_pass
        })

        if res and res.status_code == 200:
            st.session_state["token"] = res.json()["access_token"]
            st.success("Login successful 🎉")
            st.rerun()
        else:
            try:
                st.error(res.json().get("detail"))
            except:
                st.error("Login failed")

# ---------------- REGISTER ----------------
with tab2:
    st.subheader("Register")

    reg_user = st.text_input("Username", key="reg_user")
    reg_pass = st.text_input("Password", type="password", key="reg_pass")
    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register", key="register_btn"):
        if reg_pass != reg_confirm:
            st.error("Passwords do not match")
        else:
            res = post("/register", {
                "username": reg_user,
                "password": reg_pass
            })

            if res and res.status_code in [200, 201]:
                st.success("Account created successfully 🎉")
            else:
                try:
                    st.error(res.json().get("detail"))
                except:
                    st.error("Registration failed")