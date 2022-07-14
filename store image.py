import requests

with open("/workspace/plant-encyclopedia/token_acc", 'r') as f:
    acc_token = f.read()
api_url = "https://graph.facebook.com/v14.0/me/messages"

url = input()
payload = {
    "recipient": {
        "id": "5493410604036377"
    },
    "message": {
        "attachment": {
            "type": "image",
            "payload": {
                "url": url,
                "is_reusable": True
            }
        }
    }
}
auth = {
        'access_token': acc_token
    }
response = requests.post(
        api_url,
        params=auth,
        json=payload
    )
print(response.text)