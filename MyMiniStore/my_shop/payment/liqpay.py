import base64
import json
import hashlib

def liqpay_data(public_key, order_id, amount, callback_url):
    data = {
        "public_key": public_key,
        "version": "3",
        "action": "pay",
        "amount": str(amount),
        "currency": "UAH",
        "description": f"Order #{order_id}",
        "order_id": str(order_id),
        "server_url": callback_url,
        "result_url": callback_url,
    }

    json_data = json.dumps(data)
    encoded_data = base64.b64encode(json_data.encode()).decode()
    return encoded_data


def liqpay_signature(private_key, data):
    sign_string = private_key + data + private_key
    return base64.b64encode(
        hashlib.sha1(sign_string.encode()).digest()
    ).decode()
