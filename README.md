# File System LLM Assistant

This project is a Python-based intelligent file system assistant that uses an LLM (OpenAI) to perform tasks on your local file system, such as reading documents (PDF, TXT, DOCX), searching for keywords, listing files, and writing summaries.

It includes a Streamlit web interface so users can securely enter their API keys and interact with the assistant.

## Features (Part A & B)
- **Read Files**: Extract text from `.txt`, `.pdf`, and `.docx` files.
- **List Files**: List files in a directory, with optional extension filtering.
- **Search Files**: Search for keywords in files and return surrounding context.
- **Write Files**: Create and write to text files automatically.
- **LLM Tool Calling**: The OpenAI model automatically determines which tools to call to answer your prompts.
- **Streamlit UI**: A clean chat interface where API keys are entered safely instead of being hardcoded.

## Setup Instructions

1. **Clone the repository / Enter the project directory**:
   ```bash
   cd path/to/llm_fs_assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Dummy Data**:
   This script generates 5-10 random dummy resumes in `.pdf`, `.docx`, and `.txt` format inside the `sample_data/` directory.
   ```bash
   python generate_dummy_data.py
   ```

4. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the UI (typically http://localhost:8501).
2. Enter your **OpenAI API Key** in the sidebar.
3. Try example queries like:
   - *"Read all resumes in the sample_data folder"*
   - *"Find resumes mentioning Python experience"*
   - *"Create a summary file for sample_data/resume_john_doe.txt"*

## Demo
Watch the LLM File System Assistant in action here: demo.webm

<video controls src="demo.webm" title="Title"></video>

