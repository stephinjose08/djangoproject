from django.db import models
from accounts.models import CustomUser
from product.models import product
# Create your models here.

class payment(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_mode=(
        ("COD","COD"),
        ("Razorpay","Razorpay"),
        ("paypal","paypal")
    )
    payment_mode=models.CharField(max_length=100,choices=payment_mode)
    amount_paid=models.CharField(max_length=50)
    status=models.CharField(max_length=100)





class order(models.Model):
    user=models.ForeignKey(CustomUser ,on_delete=models.CASCADE)
    order_for_others=models.BooleanField(default=False)
    fist_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    addressline1=models.CharField(max_length=200)
    addressline2=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100 ,null=True)
    country=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=8)
    total_price=models.CharField(max_length=100)
    payment_mode=models.ForeignKey(payment, on_delete=models.CASCADE)
    order_status=(
       ( "pending","pending"),
       ("out  for  shipping","out or shipping"),
       ("completed","completed"),
       ("canceled","canceled"),

       


    )
    status=models.CharField(max_length=50,  choices=order_status,default='pending')
    notes=models.TextField(default='avoid plastic cover',null=True)
    tracking_number=models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
class orderproduct(models.Model):
    order=models.ForeignKey(order, on_delete=models.CASCADE)
    payment=models.ForeignKey(payment, on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    price=models.FloatField(null=True)
    quantity=models.IntegerField(null=True)  