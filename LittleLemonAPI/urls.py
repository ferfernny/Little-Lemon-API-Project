from django.urls import include, path
from . import views
from .views import cart_views, menu_views, manage_user_views, order_views, base_views

urlpatterns = [
    path('', base_views.home, name="home"),
    path('menu-item/', menu_views.menu, name="menu"),
    path('menu-items/',menu_views.MenuItems.as_view({'get':'list'}), name="menu_items"),
    path('menu-items/<int:pk>/',menu_views.SingleMenuItem.as_view(), name="menu_items_id"),
    #User group management endpoints
    path('groups/manager/views', manage_user_views.manager, name='manager_view'),
    path('groups/manager/users/', manage_user_views.Managers.as_view(), name='users_manager'),
    path('groups/manager/users/<int:pk>/', manage_user_views.DeleteManager.as_view(), name="userid_manager"),  
    path('groups/delivery-crew/users/', manage_user_views.DeliveryCrew.as_view(), name='users_delivery_crew'),   
    path('groups/delivery-crew/users/<int:pk>/', manage_user_views.DeleteDeliveryCrew.as_view(), name="userid_delivery_crew"), 
    #Cart management endpoints 
    path('cart/menu-items', cart_views.cart.as_view(), name="cart"),    
    #Order management endpoints
    path('order/', order_views.order, name="order"),
    path('orders/', order_views.Orders.as_view(), name='orders'),   
    path('orders/<int:pk>/', order_views.SingleOrder.as_view(), name='orders_id'),
]