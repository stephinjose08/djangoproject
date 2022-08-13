
from django.urls import  path
from  .import views

urlpatterns=[

path("add_cart/<int:product_id>/",views.add_cart,name='add-cart'),
path("remove_cart/<int:product_id>/",views.remove_cart,name='remove-cart'),
path("cart_items/",views.cart_items,name='cart-items'),
path("remove_cartitem/<int:product_id>/",views.remove_cartitem,name='remove-cart-item'), 
path("add_cartitem/<int:product_id>/",views.add_product,name='add-cart-item'), 
path("wishlist/",views.wishlist_page,name='wishlist'),
path("wishlist_add/<int:id>/",views.add_to_wishlist,name='wishlist-add'),
path("wishlist_remove/<int:id>/",views.remove_from_wishlist,name='wishlist-remove'),

]