import os
from pypdf import PdfReader

def load_pdfs_from_uploads(uploaded_files):
    """
    Reads PDFs directly from Streamlit's uploaded file objects (no folder needed).
    """
    all_text = {}

    for uploaded_file in uploaded_files:
        reader = PdfReader(uploaded_file)

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        all_text[uploaded_file.name] = text

    return all_text

def load_Pdf(data_folder = "data"):
    all_text = {}

    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(data_folder,filename)
            reader = PdfReader(filepath)

            text = ""
            for page in reader.pages:
                text+=page.extract_text()
            all_text[filename]=text
            print(f"✅ Loaded {filename} — {len(text)} characters")
    return all_text

if __name__=="__main__":
    documents = load_Pdf()
    print(f"\nTotal documents loaded: {len(documents)}")
    for filename, text in documents.items():
        print(f"preview of {filename}")
        print(text[:500])
        print("....theres more ofc....")