import streamlit as st
from g4f.client import Client
from groq import Groq
import tiktoken

# ==============================================================================
# 🔑 CONFIGURAÇÃO DE SEGURANÇA E CHAVES DE API
# ==============================================================================
# O Streamlit lê automaticamente do arquivo .streamlit/secrets.toml
GROQ_KEY = st.secrets.get("GROQ_API_KEY", None)

# 1. Função para calcular os tokens da OpenAI/Groq (usando a lib oficial tiktoken)
def calcular_tokens(texto, modelo="gpt-4o-mini"):
    try:
        codificador = tiktoken.encoding_for_model(modelo)
    except KeyError:
        codificador = tiktoken.get_encoding("cl100k_base")
    return len(codificador.encode(texto))

# Configuração da página do Streamlit
st.set_page_config(page_title="Multi-Cérebro Bot", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot Multi-API: Escolha o Cérebro")

# Inicializando o histórico de mensagens no formato padrão do mercado (OpenAI/Groq)
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "system", "content": "Você é um assistente virtual criado no curso do SENAI."}
    ]

# ==============================================================================
# 📊 BARRA LATERAL: Configurações e Seletor de IA
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Provedor de IA")
    
    # Seletor simples de modelo
    provedor_selecionado = st.selectbox(
        "Escolha qual IA vai responder:",
        ["GPT-4o Mini (Via G4F)", "Llama 3.3 70B (Via Groq)"]
    )
    
    st.divider()
    
    # Status visual da chave do Groq
    if provedor_selecionado == "Llama 3.3 70B (Via Groq)":
        if not GROQ_KEY:
            st.error("⚠️ 'GROQ_API_KEY' não encontrada no arquivo secrets.toml.")
        else:
            st.success("⚡ Conexão com a Groq ativa!")
            
    st.divider()
    
    # Monitor visual de consumo de tokens
    st.subheader("📊 Monitor de Contexto")
    total_tokens = sum(calcular_tokens(msg["content"]) for msg in st.session_state.mensagens)
    st.metric(label="Tokens Acumulados no Histórico", value=f"{total_tokens} tokens")

# ==============================================================================
# 💬 INTERFACE DO CHAT
# ==============================================================================

# Renderizar histórico de mensagens na tela (ignorando o system prompt oculto)
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Capturar nova mensagem digitada pelo usuário
if prompt := st.chat_input("Digite sua dúvida aqui..."):
    
    # 1. Exibir e salvar a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    # 2. Processar a resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner(f"Processando pelo {provedor_selecionado}..."):
            try:
                # --------------------------------------------------------------
                # OPÇÃO A: G4F (Simula OpenAI)
                # --------------------------------------------------------------
                if provedor_selecionado == "GPT-4o Mini (Via G4F)":
                    client = Client()
                    resposta_api = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.mensagens
                    )
                    texto_resposta = resposta_api.choices[0].message.content

                # --------------------------------------------------------------
                # OPÇÃO B: Groq (Usa a mesma sintaxe da OpenAI!)
                # --------------------------------------------------------------
                elif provedor_selecionado == "Llama 3.3 70B (Via Groq)":
                    if not GROQ_KEY:
                        st.error("Configure a 'GROQ_API_KEY' no arquivo secrets.toml para continuar.")
                        st.stop()
                    
                    client_groq = Groq(api_key=GROQ_KEY)
                    resposta_api = client_groq.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.mensagens
                    )
                    texto_resposta = resposta_api.choices[0].message.content

                # 3. Exibir a resposta final e salvar no histórico
                st.markdown(texto_resposta)
                st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
                st.rerun()

            except Exception as e:
                st.error(f"Erro na comunicação com o provedor {provedor_selecionado}.")
                st.caption(f"Detalhe técnico: {e}")