# import streamlit as st
# from g4f.client import Client
# from groq import Groq
# import tiktoken

# # ==============================================================================
# # 🔑 CONFIGURAÇÃO DE SEGURANÇA E CHAVES DE API
# # ==============================================================================
# # O Streamlit lê automaticamente do arquivo .streamlit/secrets.toml
# GROQ_KEY = st.secrets.get("GROQ_API_KEY", None)

# # 1. Função para calcular os tokens da OpenAI/Groq (usando a lib oficial tiktoken)
# def calcular_tokens(texto, modelo="gpt-4o-mini"):
#     try:
#         codificador = tiktoken.encoding_for_model(modelo)
#     except KeyError:
#         codificador = tiktoken.get_encoding("cl100k_base")
#     return len(codificador.encode(texto))

# # Configuração da página do Streamlit
# st.set_page_config(page_title="Multi-Cérebro Bot", page_icon="🤖", layout="wide")
# st.title("🤖 Chatbot Multi-API: Escolha o Cérebro")

# # Inicializando o histórico de mensagens no formato padrão do mercado (OpenAI/Groq)
# if "mensagens" not in st.session_state:
#     st.session_state.mensagens = [
#         {"role": "system", "content": "Você é um assistente virtual criado no curso do SENAI."}
#     ]

# # ==============================================================================
# # 📊 BARRA LATERAL: Configurações e Seletor de IA
# # ==============================================================================
# with st.sidebar:
#     st.header("⚙️ Provedor de IA")
    
#     # Seletor simples de modelo
#     provedor_selecionado = st.selectbox(
#         "Escolha qual IA vai responder:",
#         ["GPT-4o Mini (Via G4F)", "Llama 3.3 70B (Via Groq)"]
#     )
    
#     st.divider()
    
#     # Status visual da chave do Groq
#     if provedor_selecionado == "Llama 3.3 70B (Via Groq)":
#         if not GROQ_KEY:
#             st.error("⚠️ 'GROQ_API_KEY' não encontrada no arquivo secrets.toml.")
#         else:
#             st.success("⚡ Conexão com a Groq ativa!")
            
#     st.divider()
    
#     # Monitor visual de consumo de tokens
#     st.subheader("📊 Monitor de Contexto")
#     total_tokens = sum(calcular_tokens(msg["content"]) for msg in st.session_state.mensagens)
#     st.metric(label="Tokens Acumulados no Histórico", value=f"{total_tokens} tokens")

# # ==============================================================================
# # 💬 INTERFACE DO CHAT
# # ==============================================================================

# # Renderizar histórico de mensagens na tela (ignorando o system prompt oculto)
# for msg in st.session_state.mensagens:
#     if msg["role"] != "system":
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

# # Capturar nova mensagem digitada pelo usuário
# if prompt := st.chat_input("Digite sua dúvida aqui..."):
    
#     # 1. Exibir e salvar a mensagem do usuário
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.mensagens.append({"role": "user", "content": prompt})

#     # 2. Processar a resposta do assistente
#     with st.chat_message("assistant"):
#         with st.spinner(f"Processando pelo {provedor_selecionado}..."):
#             try:
#                 # --------------------------------------------------------------
#                 # OPÇÃO A: G4F (Simula OpenAI)
#                 # --------------------------------------------------------------
#                 if provedor_selecionado == "GPT-4o Mini (Via G4F)":
#                     client = Client()
#                     resposta_api = client.chat.completions.create(
#                         model="gpt-4o-mini",
#                         messages=st.session_state.mensagens
#                     )
#                     texto_resposta = resposta_api.choices[0].message.content

#                 # --------------------------------------------------------------
#                 # OPÇÃO B: Groq (Usa a mesma sintaxe da OpenAI!)
#                 # --------------------------------------------------------------
#                 elif provedor_selecionado == "Llama 3.3 70B (Via Groq)":
#                     if not GROQ_KEY:
#                         st.error("Configure a 'GROQ_API_KEY' no arquivo secrets.toml para continuar.")
#                         st.stop()
                    
#                     client_groq = Groq(api_key=GROQ_KEY)
#                     resposta_api = client_groq.chat.completions.create(
#                         model="llama-3.3-70b-versatile",
#                         messages=st.session_state.mensagens
#                     )
#                     texto_resposta = resposta_api.choices[0].message.content

#                 # 3. Exibir a resposta final e salvar no histórico
#                 st.markdown(texto_resposta)
#                 st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
#                 st.rerun()

#             except Exception as e:
#                 st.error(f"Erro na comunicação com o provedor {provedor_selecionado}.")
#                 st.caption(f"Detalhe técnico: {e}")

