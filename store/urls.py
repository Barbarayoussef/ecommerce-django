
from django.urls import path , include
from .import views

urlpatterns = [
  path('',views.home,name='home'),
  path('about/',views.about, name='about'),
  path('login/',views.login_user,name='login'),
  path('logout/',views.logout_user,name='logout'),
  path('register/',views.register_user,name='register'),
  path('update_user/',views.update_user,name='update_user'),
  path('update_info/',views.update_info,name='update_info'),
   path('update_password/',views.update_password,name='update_password'),
  path('product/<int:pk>',views.product,name='product'),
  path('add-product/', views.add_product, name='add_product'),
  path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),



]