import streamlit as st
from db import get_connected

st.title("Supabase DB Test")

try:
    conn = get_connected()
    st.success("✅ Supabase connected successfully!")
    conn.close()
except Exception as e:
    st.error(e)