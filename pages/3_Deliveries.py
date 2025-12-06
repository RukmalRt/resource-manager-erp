import streamlit as st
import pandas as pd
from db import get_connected

st.title("Project Resource Planner")

if "delivery_list" not in st.session_state:
    st.session_state.delivery_list = []

st.subheader('Delivery Header')

project_number = st.number_input('Project Number', min_value=1)
delivery_date = st.date_input('Delivery Date')

st.subheader('Add Materials to Deliver')

item_code = st.text_input('Item Code')
qty = st.number_input('Quantity', min_value=1.0)

add_button = st.button('Add Item')

if add_button:
    conn = get_connected()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT item, quantity_onhand 
        FROM materials 
        WHERE item_code = %s
    """, (item_code,))

    row = cursor.fetchone()

    if row:
        item_name, available_qty = row

        if qty > available_qty:
            st.error(f"❌ Not enough stock. Available: {available_qty}")
        else:
            st.session_state.delivery_list.append({
                "item_code": item_code,
                "item_name": item_name,
                "quantity": qty
            })
            st.success("✅ Item added!")
    else:
        st.error('❌ Invalid item code.')

    conn.close()

if st.session_state.delivery_list:
    st.subheader('Delivery Items')
    st.dataframe(pd.DataFrame(st.session_state.delivery_list))

if st.button('Submit Delivery'):
    if not st.session_state.delivery_list:
        st.warning("⚠ No items in delivery list.")
    else:
        conn = get_connected()
        cursor = conn.cursor()

        for d in st.session_state.delivery_list:
            # Insert delivery record
            cursor.execute("""
                INSERT INTO project_materials 
                (project_number, item_code, item, quantity, delivery_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (project_number, d["item_code"], d["item_name"], d["quantity"], delivery_date))

            # Update stock
            cursor.execute("""
                UPDATE materials
                SET quantity_onhand = quantity_onhand - %s,
                    quantity_delivered = quantity_delivered + %s
                WHERE item_code = %s
            """, (d["quantity"], d["quantity"], d["item_code"]))

        conn.commit()
        conn.close()

        st.session_state.delivery_list = []
        st.success("✅ Delivery submitted successfully!")
