import streamlit as st
from pages import chatbot, ask_to_pdf, resume_analyzer

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("ChatBot", "AskToPDF", "Resume Analyzer"))

# Load selected page
if page == "ChatBot":
    chatbot.main()
elif page == "AskToPDF":
    ask_to_pdf.main()
elif page == "Resume Analyzer":
    resume_analyzer.main()
