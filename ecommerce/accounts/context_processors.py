from cart.models import cartItem
from.models import CustomUser
def get_cartItems(request):
    if request.user.is_authenticated:
        cartitems=cartItem.objects.filter(useID=request.user)
        user=CustomUser.objects.get(phone=request.user)
        name=user.first_name[0]



        return{'cartitems':cartitems,'name':name}
    else:
        return{}