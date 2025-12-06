import streamlit as st
import pandas as pd
from db import get_connected

st.title('Projects Manager')

st.subheader('Add New Project')

with st.form('project_form'):
    name = st.text_input('Project Name')
    address = st.text_input('Project Address')
    quotation = st.text_input('Quotation Number')
    customer = st.text_input('Customer Name')
    customer_address = st.text_input('Customer Address')
    phone = st.text_input('Customer Phone Number')

    submitted = st.form_submit_button('Add Project')

if submitted:
    conn = get_connected()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projects 
        (project_name, project_address, quotation_number, customer_name, customer_address, customer_phone_number)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, address, quotation, customer, customer_address, phone))

    conn.commit()
    conn.close()

    st.success('✅ Project added successfully!')

st.subheader('Existing Projects')

conn = get_connected()
df = pd.read_sql("SELECT * FROM projects ORDER BY project_number", conn)
conn.close()

st.dataframe(df)
