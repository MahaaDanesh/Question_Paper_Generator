import fitz
import os


# ==========================================
# Read One PDF
# ==========================================

def read_pdf(pdf_path):

    text = ""

    try:

        document = fitz.open(pdf_path)

        for page in document:

            text += page.get_text()

        document.close()

    except Exception as e:

        print("Error:", e)

    return text


# ==========================================
# Read All Previous Papers
# ==========================================

def read_previous_papers(folder_path):

    all_text = ""

    if not os.path.exists(folder_path):

        return all_text


    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            pdf = os.path.join(folder_path, file)

            all_text += "\n\n"

            all_text += "=================================\n"

            all_text += file

            all_text += "\n"

            all_text += "=================================\n"

            all_text += read_pdf(pdf)


    return all_text