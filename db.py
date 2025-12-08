import streamlit as st
import psycopg2
import os
def get_connected():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode="require",
        options='-c hostaddr=<IPv4_ADDRESS_OF_DB_HOST>'
    )
