# Environment Setup

## Install Poetry
Poetry is a project and virtual environment management tool. If you haven't installed it yet, run the following command in your global Python environment:

```bash
pip install poetry
```

## Set Up the Virtual Environment
Ensure that `pyproject.toml` is in your current working directory, then run the following commands in the terminal:

```bash
poetry shell
poetry install
```

This will create a virtual environment and install all dependencies listed in the `pyproject.toml` file.

---

# LLM Setup

## Using a Hugging Face Model
1. Create an account on [Hugging Face](https://huggingface.co/).
2. Generate a personal access token from [Hugging Face Tokens](https://huggingface.co/settings/tokens).
3. When selecting the "HuggingFace API" option in the Streamlit UI, input the token in the provided password input field to authenticate the inference API.

## Using a Locally Downloaded LLM
1. Download and install the Ollama software from [Ollama](https://ollama.com/) according to your system.
2. Verify installation by running:

   ```bash
   ollama
   ```

3. To use the `llama3.2:3b-instruct-q2_K` model, pull it by running:

   ```bash
   ollama pull llama3.2:3b-instruct-q2_K
   ```

---

# Application Usage

## Supported File Types
- PDF files
- Image files (`.jpg`, `.png`)

## Text Extraction Process
1. Text is extracted from supported files and displayed in JSON format.
2. For images, EasyOCR is used for text extraction.
3. The extracted text is refined into a structured JSON format using an LLM.

## LLM Modes
This application supports two modes for using LLMs:
1. **Hugging Face Inference API** (via personal access token)
2. **Locally Downloaded LLMs** (using Ollama software)

---

# Running the Application
To start the Streamlit application, run:

```bash
streamlit run ./streamlit_UI.py
```
# Application Layout

![Application Screenshot](images\app.jpg)
