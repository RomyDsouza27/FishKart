from django.urls import path
from . import views

app_name = 'fishkart'

urlpatterns = [
    path('register/', views.CustomerRegisterView.as_view(), name='register'),
    path('', views.loginview, name='login'),
    path('resthome/', views.Fishlistlist.as_view(), name='menu_list'),
    path('past_orders/', views.PastOrderlist.as_view(), name='past_order_list'),
    path('add/', views.AddFood.as_view(), name='addfood'),
    path('update/<int:pk>/', views.UpdateFood.as_view(), name='updatefood'),
    path('delete/<int:pk>/', views.DeleteFood.as_view(), name='deletefood'),
    path('detail/<int:pk>/', views.DetailFood.as_view(), name='detail'),
    path('addcart/<int:item_id>/', views.additemview, name='add_to_cart'),
    path('home/', views.Home.as_view(), name='home'),
    path('home/detail/<int:pk>/', views.DetailFood.as_view(), name='home_detail'),
    path('mycart/', views.MyCart.as_view(), name='mycart'),
    path('<int:pk>/mycart/', views.CartDelete.as_view(), name='deletecart'),
    path('ordersummary/', views.ordersummaryview, name='ordersummary'),
    path('delhome/', views.DelHome.as_view(), name='delhome'),
    path('takeorder/<str:q>/', views.takeorderview, name='takeorder'),
    path('restordercheck/<str:q>/', views.restcheckorderview, name='checkorder'),
    path('trackorders/', views.trackordersview, name='trackorders'),
    path('successorder/', views.successorderview, name='successorder'),
    path('logout/', views.logout_request, name='logout'),
    path('finishorder/<str:q>/', views.finishorderview, name='finishorder'),
    path('orderlist/', views.order_list_restaurant, name='orderlist'),
    path('trackorders/', views.trackordersview, name='trackorders'),

]