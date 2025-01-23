from rest_framework.response import Response
from ..models import Cart, Order, OrderItem
from ..serializers import OrderSerializer, OrderItemSerializer, OrderStatusSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from ..business_logic.permission_business_logic import permission_business_logic
from ..business_logic.http_status_code_business_logic import http_status_code_business_logic

def order(request: HttpRequest) -> HttpResponse:
    order_data = Order.objects.all()
    main_data = {"order":order_data}
    return render(request, 'order.html', main_data)

class Orders(APIView): 
    serializer_class = OrderSerializer
    def get(self, request, *args, **kwargs):
        user = request.user
        if permission_business_logic.has_permission(user, ['Manager', 'Delivery crew']):
            if user.groups.filter(name='Delivery crew').exists():
                orders = Order.objects.filter(delivery_crew=request.user)
            elif user.groups.filter(name='Manager').exists():
                orders = Order.objects.all()
            data = {}
            for order_user in orders:
                if str(order_user.user) not in data:
                    order_items = OrderItem.objects.filter(order=order_user.user)
                    if user.groups.filter(name='Manager').exists():
                        orders = Order.objects.filter(user=order_user.user.id)
                    order_serializer = OrderSerializer(orders, many=True)
                    order_item_serializer = OrderItemSerializer(order_items, many=True)
                    data[str(order_user.user)] = {
                        'Order' : order_serializer.data,
                        'OrderItem': order_item_serializer.data
                    }
        elif permission_business_logic.customer_permission(user):
            orders = Order.objects.filter(user=request.user)
            order_items = OrderItem.objects.filter(order=request.user)
            order_serializer = OrderSerializer(orders, many=True)
            order_item_serializer = OrderItemSerializer(order_items, many=True)
            data = {
                'Order' : order_serializer.data,
                'OrderItem': order_item_serializer.data
            }
            if len(order_item_serializer.data) == 0:
                return http_status_code_business_logic.status_404_not_found('Please use POST method to move cart item to order item')
        else:
            return http_status_code_business_logic.status_403_forbidden('This user has unauthorized access.')
            
        return Response(data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        if not request.user.groups.exists():
            user = self.request.user
            CartItem = Cart.objects.filter(user=user)
            if not CartItem:
                return http_status_code_business_logic.status_400_bad_request('No cart items found for this user.')
            for item in CartItem:
                OrderItemData = {
                    'order': user,
                    'menuitem': item.menuitem,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'price': item.price
                }
                order_item = OrderItem.objects.create(**OrderItemData)
            CartItem.delete()
            serialized_item = OrderSerializer(data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()  
                return http_status_code_business_logic.status_201_created('Order and Order items created and cart items are deleted successfully.')
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
             

class SingleOrder(generics.RetrieveUpdateDestroyAPIView):  
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    def get(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('pk')
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return http_status_code_business_logic.status_404_not_found('Order does not exist.')
        if permission_business_logic.customer_permission(request.user):
            order_id = kwargs.get('pk')
            user = self.request.user
            if Order.objects.filter(user=user, pk=order_id).exists():
                order = Order.objects.get(pk=order_id)
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            return http_status_code_business_logic.status_403_forbidden("This order ID doesn't belong to the current user.")
        elif permission_business_logic.has_permission(request.user, ['Manager']):
            order_id = kwargs.get('pk')
            order = Order.objects.get(pk=order_id)
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        elif permission_business_logic.has_permission(request.user, ['Delivery crew']): 
            order_id = kwargs.get('pk')
            user = self.request.user
            if Order.objects.filter(delivery_crew=user, pk=order_id).exists():
                order = Order.objects.get(pk=order_id)
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            return http_status_code_business_logic.status_403_forbidden("This order ID doesn't assigned to this Delivery crew userid.")
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access.')
    def delete(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            order_id = kwargs.get('pk')
            order = Order.objects.get(pk=order_id)
            order.delete()
            return http_status_code_business_logic.status_200_ok('Delete this user successfully.')
        return http_status_code_business_logic.status_403_forbidden('Only Manager group can delete the order.')
    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() or not request.user.groups.exists():
            item = self.get_object()
            serializer_item = OrderSerializer(item, data=request.data)
            if serializer_item.is_valid():
                serializer_item.save()
                return Response(serializer_item.data, status=status.HTTP_200_OK)
            return Response(serializer_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return http_status_code_business_logic.status_403_forbidden('Only Manager and customer group can update the entire table of order.')
    def patch(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Delivery crew']):
            try:
                order_id = kwargs.get('pk')
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return http_status_code_business_logic.status_404_not_found('Order does not exist.')
            serializer = OrderStatusSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)