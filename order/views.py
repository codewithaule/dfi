from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.contrib import messages
from cart.cart import Cart
from .forms import PaymentForm
from django.conf import settings
from .models import Payment, PaymentItem

# Create your views here.


def initiate_payment(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            for item in cart:
                PaymentItem.objects.create(payment=payment, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request,'order/make_payment.html',{'payment':payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

    else:
        form = PaymentForm()
    return  render(request,'order/initiate_payment.html', {'cart': cart, 'form':form})

def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification Successfull")
    else:
        messages.error(request, "Verification Failed.")
    return render(request,'shop/product/list.html')
