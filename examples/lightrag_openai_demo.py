import os
import time
import streamlit as st
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Working directory and model setup
WORKING_DIR = "./dickens"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,
)

with open("../VB_LAW/test.txt", encoding='utf-8') as f:
    rag.insert(f.read())

# Rate limit settings
MAX_TOKENS_PER_MINUTE = 200000
token_count = 0
start_time = time.time()

# Streamlit setup
st.title("Q&A Chat Interface VietNamese Economic Law")
st.write("Enter your query below and see the response interleaved with your question.")
query_input = st.text_input("Your query:")
selected_mode = st.selectbox("Choose a mode:", ["naive", "local", "global", "hybrid"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def rate_limiter(tokens_used):
    global token_count, start_time
    token_count += tokens_used
    current_time = time.time()
    elapsed_time = current_time - start_time

    # If we exceed the token limit, wait for the remainder of the minute
    if token_count > MAX_TOKENS_PER_MINUTE:
        time_to_wait = 60 - elapsed_time
        if time_to_wait > 0:
            st.write(f"Rate limit reached, waiting for {time_to_wait:.2f} seconds...")
            time.sleep(time_to_wait)
        # Reset the token count and start time after waiting
        token_count = 0
        start_time = time.time()
    elif elapsed_time > 60:
        # Reset the token count and start time every minute
        token_count = 0
        start_time = time.time()

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def query_with_backoff(query_text, mode):
    # Estimate token usage (for example, consider 1 token per character as a rough estimate)
    tokens_used = len(query_text)
    rate_limiter(tokens_used)
    while True:
        try:
            # Make the request to the API
            response = rag.query(query_text, param=QueryParam(mode=mode))
            return response
        except Exception as e:
            error_message = str(e)
            if "HTTP/1.1 429 Too Many Requests" in error_message:
                st.write("Received 429 Too Many Requests error. Waiting for 60 seconds...")
                time.sleep(60)  # Wait for 1 minute
            else:
                raise e  # Re-raise the exception if it's not a rate limit issue

# Perform query if input is provided
if query_input:
    st.write(f"Performing {selected_mode} search...")
    try:
        result = query_with_backoff(query_input, mode=selected_mode)
        # Add to chat history
        st.session_state.chat_history.append({"query": query_input, "mode": selected_mode, "response": result})
        # Display chat history interleaved
        for chat in st.session_state.chat_history:
            st.write(f"**You:** {chat['query']}")
            st.write(f"**Law BOT:** {chat['response']}")
            st.write("-" * 100)
    except Exception as e:
        st.write(f"{selected_mode.capitalize()} search failed: {e}")
