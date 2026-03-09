import base64
import hashlib
import json
import uuid
from django.conf import settings


def generate_liqpay_data(order):
    public_key = settings.LIQPAY_PUBLIC_KEY
    private_key = settings.LIQPAY_PRIVATE_KEY

    liqpay_order_id = f"{order.id}-{uuid.uuid4()}"

    params = {
        "public_key": public_key,
        "version": "3",
        "action": "pay",
        "amount": str(order.get_total_cost),
        "currency": "UAH",
        "description": f"Оплата замовлення №{order.id}",
        "order_id": liqpay_order_id,
        "result_url": f"http://127.0.0.1:8000/payment/success/{order.id}",
        "server_url": "http://127.0.0.1:8000/payment/liqpay/callback/",
    }

    json_data = json.dumps(params)
    data = base64.b64encode(json_data.encode()).decode()

    sign_string = private_key + data + private_key
    signature = base64.b64encode(
        hashlib.sha1(sign_string.encode()).digest()
    ).decode()

    return data, signature, liqpay_order_id


def verify_liqpay_signature(data, signature):
    private_key = settings.LIQPAY_PRIVATE_KEY
    sign_string = private_key + data + private_key
    expected_signature = base64.b64encode(
        hashlib.sha1(sign_string.encode()).digest()
    ).decode()
    return signature == expected_signature
