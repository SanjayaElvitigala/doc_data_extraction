import easyocr

__all__ = ["get_text_from_image"]


def get_text_from_image(image):
    reader = easyocr.Reader(["en"], gpu=False)
    result = reader.readtext(image)
    text_extracted = []

    for element in result:
        text_extracted.append(element[1])

    extracted_str = " ".join(text_extracted)

    return extracted_str
