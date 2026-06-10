import streamlit as st
import requests
import uuid

# Initialize Session State

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.session_state.setdefault(
    "session_id",
    str(uuid.uuid4())
)

st.session_state.setdefault(
    "chat_history",
    []
)

st.set_page_config(
    page_title="slashAsk",
    layout="wide"
)

st.title("🚀 slashAsk")
st.caption("Ask questions from your documents instantly")

st.sidebar.title("📂 Document Management")
st.sidebar.info(
    f"Session ID: {st.session_state.session_id[:8]}"
)

# ==========================
# Chat History Initialization
# ==========================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(
        uuid.uuid4()
    )
st.sidebar.info(
    f"Session ID: {st.session_state.get('session_id', '')[:8]}"
)

# Clear Chat Button
if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.chat_history = []

    st.session_state.session_id = str(
        uuid.uuid4()
    )

    st.rerun()


# ==========================
# Upload Document
# ==========================

uploaded_file = st.sidebar.file_uploader(
    "Upload Document",
    type=[
        "pdf",
        "docx",
        "xlsx",
        "xls",
        "csv",
        "txt"
    ]
)

if uploaded_file:

    if st.sidebar.button("Upload"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue()
            )
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        st.sidebar.success(
            "Document uploaded successfully"
        )

# ==========================
# Available Documents
# ==========================

st.sidebar.divider()

st.sidebar.subheader(
    "Available Documents"
)

if st.sidebar.button("Load Documents"):

    response = requests.get(
        "http://127.0.0.1:8000/documents"
    )

    st.sidebar.json(
        response.json()
    )

# ==========================
# Get Documents
# ==========================

try:

    response = requests.get(
        "http://127.0.0.1:8000/documents"
    )

    docs = response.json()["documents"]

except Exception:

    docs = []

# ==========================
# Chat Section
# ==========================

st.subheader("💬 Chat")

if len(docs) > 0:

    selected_doc = st.selectbox(
        "Select Document",
        docs
    )

    # Display Previous Chat History

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(
                chat["question"]
            )

        with st.chat_message("assistant"):
            st.write(
                chat["answer"]
            )

    # Enter to Submit

    question = st.chat_input(
        "Ask a question about the document..."
    )

    if question:

        payload = {
            "document_name": selected_doc,
            "question": question,
            "session_id": st.session_state.session_id
        }   

        response = requests.post(
            "http://127.0.0.1:8000/ask-document",
            json=payload
        )

        answer = response.json()["answer"]

        # Store Chat History

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.rerun()

else:

    st.warning(
        "No documents uploaded."
    )

# ==========================
# Delete Document
# ==========================

st.sidebar.divider()

st.sidebar.subheader(
    "Delete Document"
)

try:

    if len(docs) > 0:

        doc_to_delete = st.sidebar.selectbox(
            "Select Document to Delete",
            docs,
            key="delete_doc"
        )

        if st.sidebar.button(
            "Delete Document"
        ):

            response = requests.delete(
                f"http://127.0.0.1:8000/document/{doc_to_delete}"
            )

            st.sidebar.success(
                "Document deleted successfully"
            )

            st.sidebar.json(
                response.json()
            )

except Exception as e:

    st.error(str(e))

# ==========================
# Document Details
# ==========================

st.sidebar.divider()

st.sidebar.subheader(
    "Document Details"
)

try:

    if len(docs) > 0:

        details_doc = st.sidebar.selectbox(
            "Select Document",
            docs,
            key="details_doc"
        )

        if st.sidebar.button(
            "Get Details"
        ):

            response = requests.get(
                f"http://127.0.0.1:8000/document-details/{details_doc}"
            )

            st.sidebar.json(
                response.json()
            )

except Exception as e:

    st.error(str(e))