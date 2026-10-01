from os import environb
import os

import streamlit as st
from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from sympy.codegen import Print

load_dotenv()
DATA_DIR = "data"
Settings.llm = GoogleGenAI(model="gemini-2.5-flash")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def get_query_engine():
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        st.error("MISSING API KEY")
        st.stop()

    reader = SimpleDirectoryReader("data")
    documents = reader.load_data()

    return index.as_query_engine()
    index = VectorStoreIndex.from_documents(documents)

st.title("Handbook Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question := st.chat_input("Ask a question about the handbook..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    query_engine = get_query_engine()
    response = query_engine.query(question)

    st.session_state.messages.append({"role": "assistant", "content": response.response})
    with st.chat_message("assistant"):
        st.write(response.response)
