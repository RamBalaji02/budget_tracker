import streamlit as st
from utils.api import post, get

st.title("➕ Add Expense")

token = st.session_state.get("token")
if not token:
    st.warning("Please login first 🔐")
    st.stop()

cat_res = get("/categories/", token)
categories = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Salary", "Investment", "Other"]
if cat_res.status_code == 200:
    try:
        categories = [c["name"] for c in cat_res.json()]
    except:
        pass

with st.sidebar:
    st.subheader("Manage Categories")
    new_cat = st.text_input("Add Custom Category", placeholder="e.g. Subscriptions")
    if st.button("Create Category", use_container_width=True):
        if new_cat.strip():
            res = post("/categories/", {"name": new_cat.strip()}, token)
            if res.status_code in [200, 201]:
                st.success(f"Category '{new_cat}' created!")
                st.rerun()
            else:
                st.error("Failed to create category")
        else:
            st.warning("Category name cannot be empty")

amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
category = st.selectbox("Category", categories)
note = st.text_input("Note (Optional)", placeholder="e.g. Weekly grocery")
date = st.date_input("Date")

if st.button("Add Expense", use_container_width=True):
    if amount <= 0:
        st.error("Amount must be greater than zero")
    else:
        res = post("/expenses/", {
            "amount": amount,
            "category": category,
            "note": note,
            "exp_date": str(date)
        }, token)

        if res.status_code in [200, 201]:
            st.success("Expense added 🎉")
        else:
            st.error("Failed to add expense: " + res.text)