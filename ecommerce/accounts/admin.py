from django.contrib import admin
from . models import CustomUser,code

class customuserAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email','phone')


# Register your models here.
admin.site.register(CustomUser,customuserAdmin)
admin.site.register(code)
