import streamlit as st
import uuid
import os

# Import backend services directly
from app.services.session_service import get_history
from app.services.document_processing_service import process_document
from app.services.url_processing_service import process_url
from app.services.rag_service import ask_document

# Ensure required storage directories exist
for _folder in (
    "uploads",
    "vector_store/indexes",
    "vector_store/chunks",
):
    os.makedirs(_folder, exist_ok=True)

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
            raw_history = get_history(load_session_id.strip())
            
            # Convert raw history list of dicts to the question-answer pair format expected by the UI
            formatted_history = []
            current_pair = {}
            for msg in raw_history:
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    current_pair["question"] = content
                elif role == "assistant":
                    current_pair["answer"] = content
                    if "question" in current_pair:
                        formatted_history.append(current_pair)
                        current_pair = {}
            
            st.session_state.session_id = load_session_id.strip()
            st.session_state.chat_history = formatted_history
            st.sidebar.success("Session loaded successfully!")
            st.rerun()
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
            try:
                file_path = os.path.join("uploads", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                result = process_document(file_path)
                st.sidebar.success("Document uploaded successfully")
            except Exception as e:
                st.sidebar.error(f"Failed to upload document: {e}")

url = st.sidebar.text_input("Enter Website URL")

if st.sidebar.button("Process URL"):
    with st.spinner("Extracting from URL..."):
        try:
            result = process_url(url)
            st.sidebar.success("URL processed successfully")
        except Exception as e:
            st.sidebar.error(f"Backend error: {e}")

# ==========================
# Available Documents
# ==========================
st.sidebar.divider()
st.sidebar.subheader("Available Documents")

if st.sidebar.button("Refresh Document List"):
    try:
        documents = os.listdir("uploads")
        st.sidebar.json({"total_documents": len(documents), "documents": documents})
    except Exception as e:
        st.sidebar.error(f"Error fetching documents: {e}")

# ==========================
# Get Documents
# ==========================
try:
    docs = os.listdir("uploads")
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
        with st.spinner("Generating answer..."):
            try:
                answer = ask_document(
                    question,
                    "vector_store/indexes/master.index",
                    "vector_store/chunks/master.pkl",
                    st.session_state.session_id
                )
                
                # Store Chat History
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer
                })
                st.rerun()
            except Exception as e:
                st.error(f"Error parsing response: {e}")
                st.stop()
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
            upload_path = f"uploads/{doc_to_delete}"
            index_path = f"vector_store/indexes/{doc_to_delete}.index"
            chunk_path = f"vector_store/chunks/{doc_to_delete}.pkl"
            
            if os.path.exists(upload_path): os.remove(upload_path)
            if os.path.exists(index_path): os.remove(index_path)
            if os.path.exists(chunk_path): os.remove(chunk_path)
            
            st.sidebar.success("Document deleted successfully")
            st.rerun()
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
            upload_path = f"uploads/{details_doc}"
            index_path = f"vector_store/indexes/{details_doc}.index"
            chunk_path = f"vector_store/chunks/{details_doc}.pkl"
            
            if not os.path.exists(upload_path):
                st.sidebar.error("Document not found")
            else:
                file_size = os.path.getsize(upload_path)
                st.sidebar.json({
                    "document_name": details_doc,
                    "file_size_kb": round(file_size / 1024, 2),
                    "index_exists": os.path.exists(index_path),
                    "chunk_exists": os.path.exists(chunk_path)
                })
except Exception as e:
    st.sidebar.error(f"Error in details section: {str(e)}")