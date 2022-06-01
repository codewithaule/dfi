from django import forms 

from.models import Payment



class PaymentForm(forms.ModelForm):
    class Meta: 
        model = Payment
        fields = ('first_name', 'last_name', 'email', 'address', 'city','amount', )