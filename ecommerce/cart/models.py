from product.models import product
from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Cart(models.Model):
    cart_ID=models.CharField(max_length=100)
    date=models.DateField( auto_now_add=True)

class cartItem(models.Model):
    useID=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    Product=models.ForeignKey(product, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()


class wishlist(models.Model):
    wishlist_items=models.ForeignKey(product,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    