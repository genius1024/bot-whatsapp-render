from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Récupérer les variables d'environnement
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN_META")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.route("/", methods=["GET"])
def verify_webhook():
    """ Vérifier le webhook avec le token """
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return challenge
    return "Token invalide", 403

@app.route("/", methods=["POST"])
def receive_message():
    """ Recevoir et traiter les messages WhatsApp """
    data = request.get_json()
    print("Données reçues :", data)  # Pour debug

    if "entry" in data and "changes" in data["entry"][0]:
        message = data["entry"][0]["changes"][0]["value"]
        if "messages" in message:
            sender = message["messages"][0]["from"]
            text = message["messages"][0]["text"]["body"]

            # Répondre à l'utilisateur
            send_message(sender, f"Tu as dit : {text}")
    
    return "OK", 200

def send_message(to, text):
    """ Fonction pour envoyer un message WhatsApp """
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
