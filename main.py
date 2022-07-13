from flask import Flask, request
import requests

app = Flask(__name__)
api_url = "https://graph.facebook.com/v14.0/me/messages"
v_token = "bipaktfmpea"
acc_token = "EAAGf9UtML2gBAJFrfidEGGL37xJiegdiIzsgKRZAZCY5PwQPxZAO6T5KkK7ZANkCpk5a9FZCUS9GKyX4r3yyXy6zXLGAuzcqhafRhcyF1Fpcj1yKsPu4fC1v4GtJcFSQSngegAZB6chXEenDyBICdKIrg14Cg58yhnyssn7Ajee9q1t22ZAg1EU"


def get_bot_response(sender, message):
    if message == "야":
        return "네"


def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular',
        'messaging_type': 'MESSAGE_TAG',
        "tag": "CONFIRMED_EVENT_UPDATE"
    }

    auth = {
        'access_token': acc_token
    }

    response = requests.post(
        api_url,
        params=auth,
        json=payload
    )
    return response.json()


def verify_webhook(req):
    if req.args.get("hub.verify_token") == v_token:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def respond(sender, message):  # 대답하는코드
    response = get_bot_response(sender, message)
    print(response)
    payload = {
        'message': {
            'text': response
        },
        'recipient': {
            'id': sender
        },
        'notification_type': 'regular',
        'messaging_type': 'RESPONSE',
    }

    auth = {
        'access_token': acc_token
    }

    response = requests.post(
        api_url,
        params=auth,
        json=payload
    )
    return response.json()


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook", methods=['GET'])
def listen():
    """This is the main function flask uses to
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)


@app.route("/webhook", methods=['POST'])
def talk():
    payload = request.get_json()
    event = payload['entry'][0]['messaging']
    for x in event:
        if is_user_message(x):
            print("yee")
            text = x['message']['text']
            print(text)
            sender_id = x['sender']['id']
            print(sender_id)
            print(respond(sender_id, text))

    return "ok"


@app.route('/')
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=80)
