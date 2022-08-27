from django.urls import  path
from  .import views

urlpatterns = [

  path("grid_view/<int:bid>/",views.grid_view,name="grid-view"),  
  path("<str:brandname>/",views.brandwise,name="brandwise"),  
  path("category/<int:id>",views.categorywise,name="categorywise"),
  path("single_item/<int:id>",views.detail_view,name="detail-view-product"),
  path("grid_view/<int:bid>/search_item/",views.searchgrid,name="search-items"),
  # path("grid_view/<int:bid>/size_sort/<str:size>/",views.size_sort,name="size-sort"),
  
]