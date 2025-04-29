from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from django.urls import reverse
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Payment
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Process the payment here
        # For now, we'll just mark the order as paid
        order.paid = True
        order.save()
        return redirect('payments:done')
    
    return render(request, 'payments/process.html', {
        'order': order,
        'client_id': settings.PAYPAL_CLIENT_ID
    })

def payment_done(request):
    return render(request, 'payments/done.html')

def payment_canceled(request):
    return render(request, 'payments/canceled.html')

@require_POST
@csrf_exempt
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),  # Convert to cents
            currency='usd',
            metadata={'order_id': order.id}
        )
        
        # Create a payment record
        Payment.objects.create(
            order=order,
            stripe_payment_intent=intent.id,
            amount=order.total_amount,
            status='pending'
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

@require_POST
@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment = Payment.objects.get(stripe_payment_intent=payment_intent['id'])
        payment.status = 'completed'
        payment.save()
        
        # Update order status
        order = payment.order
        order.status = 'paid'
        order.save()

    return JsonResponse({'status': 'success'})
