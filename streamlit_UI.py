import streamlit as st

from services.text_extraction_service import get_text_from_image
from services.llm_service import (
    get_json_summary_hugging_face,
    get_json_summary_local_llm,
    filter_json_output,
)
from services.pdf_reader_service import get_pdf_text
from config import (
    HUGGING_FACE_LLM_ID,
    HUGGING_FACE_SELECT,
    LOCAL_LLM_SELECT,
    LOCAL_LLM_ID,
    PDF_FILE_TYPES,
    IMAGE_FILE_TYPES,
    ALLOWED_FILE_TYPES,
    HUGGING_FACE_API_RETRIES,
)


def get_response_llm(
    text_input, llm_option, token=None, n_retries=HUGGING_FACE_API_RETRIES
):
    if llm_option == HUGGING_FACE_SELECT:
        if (token != None) and (token != ""):

            for retry_i in range(n_retries):
                llm_response = get_json_summary_hugging_face(
                    text=text_input, token=token, llm_id=HUGGING_FACE_LLM_ID
                )

                if not ("Model too busy" in llm_response):
                    return filter_json_output(llm_response)

            if "Model too busy" in llm_response:
                return f"Model too busy. {n_retries} retries were attempted"
            else:
                return llm_response

        else:
            st.write("please provide the hugging face api token")
    elif llm_option == LOCAL_LLM_SELECT:
        return get_json_summary_local_llm(text=text_input, llm_id=LOCAL_LLM_ID)


def get_summary(uploaded_file):

    if uploaded_file != None:
        bytes_data = uploaded_file.read()

        if uploaded_file.type in IMAGE_FILE_TYPES:

            extracted_str = get_text_from_image(bytes_data)

            llm_response = get_response_llm(
                text_input=extracted_str, llm_option=LLM_option, token=token
            )
            st.code(llm_response, language="python", wrap_lines=True)
        elif uploaded_file.type in PDF_FILE_TYPES:
            extracted_str = get_pdf_text(uploaded_file)

            llm_response = get_response_llm(
                text_input=extracted_str, llm_option=LLM_option, token=token
            )

            st.code(llm_response, language="python", wrap_lines=True)
    else:
        st.write("Please upload a file")


LLM_option = st.sidebar.radio(
    "LLM usage mode",
    key="visibility",
    options=[HUGGING_FACE_SELECT, LOCAL_LLM_SELECT],
)


uploaded_file = st.file_uploader(
    "Upload a PDF or image file",
    accept_multiple_files=False,
    type=ALLOWED_FILE_TYPES,
)

token = None
if LLM_option == HUGGING_FACE_SELECT:
    st.sidebar.info(
        "⚠️ Note: The requests for this model may get a 'Model too busy' response. Consider using locally downloaded LLMs for best results"
    )
    token = st.sidebar.text_input(
        "Enter your hugging face Personal Access token", type="password"
    )
elif LLM_option == LOCAL_LLM_SELECT and uploaded_file != None:
    if uploaded_file.type in IMAGE_FILE_TYPES:
        st.sidebar.info(
            "Note: Consider clicking 'Get Summary' until you receive satisfactory result due to the quality of the image uploaded"
        )

st.button("Get Summary", on_click=get_summary(uploaded_file=uploaded_file))
