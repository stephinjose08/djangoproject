from django.urls import  path
from  .import views

urlpatterns = [

#   path("",views.grid_view,name="grid-view"),  
path('check_out/',views.check_out,name="check-out"),
path('check_out/<int:id>/',views.check_out,name="buy-now"),
path('place_order/',views.placeorder,name="place-order"),
path('check_out/proced-to-pay/',views.proced_to_pay,name="procedtopay"),
path('check_out/online/',views.online,name="online"),
path('check_out/my_orders/',views.my_orders,name="my-order"),
path('check_out/<int:id>/my_orders/',views.my_orders,name="my-order"),
path('my_orders/order_detail/<int:id>/',views.order_details,name="detail-order"),
path('track/<str:track>/',views.trackorder,name="track"),
path('cancel_order/<str:rack>/',views.cancel_order,name="cancel-order"),
path('check_out/coupen_offer/',views.coupenoffer,name='coupon-offer'),
path('check_out/invoice/<int:id>/',views.invoice,name="invoice"),
#path('check_out/invoice/dounload/',views.export_invoice_pdf,name="dounload-pdf"),
path('return/<str:rack>/',views.return_order,name="returned-order"),


] 