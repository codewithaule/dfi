from django.db import models
import secrets
from shop.models import Product
from .paystack import PayStack

class Payment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    verified =models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref= ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save( *args, **kwargs)

    def amount_value(self ) -> int:
        return self.amount *100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] /100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
                return True
        return False



class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
