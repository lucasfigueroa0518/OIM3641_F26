from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings
import streamlit as st
load_dotenv()

DATA_DIR = Path("data/handbook")

load_dotenv()

def get_api_key():
    """Return the Gemini API key or stop the app if it is missing."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "GEMINI_API_KEY is missing. "
            "Add GEMINI_API_KEY=your_key to your .env file."
        )
        st.stop()
    return api_key

def validate_data_directory():
    """Check that the data directory exists"""
    if not DATA_DIR.exists() or not DATA_DIR.is_dir():
        st.error(
            f"Data directory '{DATA_DIR}' was not found. "
            f"Create this folder and add your handbook files."
        )
        st.stop()

    files = [
        file for file in DATA_DIR.iterdir()
        if file.is_file() and not file.name.startswith(".")
    ]
    if not files:
        st.error(
            f"Data directory '{DATA_DIR}' is empty. "
            f"Add at least one document before running the chatbot."
        )
        st.stop


Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash",
    api_key=api_key
)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


@st.cache_resource
def get_query_engine(api_key):
    """Build and return the cached RAG query engine."""
    Settings.llm = GoogleGenAI(
        model="gemini-2.5-flash",
        api_key=api_key
    )
    documents = SimpleDirectoryReader("data/handbook").load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()

st.title("Bare Bones Rag Chatbot")
api_key= get_api_key()
validate_data_directory()

# everything above is setting up the function to get the query engine function and the api key and llm and
# the streamlit title

try:
    query_engine = get_query_engine(api_key)

except Excesption as e:
    st.error(
        f"Could not build the query engine: {e}"
    )
    st.stop()

prompt = st.chat_input("Ask me anything...")
if prompt:
    st.write(f"User: {prompt}")

    try:
        response = query_engine.query(prompt)
        bot_response = response.response

        with st.chat_message("assistant"):
            st.chat_message(f"Bot response: {bot_response}")

except Exception as e:
    st.error(
        f"Your question could not be processed"
    )






