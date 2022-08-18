from django.urls import  path
from  .import views

urlpatterns = [

  path("",views.admin_login),
  path('admin_home/',views.load_adminhome,name="admin-home"), 
  path("list_user/",views.displayUsers,name="view-user"), 
  path("list_product/",views.productlist,name="view-product"), 
   path("<int:id>/",views.add_OR_edit_Product,name="edit-product"),
  path("add_edit_product/",views.add_OR_edit_Product,name="add-product"),
  path("delete/<int:id>/",views.deletproduct,name="delete-product"),
  path("add_edit_categories/",views.add_edit_categories,name="add-categories"),
   path("edit_cat/<int:id>/",views.add_edit_categories,name="edit-categories"),
  path("add_edit_subcategories/",views.add_edit_subcategories,name="add-subcategories"),
   path("edit_subcat/<int:id>/",views.add_edit_subcategories,name="edit-subcategories"),
  path("delete_sub/<int:id>/",views.delete_subcategory,name="delete-subcategory"),
  path("delete_cat/<int:id>/",views.delete_category,name="delete-category"),
  path("block/<int:id>/",views.block_user,name="block-user"),
  path("banner_images/",views.baner_manage,name="banner-manage"),
  path("orders/",views.orders,name='orders'),
  path("list_product/get_subcategory/",views.subcategory_get,name="sub-categories"),
  path("list_product/get_subcategory/sort_by_category/",views.sort_by_category,name="sort-by-categories"),
  path("list_product/",views.display_all,name="display-all"),
  path("orders/order_details/<int:id>/",views.order_detail,name="order-details"),
  path("delete_order/<int:id>/",views.delete_order,name="delete-order"),
  path("update_status/<int:pid>/",views.order_status_change,name="order-status"),
  path("admin_home/coupons/",views.couponadd,name="coupon-add"),
  path("admin_home/brands/",views.brands,name="brands"),
  path("admin_home/brands/<int:id>/",views.brands,name="edit-brand"),
  path("admin_home/delete_brand/<int:id>/",views.delete_brand,name="delete-brand"),
  path("admin_home/coupons_edit/<int:id>",views.couponadd,name="coupon-edit"),
  path("admin_home/category_offer/",views.category_offer,name="category-offer"),
  path("admin_home/category_offer/<int:id>",views.category_offer,name="category-offer-edit"),
  path("admin_home/category_offer_delete/<int:id>",views.delete_category_offer,name="category-offer-delete"),

]

htmx_urlpatterns=[
   path("check_username/",views.username_check,name="username-check"),
   path("check_password/",views.password_check,name="password-check"),

]
urlpatterns+=htmx_urlpatterns
