import streamlit as st
from utils.api import get, put, delete
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="History", page_icon="📜", layout="wide")
st.title("📜 Transaction History")

token = st.session_state.get("token")
if not token:
    st.warning("Please login first 🔐")
    st.stop()

type_option = st.radio("Select Transaction Type", ["Expenses", "Income"], horizontal=True)

cat_res = get("/categories/", token)
categories = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Salary", "Investment", "Other"]
if cat_res.status_code == 200:
    try:
        categories = [c["name"] for c in cat_res.json()]
    except:
        pass

col1, col2 = st.columns(2)
with col1:
    default_start = datetime.now() - timedelta(days=30)
    default_end = datetime.now()
    date_range = st.date_input("Date Range", [default_start, default_end])
with col2:
    selected_cat = None
    if type_option == "Expenses":
        selected_cat = st.selectbox("Filter by Category", ["All"] + categories)

if type_option == "Expenses":
    res = get("/expenses/", token)
else:
    res = get("/income/", token)

if res.status_code != 200:
    st.error("Failed to fetch transactions: " + res.text)
    st.stop()

data = res.json()

if not isinstance(data, list) or len(data) == 0:
    st.info(f"No {type_option.lower()} transactions found.")
    st.stop()

df = pd.DataFrame(data)

df["date"] = pd.to_datetime(df["date"])

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

if type_option == "Expenses" and selected_cat and selected_cat != "All":
    df = df[df["category"] == selected_cat]

df = df.sort_values(by="date", ascending=False)
df = df.reset_index(drop=True)

if df.empty:
    st.info("No transactions match the selected filters.")
    st.stop()

if type_option == "Expenses":
    column_config = {
        "id": st.column_config.NumberColumn("ID", disabled=True),
        "amount": st.column_config.NumberColumn("Amount ($)", min_value=0.01, required=True),
        "category": st.column_config.SelectboxColumn("Category", options=categories, required=True),
        "note": st.column_config.TextColumn("Note"),
        "date": st.column_config.DateColumn("Date", required=True)
    }
else:
    column_config = {
        "id": st.column_config.NumberColumn("ID", disabled=True),
        "amount": st.column_config.NumberColumn("Amount ($)", min_value=0.01, required=True),
        "source": st.column_config.TextColumn("Source", required=True),
        "date": st.column_config.DateColumn("Date", required=True)
    }

st.subheader("📋 Transactions (Double-click cells to edit, select row and press Delete/Backspace to remove)")

edited_df = st.data_editor(
    df,
    column_config=column_config,
    disabled=["id"],
    num_rows="dynamic",
    key="transaction_editor",
    use_container_width=True
)

if st.button("💾 Save Changes", use_container_width=True):
    changes = st.session_state["transaction_editor"]
    has_success = False
    
    if changes["deleted_rows"]:
        for idx in changes["deleted_rows"]:
            row_id = int(df.loc[idx, "id"])
            if type_option == "Expenses":
                del_res = delete(f"/expenses/{row_id}", token)
            else:
                del_res = delete(f"/income/{row_id}", token)
            if del_res.status_code == 200:
                has_success = True
            else:
                st.error(f"Failed to delete transaction ID {row_id}: {del_res.text}")

    if changes["edited_rows"]:
        for idx, edited_fields in changes["edited_rows"].items():
            idx = int(idx)
            row_id = int(df.loc[idx, "id"])
            
            amount = float(edited_fields.get("amount", df.loc[idx, "amount"]))
            
            raw_date = edited_fields.get("date", df.loc[idx, "date"])
            if hasattr(raw_date, "strftime"):
                date_val = raw_date.strftime("%Y-%m-%d")
            else:
                date_val = str(raw_date)[:10]

            if type_option == "Expenses":
                category_val = edited_fields.get("category", df.loc[idx, "category"])
                note_val = edited_fields.get("note", df.loc[idx, "note"])
                
                up_res = put(f"/expenses/{row_id}", {
                    "amount": amount,
                    "category": category_val,
                    "note": note_val,
                    "exp_date": date_val
                }, token)
            else:
                source_val = edited_fields.get("source", df.loc[idx, "source"])
                up_res = put(f"/income/{row_id}", {
                    "amount": amount,
                    "source": source_val,
                    "date": date_val
                }, token)

            if up_res.status_code == 200:
                has_success = True
            else:
                st.error(f"Failed to update transaction ID {row_id}: {up_res.text}")
                
    if has_success:
        st.success("Transactions updated successfully! 🎉")
        st.rerun()