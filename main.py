from flask import Flask, request
import requests

app = Flask(__name__)
api_url = "https://graph.facebook.com/v14.0/me/messages"
v_token = "bipaktfmpea"
with open("/workspace/plant-encyclopedia/token_acc", 'r') as f:
    acc_token = f.read()

session = {}


def get_bot_response(sender, message):
    global session
    if message == "시작하기":
        session[sender] = {"session": 1, "color": None}
        return "꽃 색은 무슨색입니까? (흰색, 분홍색, 녹색, 주황색, 보라색, 노란색, 갈색 중 택 1)"
    elif sender not in session:
        return "시작하기라고 입력해주세요"
    elif session[sender]["session"] == 1 and session[sender]["color"] is None:
        if "흰색" in message:
            session[sender]["color"] = 1
            return "꽃이 핀 형태는 어떠한가요? (무리, 일렬)"
        elif "분홍색" in message:
            session[sender]["color"] = 2
        elif "녹색" in message:
            session[sender]["color"] = 3
        elif "주황색" in message:
            session[sender]["color"] = 4
            session[sender] = {"session": None, "color": None}
            return "그 꽃은 인도 칸나입니다."
        elif "보라색" in message:
            session[sender]["color"] = 5
            session[sender] = {"session": None, "color": None}
            return "그 꽃은 순비기나무입니다."
        elif "노란색" in message:
            session[sender]["color"] = 6
            session[sender] = {"session": None, "color": None}
            return "그 꽃은 인동덩굴입니다."
        elif "갈색" in message:
            session[sender]["color"] = 7
            session[sender] = {"session": None, "color": None}
            return "그 꽃은 밀사초입니다."
        else:
            return "저 중에 다시 선택해 주세요"
        return "잎 모양은 어떠한가요? (물방울, 단풍, 길쭉함, 가늘고 길쭉 중 택 1)"

    elif session[sender]["session"] == 1 and session[sender]["color"] is not None:
        session[sender] = {"session": None, "color": None}
        if session[sender]["color"] == 1 and ("무리" in message):
            return "그 꽃은 사상자입니다."
        elif session[sender]["color"] == 1 and ("일렬" in message):
            return "그 꽃은 참새피입니다."
        elif session[sender]["color"] == 2 and ("물방울" in message):
            return "그 꽃은 분꽃입니다."
        elif session[sender]["color"] == 2 and ("길쭉함" in message):
            return "그 꽃은 엉겅퀴입니다."
        elif session[sender]["color"] == 3 and ("단풍" in message):
            return "그 꽃은 환삼덩굴입니다."
        elif session[sender]["color"] == 3 and ("가늘고 길쭉" in message):
            return "그 꽃은 가는갯는쟁이입니다."


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
