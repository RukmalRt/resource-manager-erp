import streamlit as st
import psycopg2
import os
def get_connected():
    return psycopg2.connect(
        dbname=st.secrets["postgres"]["db_name"],
        user=st.secrets["postgres"]["db_user"],
        password=st.secrets["postgres"]["db_password"],
        host=st.secrets["postgres"]["db_host"],
        port=st.secrets["postgres"]["db_port"]
         sslmode="require"
    )
