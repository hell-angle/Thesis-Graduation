import os
import time
import streamlit as st
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete

# Working directory and model setup
WORKING_DIR = "./dickens"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,
)

# Đọc toàn bộ nội dung file
# with open("./output_chunks_merged.txt", encoding='utf-8') as f:
#     rag.insert(f.read())

# # Tách nội dung thành các chunk riêng biệt
# chunks = content.split("Chunk")[1:]  # Bỏ phần trống đầu tiên
# chunks = [chunk.strip() for chunk in chunks]

# # Nạp từng chunk vào RAG
# for chunk in chunks:
#     full_chunk = "Chunk" + chunk
#     print(full_chunk[:20000])
#     rag.insert([full_chunk])

# Streamlit setup
st.title("Q&A Chat Interface VietNamese Economic Law")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
selected_mode = st.selectbox("Choose a mode:", ["naive", "local", "global", "hybrid"])

# Basic error handling for querying
def basic_query(query_text, mode):
    try:
        response = rag.query(query_text, param=QueryParam(mode=mode))
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Accept user input
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            response = basic_query(prompt, mode=selected_mode)
            if response:
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
