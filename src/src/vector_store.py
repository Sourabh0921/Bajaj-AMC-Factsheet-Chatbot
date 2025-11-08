from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.file_processing import process_uploaded_files
from langchain.schema import Document
import streamlit as st
import os


def vector_embedding(uploaded_files):
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

        if not extracted_docs:
            st.error("No valid documents were uploaded.")
            return

        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        final_documents = []
        for doc in extracted_docs:
            chunks = st.session_state.text_splitter.split_text(doc["content"])
            for chunk in chunks:
                final_documents.append(Document(page_content=chunk, metadata=doc["metadata"]))
        
        st.session_state.vectors = FAISS.from_documents(final_documents, st.session_state.embeddings)
    else:
        st.info("Vector store is already initialized.")

