import os
from utils.load_excel import load_excel_with_metadata
from utils.load_pdf import load_pdf
from utils.load_docx import load_docx


def load_all_documents():

    docs = []

    folder = "data/uploads"

    os.makedirs(folder, exist_ok=True)

    for file in os.listdir(folder):

        path = os.path.join(folder,file)

        if file.endswith(".xlsx") or file.endswith(".csv"):
            docs.extend(load_excel_with_metadata(path))

        elif file.endswith(".pdf"):
            docs.extend(load_pdf(path))

        elif file.endswith(".docx"):
            docs.extend(load_docx(path))

    return docs