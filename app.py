from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
from rag import create_rag_chain, ask_question
import os

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

rag_chain = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global rag_chain
    file = request.files["file"]
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)
    rag_chain = create_rag_chain(file_path)
    return jsonify({"message": "Document chargé avec succès !"})


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    if rag_chain:
        reply = ask_question(user_input)
    else:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant e-commerce."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)