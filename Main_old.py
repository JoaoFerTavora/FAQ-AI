import streamlit as st
import g4f.client as cl

# Configuração da página web
st.set_page_config(page_title="FAQ Bot SENAI", page_icon= "🤖")
st.title("🤖 ChatBot FAQ versão Web")
st.write("Pergunte sobre horários, cursos e contato")


# faq = {
#          ("horario", "horas", "aberto", "funciona"): "Estamos abertos das 8h às 18h.",
#          ("curso", "cursos", "estudar", "ia", "programação"): "Oferecemos cursos de programação de IA.",
#          ("contato", "telefone", "whatsapp", "ligar", "fone"): "Nosso telefone é (14) 1234-5678."
#      }

# Inicializando o cliente da api (O ´garçom´ do pedido)
client = cl.Client()

# 

# Iniciando o histórico de mensagens
# Na memória da página via Seção
if "historico" not in st.session_state:
    st.session_state.historico = [
    # Mensagem do sistema que dita o comportamento inicial da IA
    {"role":"system","content":"Você é um assistente virtual bem-humorado do SENAI São Paulo"}
    ]# inicio da seção vazia

# Exibir as mensagens anteriores
# que já estão salvas no histórico
for mensagem in st.session_state.historico:
    if mensagem["role"] != "system":
        with st.chat_message(mensagem["role"]):
            st.markdown(mensagem["content"])

    

# Capturar entrada do usuário
if pergunta_usuario:= st.chat_input("Digite sua dúvida aqui..."):
    # Mostrar a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)
    
    # Salvar a pergunta no histórico EM MEMÓRIA
    st.session_state.historico.append({"role":"user", "content": pergunta_usuario})

    # Processar a resposta usando o dicionário
    termo_busca = pergunta_usuario.lower()

    # Busca simplificada or palavra-chave
    # resposta_bot = "Desculpe, ainda sou um robô limitado. Não entendi a pergunta..."
    # for chave in faq:
    #     for ch in chave:
    #         if ch in termo_busca:
    #             resposta_bot=faq[chave]
    #             break

    

    # Mostra a resposta do robô na tela
    #with st.chat_message("assistant"):
    #    st.markdown(resposta_bot)    

    # Salvar a resposta no histórico da memória
    #st.session_state.historico.append({"role":"assistant","content":resposta_bot})


    # Chamar a API externa para processar a resposta
    with st.chat_message("assistant"):
        # Criar um elemento de carregamento visual (spinner)
        with st.spinner("Pensando..."):
            try:
                # Requisição oficial de chat completions
                resposta_api = client.chat.completions.create(
                    model = "gpt-4o-mini", # Especificando o modelo
                    messages = st.session_state.mensagem # enviar TODO o histórico
                )

                # Extrair o texto puro de dentro do payload retornado pela API
                # payload (carga útil): traz um dicionário com a resposta enviada 
                texto_resposta = resposta_api.choices[0].message.content

                # Exibir o resultado final processado pela IA
                st.markdown(texto_resposta)

                # Salvar a resposta gerada no histórico
                # para manter o contexto na próxima pergunta
                st.session_state.mensagem.append({"role":"assitant","content":texto_resposta})

            except Exception as e:
                # Tratamento de erro caso o provedor da API gratuita falhe
                st.error("Ops! Tive um problema para conectar ao servidor de IA")
                st.caption(f"Detalhe técnico do erro: {e}")

