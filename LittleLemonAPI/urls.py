from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path('menu-items',views.menu_items),
    path('menu-items/<int:id>',views.singlemenu_item),
    #User group management endpoints
    path('groups/manager/users', views.managers),
    #path('groups/manager/users/{userId}', views.managers),  #need to re-write
    #path('groups/delivery-crew/users', views.managers),    #need to re-write
    #path('groups/delivery-crew/users/{userId}', views.managers),   #need to re-write
    #Cart management endpoints 
    #path('cart/menu-items', views.managers),    #need to re-write
    #Order management endpoints
    #path('orders', views.menu_items),   #need to re-write
    #path('orders/{orderId}', views.menu_items),   #need to re-write
]