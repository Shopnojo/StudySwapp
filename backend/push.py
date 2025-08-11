import requests

def send_push(token: str, title: str, body: str):
    headers = {
        "Authorization": "key=YOUR_FCM_SERVER_KEY",
        "Content-Type": "application/json",
    }
    payload = {
        "to": token,
        "notification": {"title": title, "body": body},
    }
    res = requests.post("https://fcm.googleapis.com/fcm/send", json=payload, headers=headers)
    return res.json()
