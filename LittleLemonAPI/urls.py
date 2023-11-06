from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items',views.MenuItems.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItem.as_view()),
    #User group management endpoints
    path('groups/manager/users', views.Managers.as_view()),
    path('groups/manager/users/<int:pk>', views.DeleteManager.as_view()),  
    path('groups/delivery-crew/users', views.DeliveryCrew.as_view()),   
    path('groups/delivery-crew/users/<int:pk>', views.DeleteDeliveryCrew.as_view()), 
    #Cart management endpoints 
    path('cart/menu-items', views.cart.as_view()),    
    #Order management endpoints
    path('orders', views.Orders.as_view()),   
    path('orders/<int:pk>', views.SingleOrder.as_view()),  
]