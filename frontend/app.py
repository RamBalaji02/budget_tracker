import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("💰 Expense Tracker")

menu = st.sidebar.selectbox("Menu", ["Register", "Login", "Add Expense", "History"])

if menu == "Register":

    username = st.text_input("Username")
    password = st.text_input("Password")

    if st.button("Register"):

        res = requests.post(f"{API}/register", json={
            "username": username,
            "password": password
        })

        try:
            st.write(res.json())
        except:
            st.error(res.text)


if menu == "Login":

    username = st.text_input("Username")
    password = st.text_input("Password")

    if st.button("Login"):

        res = requests.post(f"{API}/login", json={
            "username": username,
            "password": password
        })

        try:
            st.write(res.json())
        except:
            st.error(res.text)


if menu == "Add Expense":

    amount = st.number_input("Amount")
    category = st.text_input("Category")
    note = st.text_input("Note")
    date = st.date_input("Date")

    if st.button("Add"):

        res = requests.post(f"{API}/expenses/", json={
            "amount": amount,
            "category": category,
            "note": note,
            "exp_date": str(date)
        })

        try:
            st.write(res.json())
        except:
            st.error(res.text)



if menu == "History":

    res = requests.get(f"{API}/expenses/")

    try:
        st.write(res.json())
    except:
        st.error(res.text)