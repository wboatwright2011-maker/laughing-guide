import streamlit as st
import pandas as pd
from datetime import datetime
import os
import traceback

st.set_page_config(page_title="Emanuel Sankofa Dashboard", layout="wide")
st.title("📚 Emanuel Sankofa")
st.caption("William Emanuel Boatwright — Literary Assistant Dashboard")

st.subheader("🔍 Debug Information")

# Check if secrets are available
try:
    # Try to access the secret
    raw_data = st.secrets.get("real_data")
    
    if raw_data is None:
        st.error("❌ Secret 'real_data' not found. Please add it in Settings → Secrets.")
        st.stop()
    
    st.success(f"✅ Secret 'real_data' found. Length: {len(raw_data)} characters.")
    
    # Show first 200 characters of the secret for debugging (safe)
    st.text(f"Preview: {raw_data[:200]}...")
    
    # Try to parse as CSV
    from io import StringIO
    df = pd.read_csv(StringIO(raw_data))
    
    st.success(f"✅ Successfully parsed CSV. Found {len(df)} rows and {len(df.columns)} columns.")
    
    # Display the dataframe
    st.subheader("📋 Your Submissions")
    st.dataframe(df, use_container_width=True)
    
    # Show follow-up alerts
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
            except Exception as e:
                st.warning(f"Could not parse date {fd} for {row['Title']}: {e}")
    
except Exception as e:
    st.error(f"❌ An error occurred: {type(e).__name__}: {e}")
    st.code(traceback.format_exc())

st.markdown("---")
st.caption(f"Debug version last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
