import streamlit as st
from utils.api import get
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.express as px
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Expense Tracker Dashboard")

token = st.session_state.get("token")

if not token:
    st.warning("Please login first 🔐")
    st.stop()

current_date = datetime.now()
month_options = []
for i in range(12):
    m = (current_date.month - i - 1) % 12 + 1
    y = current_date.year + (current_date.month - i - 1) // 12
    month_options.append(f"{y}-{m:02d}")

selected_month = st.selectbox("📅 Select Month", month_options, index=0)

res = get(f"/summary?month={selected_month}", token=token)

if res.status_code != 200:
    st.error("Backend error: " + res.text)
    st.stop()

try:
    summary = res.json()
except:
    st.error("Invalid JSON from backend")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Income", f"${summary.get('total_income', 0):,.2f}")
col2.metric("💸 Expense", f"${summary.get('total_expense', 0):,.2f}")

balance = summary.get("balance", 0)
col3.metric("📈 Balance", f"${balance:,.2f}", delta=f"${balance:,.2f}" if balance >= 0 else f"-${abs(balance):,.2f}")

st.divider()

exp_res = get("/expenses/", token=token)

try:
    expenses = exp_res.json()
except:
    st.error("Expense API error")
    st.stop()

# Check if we have transactions at all
if not isinstance(expenses, list):
    st.info("Failed to load expenses")
    st.stop()

df = pd.DataFrame(expenses)

if not df.empty:
    df["month"] = df["date"].apply(lambda x: x[:7] if isinstance(x, str) else "")
    filtered_df = df[df["month"] == selected_month]
else:
    filtered_df = pd.DataFrame(columns=["id", "amount", "category", "note", "date"])

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📌 Expense Breakdown (Category Wise)")
    if not filtered_df.empty:
        pie_fig = px.pie(
            filtered_df,
            names="category",
            values="amount",
            hole=0.4,
            title=f"Expense Distribution for {selected_month}",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        pie_fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(pie_fig, use_container_width=True)
    else:
        st.info("No expenses recorded for this month.")

with chart_col2:
    st.subheader("📊 Income vs Expense Overview")
    bar_df = pd.DataFrame({
        "Type": ["Income", "Expense"],
        "Amount": [
            float(summary.get("total_income", 0)),
            float(summary.get("total_expense", 0))
        ]
    })
    bar_fig = px.bar(
        bar_df,
        x="Type",
        y="Amount",
        color="Type",
        text="Amount",
        title=f"Income vs Expense for {selected_month}",
        color_discrete_map={"Income": "#2ecc71", "Expense": "#e74c3c"}
    )
    bar_fig.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
    st.plotly_chart(bar_fig, use_container_width=True)

st.subheader("📋 Recent Transactions (Selected Month)")
if not filtered_df.empty:
    presentation_df = filtered_df[["date", "category", "amount", "note"]].rename(
        columns={"date": "Date", "category": "Category", "amount": "Amount ($)", "note": "Note"}
    )
    st.dataframe(presentation_df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)
else:
    st.info("No transactions found for this month.")