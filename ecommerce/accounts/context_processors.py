from cart.models import cartItem
from.models import CustomUser
def get_cartItems(request):
    if request.user.is_authenticated:
        cartitems=cartItem.objects.filter(useID=request.user)
        

        return{'cartitems':cartitems}
    else:
        return{}