import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Chatbot lancé (tape 'quit' pour arrêter)\n")

messages = [
    {"role": "system", "content": "Tu es un assistant utile et intelligent."}
]

while True:
    user_input = input("Toi: ")

    if user_input.lower() == "quit":
        print("Chatbot arrêté.")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"tu es un assistant pour une boutique e-commerce. tu aides avec les commandes, livraisons et retours. réponds à ce client : {user_input}"
    )
    print(response.output_text)



