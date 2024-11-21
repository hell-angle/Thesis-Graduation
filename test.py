
import os
import time
import streamlit as st
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete

#########
# Uncomment the below two lines if running in a jupyter notebook to handle the async nature of rag.insert()
# import nest_asyncio
# nest_asyncio.apply()
#########

WORKING_DIR = "./dickens"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,  # Use gpt_4o_mini_complete LLM model
    # llm_model_func=gpt_4o_complete  # Optionally, use a stronger model
)

with open("./output_chunks_merged.txt", "r", encoding="utf-8") as f:
    rag.insert(f.read())


# Perform local search
print(
    rag.query("Định nghĩa luật đấu thầu?", param=QueryParam(mode="local"))
)

