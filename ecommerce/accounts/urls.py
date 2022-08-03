
from django.urls import  path
from  .import views

urlpatterns=[

   path("authenticate/",views.auth_view,name='login'),
   path("varify/",views.sms_varification,name='varification'),
   path("",views.userlogin,name="home"),
   path("logout/",views.log_out,name="log-out"),
   path("register/",views.register,name="registration"),
   path("register/new_uservarify/",views.varify,name='newuservarify'),
   path("men_load/<int:id>",views.category_display,name='displaymen'),
 

]

htmx_urlpatterns=[
   path("check_username/",views.username_check,name="username-check"),
   path("check_password/",views.password_check,name="password-check"),
   path("search_product/",views.main_search,name="search-product"),
   path("profile/",views.profile,name="profile"),
]
urlpatterns+=htmx_urlpatterns