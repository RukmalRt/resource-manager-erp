import streamlit as st
import pandas as pd
from db import get_connected

st.title('Stock Manager')

st.subheader('Add / Update Item')

with st.form("materials_form"):
    code = st.text_input('Item Code')
    item = st.text_input('Item Name')
    qty_onhand = st.number_input('Quantity On Hand', min_value=0.0)
    unit_price = st.number_input('Unit Price', min_value=0.0)
    serial = st.text_input('Serial Number', value='')

    add_material = st.form_submit_button('Save Item')

if add_material:
    conn = get_connected()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO materials 
        (item_code, item, quantity_onhand, quantity_delivered, unit_price, serial_num)
        VALUES (%s, %s, %s, 0, %s, %s)
        ON CONFLICT (item_code)
        DO UPDATE SET 
            item = EXCLUDED.item,
            quantity_onhand = EXCLUDED.quantity_onhand,
            unit_price = EXCLUDED.unit_price,
            serial_num = EXCLUDED.serial_num
    """, (code, item, qty_onhand, unit_price, serial))

    conn.commit()
    conn.close()

    st.success("Material saved successfully!")

st.subheader('All Materials in Stock')

conn = get_connected()
df = pd.read_sql("SELECT * FROM materials ORDER BY item_code", conn)
conn.close()

st.dataframe(df)
