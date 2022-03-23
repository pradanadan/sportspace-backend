import locale
import requests

locale.setlocale(locale.LC_ALL, '')

def send_notif_admin(price):
    url = 'https://fcm.googleapis.com/fcm/send'
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAE2STLnU:APA91bEYLnJd7UWL1tRG7gpyXg4oW4W6V8R2BTp91uMQfavWfM8hiYU-uC3LCDarxKw_-WmcSWEppg5rUWqyLvAqa41CEkrFf9crn2NwVNRYM8AxUqggFDAxXColYnODz5ZnZygEMvqC'
    }

    price = currency(price)

    body = "Kode unik pembayaran: " + price

    data = {
        "to": "eAVyAqJCQmKn6w4QFSfRm2:APA91bGYoHrhvvlNQr4B7grEO3dRiZTlXF9RQF-aaS5o4E77Ky6ohhMNORY8sdnyiZy4-amrPF8GcoQfudpBgWrbFgoW2vBX-1m9LLBccKkMA6bOgpH46RZGU39b9hfCyK-jyVxu2ua0",
        "notification": {
            "title": "Ada Pesanan Baru!",
            "body": body,
            "mutable_content": True,
            "sound": "Tri-tone"
        },
        "priority": "high"
        }

    req = requests.post(url, json=data, headers=header)

    return req.text

def currency(value):
    return 'Rp ' + f'{value:n}'