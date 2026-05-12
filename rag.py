from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from pypdf import PdfReader
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

document_text = ""


def load_pdf(file_path):
    global document_text
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    document_text = text[:4000]
    return document_text


def create_rag_chain(file_path):
    load_pdf(file_path)
    return True


def ask_question(question):
    global document_text
    if not document_text:
        return None

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system",
             "content": f"Tu es un assistant. Réponds uniquement basé sur ce document:\n\n{document_text}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content