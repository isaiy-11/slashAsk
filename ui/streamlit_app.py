import streamlit as st
import requests
import uuid
import os

# Configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.session_state.setdefault("session_id", str(uuid.uuid4()))
st.session_state.setdefault("chat_history", [])

st.set_page_config(
    page_title="slashAsk | Intelligent Document Q&A",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Professional CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium UI Styling */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 1px solid #E0E4E8;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

st.title("SlashAsk")
st.caption("Ask questions and extract insights from your documents instantly.")

st.sidebar.title("Document Management")

# Active Session details
st.sidebar.write("Active Session ID:")
st.sidebar.code(st.session_state.session_id)

# Clear Chat Button
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()

# Load Existing Session
st.sidebar.subheader("Resume Past Session")
load_session_id = st.sidebar.text_input("Enter Session ID to Load", key="load_session_input")
if st.sidebar.button("Load Session"):
    if load_session_id.strip():
        try:
            response = requests.get(f"{API_URL}/history/{load_session_id.strip()}")
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    st.sidebar.error(f"Error: {data['error']}")
                else:
                    st.session_state.session_id = data["session_id"]
                    st.session_state.chat_history = data["history"]
                    st.sidebar.success("Session loaded successfully!")
                    st.rerun()
            else:
                st.sidebar.error(f"Failed to load session ({response.status_code})")
        except Exception as e:
            st.sidebar.error(f"Error loading session: {e}")
    else:
        st.sidebar.warning("Please enter a Session ID first")

# ==========================
# Upload Document
# ==========================
st.sidebar.divider()
st.sidebar.subheader("Upload Sources")

uploaded_file = st.sidebar.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "xlsx", "xls", "csv", "txt"]
)

if uploaded_file:
    if st.sidebar.button("Process Document"):
        with st.spinner("Uploading and processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API_URL}/upload", files=files)
            if response.status_code == 200:
                st.sidebar.success("Document uploaded successfully")
            else:
                st.sidebar.error(f"Failed to upload document ({response.status_code})")

url = st.sidebar.text_input("Enter Website URL")

if st.sidebar.button("Process URL"):
    with st.spinner("Extracting from URL..."):
        response = requests.post(f"{API_URL}/upload-url", json={"url": url})
        if response.status_code != 200:
            st.sidebar.error(f"Backend error ({response.status_code})")
        else:
            st.sidebar.success("URL processed successfully")

# ==========================
# Available Documents
# ==========================
st.sidebar.divider()
st.sidebar.subheader("Available Documents")

if st.sidebar.button("Refresh Document List"):
    try:
        response = requests.get(f"{API_URL}/documents")
        st.sidebar.json(response.json())
    except Exception as e:
        st.sidebar.error(f"Error fetching documents: {e}")

# ==========================
# Get Documents
# ==========================
try:
    response = requests.get(f"{API_URL}/documents")
    docs = response.json()["documents"]
except Exception:
    docs = []

# ==========================
# Chat Section
# ==========================
st.subheader("Chat")

if len(docs) > 0 or os.path.exists("vector_store/indexes/master.index"):
    # Display Previous Chat History
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["question"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    # Enter to Submit
    question = st.chat_input("Ask a question about the document...")

    if question:  
        payload = {
            "question": question,
            "session_id": st.session_state.session_id
        }
        with st.spinner("Generating answer..."):
            response = requests.post(f"{API_URL}/ask-document", json=payload)
            
        if response.status_code != 200:
            st.error(f"Backend error ({response.status_code})")
            st.write("Response:")
            st.code(response.text)
        else:
            try:
                data = response.json()
                answer = data.get("answer")
                if answer is None:
                    st.error("No 'answer' key found in API response.")
                    st.json(data)
                    st.stop()
            except Exception as e:
                st.error(f"Error parsing response: {e}")
                st.code(response.text)
                st.stop()
                
            # Store Chat History
            st.session_state.chat_history.append({
                "question": question,
                "answer": answer
            })
            st.rerun()
else:
    st.info("No documents or URLs uploaded yet. Upload a document or enter a URL in the sidebar to start chatting.")

# ==========================
# Delete Document
# ==========================
st.sidebar.divider()
st.sidebar.subheader("Delete Document")

try:
    if len(docs) > 0:
        doc_to_delete = st.sidebar.selectbox("Select Document to Delete", docs, key="delete_doc")
        if st.sidebar.button("Delete Document"):
            response = requests.delete(f"{API_URL}/document/{doc_to_delete}")
            if response.status_code == 200:
                st.sidebar.success("Document deleted successfully")
            else:
                st.sidebar.error(f"Error deleting document ({response.status_code})")
except Exception as e:
    st.sidebar.error(f"Error in delete section: {str(e)}")

# ==========================
# Document Details
# ==========================
st.sidebar.divider()
st.sidebar.subheader("Document Details")

try:
    if len(docs) > 0:
        details_doc = st.sidebar.selectbox("Select Document", docs, key="details_doc")
        if st.sidebar.button("Get Details"):
            response = requests.get(f"{API_URL}/document-details/{details_doc}")
            if response.status_code == 200:
                st.sidebar.json(response.json())
            else:
                st.sidebar.error(f"Error fetching details ({response.status_code})")
except Exception as e:
    st.sidebar.error(f"Error in details section: {str(e)}")