import streamlit as st
from utils.api import get
import pandas as pd

st.title("📜 History")

token = st.session_state.get("token")

if not token:
    st.warning("Login required")
    st.stop()

data = get("/expenses/", token).json()

if isinstance(data, list) and len(data) > 0:

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    category = st.text_input("Filter by category")

    if category:
        st.dataframe(df[df["category"] == category])

else:
    st.info("No transactions yet")