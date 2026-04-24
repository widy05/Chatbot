from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Tu es un assistant e-commerce."},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response.choices[0].message.content
    print (reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)