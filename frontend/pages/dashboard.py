import streamlit as st
from utils.api import get
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Expense Tracker Dashboard")

token = st.session_state.get("token")

if not token:
    st.warning("Please login first 🔐")
    st.stop()

res = get("/summary", token=token)

if res.status_code != 200:
    st.error("Backend error: " + res.text)
    st.stop()

try:
    summary = res.json()
except:
    st.error("Invalid JSON from backend")
    st.stop()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Income", summary.get("total_income", 0))
col2.metric("💸 Expense", summary.get("total_expense", 0))
col3.metric("📈 Balance", summary.get("balance", 0))

st.divider()

exp_res = get("/expenses/", token=token)

try:
    expenses = exp_res.json()
except:
    st.error("Expense API error")
    st.stop()

if not isinstance(expenses, list) or len(expenses) == 0:
    st.info("No expenses yet")
    st.stop()

df = pd.DataFrame(expenses)

st.subheader("📌 Expense Breakdown (Category Wise)")

pie_fig = px.pie(
    df,
    names="category",
    values="amount",
    title="Expense Distribution"
)

st.plotly_chart(pie_fig, use_container_width=True)

st.subheader("📊 Income vs Expense Overview")

bar_df = pd.DataFrame({
    "Type": ["Income", "Expense"],
    "Amount": [
        summary.get("total_income", 0),
        summary.get("total_expense", 0)
    ]
})

bar_fig = px.bar(
    bar_df,
    x="Type",
    y="Amount",
    color="Type",
    text="Amount",
    title="Income vs Expense"
)

st.plotly_chart(bar_fig, use_container_width=True)

st.subheader("📋 Recent Transactions")
st.dataframe(df, use_container_width=True)