import os
import streamlit as st
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete

# Set up working directory
WORKING_DIR = "./dickens"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# Initialize LightRAG instance
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,
)

# Streamlit UI setup
st.title("RAG Query Interface")

# Input fields
query = st.text_input("Enter your query:", "")
mode = st.selectbox("Select query mode:", ["naive", "local", "global", "hybrid"])

# Use session state to control when the query is executed
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Button to execute the query
if st.button("Submit Query"):
    st.session_state.submitted = True

# Perform the query only after submission
if st.session_state.submitted:
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        query_param = QueryParam(mode=mode)
        try:
            response = rag.query(query, param=query_param)
            st.success("Response:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Reset the submission state after processing
    st.session_state.submitted = False