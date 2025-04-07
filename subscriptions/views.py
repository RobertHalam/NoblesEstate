from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import redirect
from paypal_utils import paypalrestsdk
from django.http import JsonResponse
from django.urls import reverse
from paypalrestsdk import Payment # type: ignore

def create_subscription(request, plan_name):
    # Define your subscription plans
    plans = {
        "Basic": {"price": "10.00", "description": "Basic Plan"},
        "Professional": {"price": "30.00", "description": "Professional Plan"},
        "Realtor": {"price": "50.00", "description": "Realtor Plan"},
    }

    if plan_name not in plans:
        return JsonResponse({"error": "Invalid plan name"}, status=400)

    selected_plan = plans[plan_name]

    # Create a payment object
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment_success')),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancel')),
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": plan_name,
                    "sku": plan_name,
                    "price": selected_plan["price"],
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": selected_plan["price"],
                "currency": "USD"
            },
            "description": selected_plan["description"]
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return JsonResponse({"error": "Payment creation failed", "details": payment.error}, status=500)


def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        return JsonResponse({"error": "Invalid response from PayPal"}, status=400)

    payment = Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Simulate storing subscription data
        plan_name = payment.transactions[0].item_list.items[0].name
        print(f"Payment successful for plan: {plan_name}")  # For testing purposes

        # Redirect to dashboard
        return redirect('dashboard')
    else:
        return JsonResponse({"error": "Payment execution failed", "details": payment.error}, status=500)

def payment_cancel(request):
    return render(request, 'subscriptions/payment_cancel.html')

def dashboard(request):
    return render(request, 'subscriptions/dashboard.html', {"subscription_plan": "Basic"})  # Static for testing purposes




def myview(request):
    if request.method == "POST":
        button_value = request.POST.get("button_value")
        if button_value == "Basic":
            return redirect('/subscriptions/subscribe/Basic')
        elif button_value == "Prof":
            return redirect('/subscriptions/subscribe/Professional')
        elif button_value == "Real":
            return redirect('/subscriptions/subscribe/Realtor')
        
    return render(request, 'subscriptions/t.html', {"subscription_plan": "Basic"})

