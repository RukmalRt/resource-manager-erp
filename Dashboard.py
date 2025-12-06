import streamlit as st
import pandas as pd
from db import get_connected

st.set_page_config(page_title='Resource Manager', layout='wide')

st.title('Resource Manager Dashboard')
st.markdown("### Select a module to continue")

# ------------------ LOAD KPI DATA ------------------ #
conn = get_connected()

total_projects = pd.read_sql("SELECT COUNT(*) FROM projects", conn).iloc[0, 0]
total_materials = pd.read_sql("SELECT COUNT(*) FROM materials", conn).iloc[0, 0]
total_stock = pd.read_sql("SELECT COALESCE(SUM(quantity_onhand),0) FROM materials", conn).iloc[0, 0]
total_delivered = pd.read_sql("SELECT COALESCE(SUM(quantity),0) FROM project_materials", conn).iloc[0, 0]

today_deliveries = pd.read_sql("""
    SELECT p.project_name, pm.item, pm.quantity
    FROM project_materials pm
    JOIN projects p ON pm.project_number = p.project_number
    WHERE pm.delivery_date = CURRENT_DATE
    ORDER BY p.project_name
""", conn)

low_stock = pd.read_sql("""
    SELECT item_code, item, quantity_onhand
    FROM materials
    WHERE quantity_onhand < 10
    ORDER BY quantity_onhand
""", conn)

conn.close()

# ------------------ KPI CARDS ------------------ #
col1, col2, col3, col4 = st.columns(4)

col1.metric("📁 Total Projects", total_projects)
col2.metric("📦 Material Types", total_materials)
col3.metric("📊 Stock On Hand", total_stock)
col4.metric("🚚 Total Delivered", total_delivered)

st.divider()

# ------------------ TODAY'S DELIVERIES ------------------ #
st.subheader("📆 Today's Deliveries")

if today_deliveries.empty:
    st.info("No deliveries today.")
else:
    st.dataframe(today_deliveries, use_container_width=True)

# ------------------ LOW STOCK ALERT ------------------ #
st.subheader("⚠️ Low Stock Alerts")

if low_stock.empty:
    st.success("All stock levels are healthy ✅")
else:
    st.error("Low stock detected!")
    st.dataframe(low_stock, use_container_width=True)

st.divider()

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

with col1:
    if st.button("Projects", use_container_width=True):
        st.switch_page("pages/1_Projects.py")

with col2:
    if st.button("Materials", use_container_width=True):
        st.switch_page("pages/2_Materials.py")

with col3:
    if st.button("Deliveries", use_container_width=True):
        st.switch_page("pages/3_Deliveries.py")

with col4:
    if st.button("Delivery Notes (PDF)", use_container_width=True):
        st.switch_page("pages/5_Delivery_Note.py")

with col5:
    if st.button("Delivery History", use_container_width=True):
        st.switch_page("pages/4_Delivery_History.py")

st.divider()

st.info("Use this dashboard to manage projects, stock, deliveries, and generate professional delivery notes.")