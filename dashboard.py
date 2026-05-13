
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Emanuel Sankofa Dashboard", layout="wide")
st.title("📚 Emanuel Sankofa")
st.caption("William Emanuel Boatwright — Literary Assistant Dashboard")

# Check for data files
csv_path = "submissions_practice.csv"
if not os.path.exists(csv_path):
    csv_path = "sample.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.dataframe(df, use_container_width=True)

    st.subheader("🔔 Follow-up Alerts")
    today = datetime.now().date()
    for _, row in df.iterrows():
        fd = row.get("Follow-Up Date")
        if pd.notna(fd) and fd:
            try:
                fd_date = datetime.strptime(fd, "%Y-%m-%d").date()
                days = (fd_date - today).days
                if days < 0:
                    st.error(f"🔴 {row['Title']} – OVERDUE (was {fd})")
                elif days == 0:
                    st.warning(f"🟠 {row['Title']} – DUE TODAY")
                elif days <= 7:
                    st.warning(f"🟡 {row['Title']} – due in {days} days")
                else:
                    st.info(f"✅ {row['Title']} – on track, due {fd}")
            except:
                pass
else:
    st.warning("No data file found. Please upload submissions_practice.csv or sample.csv")

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
