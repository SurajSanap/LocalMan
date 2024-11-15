import streamlit as st
import logging
from langchain.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

def main():
    st.title("ChatBot")
    st.write("Chat with an AI assistant based on selected models")

    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Function to process user question
    def process_question(question: str, model_name: str) -> str:
        # Initialize model
        llm = ChatOllama(model=model_name)
        
        # Define query prompt
        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="Generate alternative versions for: {question}"
        )

        # Setup retriever
        retriever = MultiQueryRetriever.from_llm(
            llm,
            prompt=QUERY_PROMPT
        )
        
        # Define answer prompt
        answer_template = """Answer the question based ONLY on the following context:
        Context: {context}
        Question: {question}"""
        
        prompt = PromptTemplate(input_variables=["context", "question"], template=answer_template)
        
        # Chain to process answer
        response_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        response = response_chain.invoke(question)
        return response
    
    # User prompt
    question = st.text_input("Enter your question:")
    model_name = st.selectbox("Choose a model:", ["Model A", "Model B"])  # Replace with actual model options
    
    if question:
        st.write("Processing...")
        response = process_question(question, model_name)
        st.write("Response:", response)
