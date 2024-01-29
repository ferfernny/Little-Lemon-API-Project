from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.home, name="home"),
    path('menu-item', views.menu, name="menu"),
    path('menu-items',views.MenuItems.as_view({'get':'list'}), name="menu_items"),
    path('menu-items/<int:pk>',views.SingleMenuItem.as_view(), name="menu_items_id"),
    #User group management endpoints
    path('groups/manager/users', views.Managers.as_view()),
    path('groups/manager/users/<int:pk>', views.DeleteManager.as_view()),  
    path('groups/delivery-crew/users', views.DeliveryCrew.as_view()),   
    path('groups/delivery-crew/users/<int:pk>', views.DeleteDeliveryCrew.as_view()), 
    #Cart management endpoints 
    path('cart/menu-items', views.cart.as_view(), name="cart"),    
    #Order management endpoints
    path('order', views.order, name="order"),
    path('orders', views.Orders.as_view(), name='orders'),   
    path('orders/<int:pk>', views.SingleOrder.as_view(), name='orders_id'),
]