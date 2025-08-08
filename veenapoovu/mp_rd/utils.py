import os
import openai
import streamlit as st
from datetime import datetime
from streamlit.logger import get_logger
from langchain.chat_models import ChatOllama
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

logger = get_logger('Langchain-Chatbot')

# Decorator to handle chat history
def enable_chat_history(func):
    # Clear cache when switching chatbots
    current_page = func.__qualname__
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except:
            pass

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
    # Display chat messages
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Display message in chat UI"""
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def choose_custom_openai_key():
    """Handle custom OpenAI key input"""
    openai_api_key = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        placeholder="sk-...",
        key="SELECTED_OPENAI_API_KEY"
    )
    if not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
        st.info("Obtain your key from: https://platform.openai.com/account/api-keys")
        st.stop()

    try:
        client = openai.OpenAI(api_key=openai_api_key)
        available_models = [
            model.id for model in client.models.list().data 
            if "gpt" in model.id
        ]
        available_models = sorted(available_models)
        
        model = st.sidebar.selectbox(
            label="Model Version",
            options=available_models,
            index=len(available_models)-1 if available_models else 0,
            key="SELECTED_OPENAI_MODEL"
        )
        return model, openai_api_key
    except openai.AuthenticationError as e:
        st.error(e.body["message"])
        st.stop()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()

def configure_llm():
    """Configure the language model"""
    available_llms = ["gpt-4o-mini", "Custom OpenAI API Key"]
    
    llm_opt = st.sidebar.radio(
        label="LLM Selection",
        options=available_llms,
        key="SELECTED_LLM"
    )
    
    if llm_opt == "gpt-4o-mini":
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            streaming=True,
            api_key=st.secrets.get("OPENAI_API_KEY")
        )
    else:
        model, openai_api_key = choose_custom_openai_key()
        llm = ChatOpenAI(
            model_name=model,
            temperature=0,
            streaming=True,
            api_key=openai_api_key
        )
    return llm

@st.cache_resource
def configure_embedding_model():
    from huggingface_hub import snapshot_download
    
    # Pre-download model with retry logic
    snapshot_download(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        local_dir="./models",
        resume_download=True,
        max_workers=4
    )
    
    return HuggingFaceEmbeddings(
        model_name="./models",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

def print_qa(cls, question, answer):
    """Log Q&A sessions"""
    log_str = "\n[Session] {}\n[Question] {}\n[Answer] {}\n{}".format(
        cls.__name__,
        question,
        answer,
        "-"*50
    )
    logger.info(log_str)



