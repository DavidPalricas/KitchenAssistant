from flask import Flask, render_template,request, jsonify
import requests

app = Flask(__name__)

RASA_API = "http://localhost:5005/webhooks/rest/webhook" # Url da API do Rasa



@app.route("/")
def index():
    return  render_template("index.html")

@app.route("/webhook", methods=["POST"])

def webhook(): 
    user_message = request.json["message"]
    print(f"Messangem do usuário: {user_message}")

    response = requests.post(RASA_API, json={"message": user_message})
    response = response.json()
    print(f"Resposta do Rasa: {response}")
    
    rasa_response = ""
    for r in response:
        rasa_response += r["text"] + "\n\n\n" #Caso a mensagem tenha mais de uma linha


    return jsonify({"response": rasa_response})


if __name__ == "__main__":
    app.run(debug=True) # Para mostrar os erros no browser


