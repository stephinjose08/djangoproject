from django.urls import  path
from  .import views

urlpatterns = [

  path("grid_view/<int:bid>/",views.grid_view,name="grid-view"),  
  path("<str:brandname>/",views.brandwise,name="brandwise"),  
  path("single_item/<int:id>",views.detail_view,name="detail-view-product"),
  path("grid_view/<int:bid>/search_item/",views.searchgrid,name="search-items"),
  
]