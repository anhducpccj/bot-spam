from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "123456")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "your_token_here")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token"
    elif request.method == 'POST':
        data = request.json
        for entry in data.get("entry", []):
            for msg_event in entry.get("messaging", []):
                sender = msg_event["sender"]["id"]
                if "message" in msg_event:
                    text = msg_event["message"].get("text", "")
                    reply(sender, f"Bạn nói: {text}")
        return "ok"

def reply(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
