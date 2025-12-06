import streamlit as st
import pandas as pd
from db import get_connected
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.title("Delivery Note Generator")

conn = get_connected()

projects_df = pd.read_sql(
"SELECT project_number, project_name FROM projects ORDER BY project_number",
    conn
)

project_map = dict(zip(projects_df["project_name"], projects_df["project_number"]))
selected_project = st.selectbox("Select Project", list(project_map.keys()))
project_number = project_map[selected_project]

delivery_date = st.date_input("Select Delivery Date")

if st.button("Generate Delivery Note"):
    query = """
        SELECT 
            p.project_name, 
            pm.item_code, 
            pm.item, 
            pm.quantity, 
            pm.delivery_date
        FROM project_materials pm
        JOIN projects p ON pm.project_number = p.project_number
        WHERE pm.project_number = %s
        AND pm.delivery_date = %s
    """

    df = pd.read_sql(query, conn, params=(project_number, delivery_date))

    if df.empty:
        st.warning("No deliveries found for this date")

    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_path = tmp.name

        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"<b>Delivery Note</b>", styles["Title"]))
        elements.append(Paragraph(f"Project: {df.iloc[0]['project_name']}", styles["Normal"]))
        elements.append(Paragraph(f"Date: {delivery_date}", styles["Normal"]))
        elements.append(Paragraph(" ", styles["Normal"]))

        table_data = [["Item Code", "Item", "Quantity"]]

        for _, row in df.iterrows():
            table_data.append([
                row["item_code"],
                row["item"],
                str(row["quantity"])
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))

        elements.append(table)

        pdf = SimpleDocTemplate(pdf_path, pagesize=A4)
        pdf.build(elements)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇ Download Delivery Note (PDF)",
                data = f,
                file_name=f"Delivery_Note_Project_{project_number}_{delivery_date}.pdf",
                mime="application/pdf"
            )

conn.close()
