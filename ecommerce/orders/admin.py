from django.contrib import admin


from orders.models import order, orderproduct, payment,canceled_orders,returned_orders

# Register your models here.
admin.site.register(order)
admin.site.register(orderproduct)
admin.site.register(payment)
admin.site.register(canceled_orders)
admin.site.register(returned_orders)