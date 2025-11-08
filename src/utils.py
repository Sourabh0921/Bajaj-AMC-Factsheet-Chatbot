import os
from dotenv import load_dotenv
import streamlit as st

def load_env_variables():
    load_dotenv()

def load_styles():
    with open("static/custom_styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
