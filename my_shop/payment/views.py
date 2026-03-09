import base64
import json
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from card.models import Order
from payment.models import Payment
from payment.utils import generate_liqpay_data, verify_liqpay_signature



# def payment_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id)

#     data, signature, liqpay_order_id = generate_liqpay_data(order)

#     order.liqpay_order_id = liqpay_order_id
#     order.save(update_fields=["liqpay_order_id"])

#     return render(request, 'stors/payment.html', {
#         'order': order,
#         'data': data,
#         'signature': signature
#     })
# def payment_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id)

#     liqpay_data, liqpay_signature, liqpay_order_id = generate_liqpay_data(order)

#     payment = Payment.objects.create(
#         order=order,
#         liqpay_order_id=liqpay_order_id,
#         amount=order.get_total_cost,  
#         liqpay_data=liqpay_data,
#         liqpay_signature=liqpay_signature,
#     )

#     return render(request, 'stors/payment.html', {
#         'order': order,
#         'liqpay_data': liqpay_data,
#         'liqpay_signature': liqpay_signature,
#     })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_liqpay_data(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    data, signature, liqpay_order_id = generate_liqpay_data(order)

    Payment.objects.create(
        order=order,
        liqpay_order_id=liqpay_order_id,
        amount=order.get_total_cost,
        liqpay_data=data,
        liqpay_signature=signature
    )

    return Response({
        "data": data,
        "signature": signature
    })


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def liqpay_callback(request):
    data = request.data.get('data')
    signature = request.data.get('signature')

    if not verify_liqpay_signature(data, signature):
        return Response({"error": "Invalid signature"}, status=400)

    payload = json.loads(base64.b64decode(data).decode())

    liqpay_order_id = payload.get('order_id')
    status = payload.get('status')

    payment = get_object_or_404(Payment, liqpay_order_id=liqpay_order_id)

    payment.status = status
    payment.liqpay_response = payload
    payment.save()

    if status in ('success', 'sandbox'):
        payment.order.status = 'paid'
    else:
        payment.order.status = 'failed'

    payment.order.save()

    return Response({"status": "ok"})
