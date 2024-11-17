"""
Streamlit application for a ChatBot using Ollama.

This application allows users to interact with an AI chatbot powered by a selected language model.
"""

import streamlit as st
import ollama
import logging

# Streamlit page configuration
st.set_page_config(
    page_title="ChatBot with Ollama",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def process_message(user_message: str, model: str = "Phi3.5") -> str:
    """
    Generate a response using the Ollama API with improved handling of responses.

    Args:
        user_message (str): The user's input or question.
        model (str): The name of the language model (default: Phi3.5).

    Returns:
        str: The AI-generated response or an error message.
    """
    try:
        # Call the Ollama API to generate a response
        api_response = ollama.generate(model=model, prompt=user_message)
        logger.info(f"Ollama API raw response: {api_response}")
        
        # Extract the main chatbot response from the 'response' key
        bot_reply = api_response.get("response", "").strip()  # Safely get the response key
        
        if not bot_reply:
            # Handle the case where the response is empty
            logger.error("The response from the AI model is empty or invalid.")
            return "Error: The AI did not return a valid response."

        return bot_reply

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"Error: {str(e)}"


# Main ChatBot UI
st.title("🤖 ChatBot with Ollama")
st.markdown("Interact with the AI chatbot! Type your questions below, and the chatbot will respond.")

# Sidebar for model selection
available_models = ollama.list()
model_names = [model["name"] for model in available_models.get("models", [])]
selected_model = st.sidebar.selectbox("Select a model for the ChatBot", model_names, index=0)

# Chat History Display
with st.container():
    st.write("### Chat History")
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Bot:** {message['content']}")

# User Input for Chat
prompt = st.chat_input("Type your message here...")
if prompt:
    # Display the user's message instantly
    with st.chat_message("user", avatar="😎"):
        st.markdown(prompt)
    
    # Save user message in session state
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Generate bot response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Processing..."):
            bot_response = process_message(user_message=prompt, model=selected_model)
            st.markdown(bot_response)  # Display bot's response instantly

    # Save bot response in session state
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
# Clear Chat Button
if st.sidebar.button("Clear Chat"):
    st.session_state["messages"] = []
    st.experimental_rerun()
