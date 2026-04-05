import streamlit as st
import os
from llm_file_assistant import LLMFileAssistant

st.set_page_config(page_title="File System LLM Assistant", page_icon="📁", layout="wide")

st.title("📁 File System LLM Assistant")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here.")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
    st.markdown("---")
    st.markdown("### Example Queries")
    st.markdown("- *Read all resumes in the Downloads folder*")
    st.markdown("- *Find resumes mentioning Python experience in Downloads*")
    st.markdown("- *Create a summary file for Downloads/resume_john_doe.pdf*")

if not api_key:
    st.info("Please enter your OpenAI API key in the sidebar to begin.")
    st.stop()

# Initialize session state for chat and assistant
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful file system assistant. You can read, write, list, and search files locally using the tools provided. When a user asks you to interact with 'resumes' or the 'Downloads folder', assume the path is 'C:/Users/disha/Downloads'. Always use the tools when users ask you to interact with files. If a user asks to summarize a file, read it first, then summarize."}
    ]

try:
    assistant = LLMFileAssistant(api_key=api_key, model_name=model)
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    st.stop()

# Display chat messages (excluding system prompt and tool calls logic for clean UI)
for msg in st.session_state.messages:
    # Handle both dicts and OpenAI objects seamlessly
    role = msg.get("role") if isinstance(msg, dict) else msg.role
    content = msg.get("content") if isinstance(msg, dict) else msg.content
    
    if role == "user":
        st.chat_message("user").write(content)
    elif role == "assistant" and content:
        st.chat_message("assistant").write(content)
    elif role == "tool":
        name = msg.get("name", "tool") if isinstance(msg, dict) else getattr(msg, "name", "tool")
        with st.expander(f"Tool Result: {name}"):
            st.code(content)

# Chat input
if prompt := st.chat_input("Enter your command (e.g., 'Read all resumes...')"):
    # Display user input
    st.chat_message("user").write(prompt)
    
    with st.spinner("Processing..."):
        try:
            # We already have history in session_state, pass it
            response, updated_messages = assistant.process_query(prompt, st.session_state.messages)
            st.session_state.messages = updated_messages
            
            # Since process_query might have appended tool messages and assistant messages,
            # we need to force a rerun so everything renders correctly from the loop above,
            # but wait, streamlit reruns from top to bottom. We actually just need to write the response.
            # Rerunning is better to render the newly added tool expanders and final response properly.
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

