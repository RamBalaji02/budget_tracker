import streamlit as st

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

token = st.session_state.get("token")

login_page = st.Page("pages/login.py", title="Login / Register", icon="🔐", default=True)

if not token:
    pg = st.navigation([login_page])
else:
    dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True)
    add_expense_page = st.Page("pages/add_expense.py", title="Add Expense", icon="➕")
    add_income_page = st.Page("pages/add_income.py", title="Add Income", icon="💵")
    history_page = st.Page("pages/history.py", title="History", icon="📜")
    
    with st.sidebar:
        st.write("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.success("Logged out successfully!")
            st.rerun()
            
    pg = st.navigation([dashboard_page, add_expense_page, add_income_page, history_page])

pg.run()