from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "test@test@1234"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    if request.method == "POST":
        data = request.json
        print("Webhook received:", data)
        return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
