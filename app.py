import streamlit as st
import psycopg2
import pandas as pd

# No Streamlit.io, você configurará estas chaves em "Secrets"
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        sslmode="require"
    )

st.title("🚀 CRUD SkyData - Aiven PostgreSQL")

# Exemplo de Read (Leitura)
try:
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM contatos", conn)
    st.write("### Lista de Contatos")
    st.dataframe(df)
    conn.close()
except Exception as e:
    st.error(f"Erro de conexão: {e}")
