import os
import time
import streamlit as st
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete

WORKING_DIR = "./dickens"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,
)

# Read the entire content file
with open("./output_chunks_merged.txt", encoding='utf-8') as f:
    content = f.read()

# Split content into chunks
chunks = content.split("Chunk")[1:]  # Remove first empty part
chunks = [chunk.strip() for chunk in chunks]

# Insert chunks with 1-second delay
for chunk in chunks:
    full_chunk = "Chunk" + chunk
    print(f"Inserting chunk (first 20 characters): {full_chunk[:20]}")
    rag.insert([full_chunk])
    
    # Sleep for 1 second between chunk insertions
    time.sleep(1)

# Perform local search as an example
print(
    rag.query("Định nghĩa luật đấu thầu?", param=QueryParam(mode="local"))
)