import streamlit as st
pagina_chat = st.Page(chat_view.py, title = "Consultor SENAI", default = True)
pagina_admin = st.Page(chat_admin.py, title = "Painel ADMIN", default = True)

pg = st.navigation({
    "Atendimento" : [pagina_chat],
    "Gerenciamento" : [pagina_admin]
})

pg.run()