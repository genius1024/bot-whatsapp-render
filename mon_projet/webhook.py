from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "7d2ad5c4cdd9dd9af7bed7a98f850590"  # Le même que celui dans Meta

@app.route('/webhook', methods=['GET'])
def verify():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return challenge  # Meta attend cette réponse
    return "Invalid verification token", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Message reçu :", data)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
