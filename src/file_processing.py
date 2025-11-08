import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import streamlit as st
from tempfile import NamedTemporaryFile
import os

def extract_text_from_pdf_with_images(pdf_file):
    text = ""
    temp_pdf_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_file.read())
            temp_pdf_path = temp_pdf.name
        
        pdf_reader = PdfReader(temp_pdf_path)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        try:
            pdf_images = convert_from_path(temp_pdf_path)  
            for image in pdf_images:
                image_text = pytesseract.image_to_string(image, lang="eng")
                if image_text.strip():
                    text += image_text + "\n"
        except Exception as ocr_error:
            st.warning(f"OCR processing failed, using text extraction only: {ocr_error}")
            
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    finally:
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)
    
    return text.strip()

def process_uploaded_files(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        try:
            text = None
            if uploaded_file.name.endswith(".pdf"):
                text = extract_text_from_pdf_with_images(uploaded_file)
                # print("=========Pdf text==========",text)
            if text and isinstance(text, str) and text.strip():
                documents.append({"content": text, "metadata": {"file_name": uploaded_file.name}})
            else:
                st.warning(f"File '{uploaded_file.name}' could not be processed or is empty.")
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
    return documents