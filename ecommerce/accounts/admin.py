from django.contrib import admin
from . models import CustomUser,code,user_address2

class customuserAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email','phone')
class user_sddress2Admin(admin.ModelAdmin):
    list_display=('fist_name','last_name')


# Register your models here.
admin.site.register(CustomUser,customuserAdmin)
admin.site.register(code)
admin.site.register(user_address2,user_sddress2Admin)