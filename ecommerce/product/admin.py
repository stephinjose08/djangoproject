from django.contrib import admin
from .models import *

class priceDetailsAdmin(admin.ModelAdmin):
    list_display=('actual_price','discount_price','discount_rate',)

class AddressAdmin(admin.ModelAdmin):
    list_display=('user','fist_name','last_name','addressline1','addressline2','city')
class productAdmin(admin.ModelAdmin):
    list_display=('product_name',)
class mediaAdmin(admin.ModelAdmin):
    list_display=('product',)
    
    
# Register your models here.
admin.site.register(user_address,AddressAdmin)
admin.site.register(Category)
admin.site.register(subcategory)
admin.site.register(color)
admin.site.register(product,productAdmin) 
admin.site.register(media,mediaAdmin)
admin.site.register(brand)
admin.site.register(price,priceDetailsAdmin)
admin.site.register(size)
admin.site.register(banners)