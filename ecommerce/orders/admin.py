from django.contrib import admin

from orders.models import order, orderproduct, payment

# Register your models here.
admin.site.register(order)
admin.site.register(orderproduct)
admin.site.register(payment)
