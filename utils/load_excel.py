import pandas as pd
from langchain_core.documents import Document


def load_excel_with_metadata(file_path):

    xls = pd.ExcelFile(file_path)

    docs = []

    for sheet in xls.sheet_names:

        df = pd.read_excel(file_path, sheet_name=sheet)

        df = df.dropna(how="all")

        for _, row in df.iterrows():

            text = "\n".join(
                [f"{col}: {row[col]}" for col in df.columns if str(row[col]) != "nan"]
            )

            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "department": sheet,
                        "sheet": sheet,
                        "source_file": file_path
                    }
                )
            )

    return docs