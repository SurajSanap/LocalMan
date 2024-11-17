import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Welcome to PDF RAG App",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Main Content
st.title("Welcome to the PDF Retrieval-Augmented Generation (RAG) App! 🎉")
st.markdown(
    """
    This application leverages advanced AI models like **Phi3.5** for various features, including:
    - Chat-With-PDF functionality
    - ChatBot Integration
    - Applicant Tracking System (ATS)
    - Resume Analysis

    Navigate to the desired feature using the sidebar.
    """
)
