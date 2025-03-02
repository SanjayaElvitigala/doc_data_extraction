import requests
import ollama
import numpy as np


__all__ = [
    "filter_json_output",
    "get_json_summary_hugging_face",
    "get_json_summary_local_llm",
]


def filter_json_output(text):
    dict_open_bracket_indexes = []
    dict_close_bracket_indexes = []

    for index, element in enumerate(text):
        if element == "{":
            dict_open_bracket_indexes.append(index)
        elif element == "}":
            dict_close_bracket_indexes.append(index)

    json_start = int(np.min(dict_open_bracket_indexes))
    json_end = int(np.max(dict_close_bracket_indexes))

    return text[json_start : json_end + 1]


def get_json_summary_hugging_face(
    text, token, llm_id="meta-llama/Llama-3.2-3B-Instruct"
):

    HUGGING_FACE_MODEL_ID = llm_id

    TOKEN = token
    API_URL = f"https://api-inference.huggingface.co/models/{HUGGING_FACE_MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "x-use-cache": "false",
    }

    prompt_base = """summarize the following into a structured json format and give the type of document classification which is a must. 
    DON'T NEED INSTRUCTIONS OR ADDITIONAL INFORMATION. """
    data = {"inputs": prompt_base + text, "response_format": {"type": "json"}}
    response = requests.post(API_URL, headers=headers, json=data)

    try:
        if isinstance(response.json(), dict):
            if "error" in response.json().keys():
                error_value = response.json()["error"]
                return f"Error: {error_value}"
            else:
                return f"{response.json()}"
        elif isinstance(response.json(), list):

            llm_output = f"{response.json()[0]['generated_text']}".replace(
                prompt_base, ""
            )
            return llm_output

    except Exception as e:
        return str(e)


def get_json_summary_local_llm(text, llm_id="llama3.2:3b-instruct-q2_K"):

    prompt_base = """summarize the following into a structured json format and give the type of document classification which is a must. 
    DON'T NEED INSTRUCTIONS OR ADDITIONAL INFORMATION. """
    # Get a list of locally available models
    models = ollama.list()

    # Extract model names
    model_names = [model["model"] for model in models["models"]]

    if not (llm_id in model_names):
        return f"Please download the llm model: {llm_id}"
    else:
        response = ollama.chat(
            model=llm_id,
            messages=[
                {
                    "role": "system",
                    "content": "you are document summarizer and classifier",
                },
                {
                    "role": "user",
                    "content": prompt_base + text,
                },
            ],
            format="json",
        )

        return response["message"]["content"].replace(prompt_base, "")
