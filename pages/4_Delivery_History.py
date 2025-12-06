import streamlit as st
from db import get_connected
import pandas as pd

st.title("Delivery History by Project")

conn = get_connected()

projects_df = pd.read_sql(
    "SELECT project_number, project_name FROM projects ORDER BY project_number",
    conn
)

project_map = dict(zip(projects_df['project_name'], projects_df["project_number"]))

selected_project = st.selectbox("Select Project", list(project_map.keys()))

project_number = project_map[selected_project]

start_date = st.date_input("From Date")
end_date = st.date_input("To Date")

if st.button("Load Delivery History"):
    query = """
    SELECT
        pm.project_number,
        p.project_code,
        pm.item_code,
        pm.item,
        pm.quantity,
        pm.delivery_date
    FROM project_materials pm
    JOIN projects p ON pm.project_number = p.project_number
    WHERE pm.project_number = %s
    AND pm.delivery_date BETWEEN %s AND %s
    ORDER BY pm.delivery_date"""

    df = pd.read_sql(query, conn, params=(project_number, start_date, end_date))

    if df.empty:
        st.warning("No deliveries found for this period")
    else:
        st.subheader("Delivery History")
        st.dataframe(df)

        total = df["quantity"].sum()
        st.success(f"Total Quantity Delivered: {total}Total Quantity Delivered: {total}")

conn.close()

