from django.contrib import admin
from .models import Payment,  PaymentItem

class  PaymentItemInline(admin.TabularInline):
    model = PaymentItem
    raw_id_fields = ['product']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'amount', 'city', 'ref','paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [PaymentItemInline]