import streamlit as st
from g4f.client import Client # Importando o cliente unificado de IA
from groq import Groq
import tiktoken as tik

# O Streamlit lê automaticamente 
# variáveis de ambiente
# do arquivo .streamlit/secrets.toml
GROQ_KEY = st.secrets.get("GROQ_API_KEY",None)

def calcular_tokens(texto, modelo="gpt-4o-mini"):
    try:
        # Puxa o codificador oficial da OpenAI
        # configurado para o modelo
        codificador = tik.encoding_for_model(modelo)
    except KeyError:
        # Caso o modelo seja genérico,
        # usa o padrão do GPT-4
        codificador = tik.encoding_for_model("cl100k_base")
    
    # O método .encode() transformar o texto puro
    # em uma lista de números (IDs dos tokens)
    lista_de_tokens = codificador.encode(texto)

    # Retornar o tamanho dessa lista
    # que é a quantidade exata de tokens
    return len(lista_de_tokens)

# Configuração da página web
st.set_page_config(page_title="AI Chatbot Pro", page_icon="🧠")
st.title("Meu Chatbot com IA Generativa")
st.write(st.secrets.get("PROJETO_SUBTITULO"))

# Inicializando o histórico de mensagens na memória da sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        # Mensagem de sistema que dita o comportamento inicial da IA
        {"role": "system", "content": "Você é um assistente virtual prestativo e bem-humorado criado em sala de aula."}
    ]

# Sidebar (Barra lateral)
with st.sidebar:
    st.header(" Monitor da Infraestrutura")

    # Seletor do modelo
    provedor_selecionado = st.selectbox(
        "Escolha qual IA vai responder",
        [
            "GPT-4o Mini (Via G4F)",
            "Llama 3.3 (Via Groq)"
        ]
    )

    st.divider()

    # Status visual do Groq
    if provedor_selecionado == "Llama 3.3 (Via Groq)":
        st.success(" Conexão com a Groq ativa")
    elif provedor_selecionado == "GPT-4o Mini (Via G4F)":
        st.success(" Conexão com a GPT-4o ativa")

    st.divider()

    st.subheader("Monitor de Contexto")

    # Calcular o total de tokens
    # acumulados no histórico
    total_tokens_prompt = sum(
        calcular_tokens(msg["content"]) 
        for msg in st.session_state.mensagens
    )

    # Exibir um card visual com a métrica
    st.metric(
        label="Tokens de Entrada (Contexto Atual)",
        value=f"{total_tokens_prompt} tokens",
        delta=f"+{calcular_tokens(
            st.session_state.mensagens[-1]["content"]
        )} do último turno" 
        if len(st.session_state.mensagens) > 1 else None
    )

# Renderizar as mensagens anteriores na tela (ignorando a mensagem oculta do 'system')
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Caixa de entrada de texto para o usuário interagir
if prompt := st.chat_input("Envie uma mensagem para a IA..."):
    
    # 1. Exibir e salvar a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    # 2. Chamar a API externa para processar a resposta de forma inteligente
    with st.chat_message("assistant"):
        # Criando um elemento de carregamento visual (spinner) enquanto a internet responde
        with st.spinner("Pensando..."):
            try:
                #requisição oficial de chat completion
                if provedor_selecionado == "GPT-4o Mini (Via G4F)":
                    # Inicializando o cliente da API (O nosso 'garçom' de requisições)
                    client = Client()
                    # Requisição oficial de chat completions
                    resposta_api = client.chat.completions.create(
                        model="gpt-4o-mini", # Especificando o modelo cognitivo desejado
                        messages=st.session_state.mensagens # Enviando TODO o histórico para dar contexto
                    )     
                elif provedor_selecionado == "Llama 3.3 (Via Groq)":
                    if not GROQ_KEY:
                        st.error("Erro de configuração. Contate o administrador do sistema")
                        st.stop()
                        
                    
                    client_groq = Groq(api_key=GROQ_KEY)
                    resposta_api = client_groq.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages = st.session_state.mensagens
                    )
                    
                # Extraindo o texto puro de dentro do payload retornado pela API
                    texto_resposta = resposta_api.choices[0].message.content
                
                    # Exibindo o resultado final processado pela IA na tela do usuário
                    st.markdown(texto_resposta)
                
                    # 3. Salvar a resposta gerada no histórico para manter o contexto na próxima pergunta
                    st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
                    
                
            except Exception as e:
                # Tratamento de erro caso o provedor da API gratuita falhe temporariamente
                st.error("Ops! Tive um problema para conectar ao servidor de IA.")
                st.caption(f"Detalhe técnico do erro: {e}")
