import streamlit as st
from utils.api import post

st.title("🔐 Expense Tracker Access")

tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab1:
    st.subheader("Login to your account")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", use_container_width=True):

        if not username or not password:
            st.error("Please fill all fields")
        else:
            res = post("/login", {
                "username": username,
                "password": password
            })

            if res.status_code == 200:
                data = res.json()
                st.session_state["token"] = data["access_token"]
                st.success("Login successful 🎉")
                st.rerun()
            else:
                st.error(res.json().get("detail", "Login failed"))


# ---------------- REGISTER ----------------
with tab2:
    st.subheader("Create account")

    reg_user = st.text_input("Username", key="reg_user")
    reg_pass = st.text_input("Password", type="password", key="reg_pass")
    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register", use_container_width=True):

        if not reg_user or not reg_pass:
            st.error("Please fill all fields")

        elif reg_pass != reg_confirm:
            st.error("Passwords do not match")

        else:
            res = post("/register", {
                "username": reg_user,
                "password": reg_pass
            })

            if res.status_code in [200, 201]:
                st.success("Registration successful 🎉 You can login now")
            else:
                st.error(res.json().get("detail", "Registration failed"))