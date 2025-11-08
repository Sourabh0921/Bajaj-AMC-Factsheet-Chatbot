import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
import streamlit as st
import pandas as pd
from src.vector_store import vector_embedding
from src.chat_chain import handle_query
from src.file_processing import process_uploaded_files
import base64

from src.utils import load_env_variables

st.set_page_config(page_title="Bajaj AMC Factsheet Chatbot")

load_env_variables()

with st.sidebar:
    uploaded_files = st.sidebar.file_uploader(
        "Upload your documents (PDF)",
        accept_multiple_files=True,
        type=['pdf']
    )

    if st.sidebar.button("Embed Documents") and uploaded_files:
        with st.spinner("Processing and embedding documents..."):
            processed_docs = process_uploaded_files(uploaded_files)
            # print("----Extracted_text--",processed_docs)
            
            if processed_docs:
                vector_embedding(processed_docs)
                st.success("Documents embedded successfully!")
            else:
                st.error("No valid documents were processed!")

st.header("Ask a Question")
prompt1 = st.text_input("Enter Your Question:")

if prompt1:
    if "vectors" not in st.session_state:
        st.error("Please upload and embed documents first!")
    else:
        response, context_docs, response_time = handle_query(prompt1)
        st.write("Response Time:", round(response_time, 2), "seconds")
        st.subheader("Answer:")
        st.write(response)

        with st.expander("Document Similarity Search Results"):
            for i, doc in enumerate(context_docs):
                st.write(f"**Document {i+1}:**")
                st.write(doc.page_content)
                st.write(f"**Source:** {doc.metadata['file_name']}")
                st.write("--------------------------------")