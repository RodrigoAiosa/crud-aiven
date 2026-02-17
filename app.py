import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="SkyData CRUD", page_icon="📊", layout="wide")

# Função de Conexão usando st.secrets (Segurança para o GitHub)
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        sslmode="require"
    )

st.title("🚀 Sistema de Cadastro SkyData")

# Criando as Abas para o CRUD
tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Adicionar", "📝 Editar", "🗑️ Excluir"])

# --- 1. READ (LISTAR) ---
with tab1:
    st.subheader("Contatos Cadastrados")
    try:
        conn = get_connection()
        query = "SELECT id_contato as ID, nome as Nome, data_nascimento as Nascimento FROM contatos ORDER BY id_contato ASC"
        df = pd.read_sql(query, conn)
        st.dataframe(df, use_container_width=True, hide_index=True)
        conn.close()
    except Exception as e:
        st.error(f"Erro ao listar: {e}")

# --- 2. CREATE (ADICIONAR) ---
with tab2:
    st.subheader("Novo Cadastro")
    with st.form("form_adicionar", clear_on_submit=True):
        novo_nome = st.text_input("Nome Completo")
        nova_data = st.date_input("Data de Nascimento", min_value=datetime(1930, 1, 1))
        btn_add = st.form_submit_button("Salvar no Banco")

        if btn_add:
            if novo_nome:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO contatos (nome, data_nascimento) VALUES (%s, %s)", (novo_nome, nova_data))
                    conn.commit()
                    st.success(f"✅ {novo_nome} cadastrado com sucesso!")
                    cur.close()
                    conn.close()
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            else:
                st.warning("Por favor, preencha o nome.")

# --- 3. UPDATE (EDITAR) ---
with tab3:
    st.subheader("Editar Registro Existente")
    id_editar = st.number_input("Informe o ID que deseja editar", step=1, min_value=1)
    
    with st.form("form_editar"):
        edit_nome = st.text_input("Novo Nome")
        edit_data = st.date_input("Nova Data de Nascimento")
        btn_edit = st.form_submit_button("Atualizar Dados")

        if btn_edit:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE contatos SET nome=%s, data_nascimento=%s WHERE id_contato=%s", 
                            (edit_nome, edit_data, id_editar))
                conn.commit()
                if cur.rowcount > 0:
                    st.success(f"✅ Registro ID {id_editar} atualizado!")
                else:
                    st.error("ID não encontrado.")
                cur.close()
                conn.close()
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao editar: {e}")

# --- 4. DELETE (EXCLUIR) ---
with tab4:
    st.subheader("Excluir Cadastro")
    id_excluir = st.number_input("Informe o ID para remover", step=1, min_value=1)
    confirmar = st.checkbox("Eu confirmo que desejo excluir este registro permanentemente.")
    btn_del = st.button("❌ Excluir Agora", type="primary")

    if btn_del:
        if confirmar:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM contatos WHERE id_contato = %s", (id_excluir,))
                conn.commit()
                if cur.rowcount > 0:
                    st.success(f"🗑️ Registro ID {id_excluir} removido!")
                else:
                    st.error("ID não encontrado.")
                cur.close()
                conn.close()
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir: {e}")
        else:
            st.warning("Marque a caixa de confirmação para prosseguir.")
