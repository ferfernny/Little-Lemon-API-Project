from django.shortcuts import render
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer
from .serializers import OrderSerializer, OrderItemSerializer
from .serializers import GroupSerializer, UserSerializer
from .serializers import OrderStatusSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets 
    
class MenuItems(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get(self, request, *args, **kwargs):
        if ( 
            request.user.groups.filter(name='Delivery crew').exists() or
            request.user.groups.filter(name='Manager').exists() or
            not request.user.groups.exists()
        ):
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message':'This user has unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerializer(data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()  
                return Response({'Message':'This menu-item has been created'}, status=status.HTTP_201_CREATED)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Message':'This user has unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
            
            
class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get(self, request, *args, **kwargs):
        if ( 
            request.user.groups.filter(name='Delivery crew').exists() or
            request.user.groups.filter(name='Manager').exists() or
            not request.user.groups.exists()
        ):
            response = super().get(request, *args, **kwargs)
            response.status_code = status.HTTP_200_OK
            return response
    def update(self, request, *args, **kwargs):
        item = self.get_object()
        if request.user.groups.filter(name='Manager').exists():
            serializer_item = MenuItemSerializer(item, data=request.data)
            if serializer_item.is_valid():
                serializer_item.save()
                return Response(serializer_item.data, status=status.HTTP_200_OK)
            return Response(serializer_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Message':'This user has unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        if request.user.groups.filter(name='Manager').exists():
            item.delete()
            return Response({'Message':'The menu-items has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'Message':'This user has unauthorized access'}, status=status.HTTP_403_FORBIDDEN)


class Managers(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        ManagerGroup = Group.objects.get(name='Manager')
        ManagerUser = ManagerGroup.user_set.all()
        if request.user.groups.filter(name='Manager').exists():
            return Response({'Manager users': [user.username for user in ManagerUser]}, status=status.HTTP_200_OK)
        return Response({'Message':'This user group has unauthorized access'})
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            username = request.data.get('username')
            if username == '':
                return Response({'Message': 'Username id required in the payload'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(username=username)
                Manager_group, created = Group.objects.get_or_create(name='Manager')
                Manager_group.user_set.add(user)
                return Response({'Message': 'This user is assigned to the Manager group'}, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'Mesage': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Message':'This user group has unauthorized access'})
    

class DeleteManager(generics.RetrieveAPIView, generics.DestroyAPIView):
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            user_id = kwargs.get('pk')
            try:
                user = User.objects.get(id=user_id)
                ManagerGroup = Group.objects.get(name='Manager')
                if user in ManagerGroup.user_set.all():
                    return Response({'Manager user': user.username}, status=status.HTTP_200_OK)
                return Response({'Message':'This user is not in Manager group'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'Message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Message':'This user group has unauthorized access'})
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            try:
                user_id = kwargs.get('pk')
                user = User.objects.get(id=user_id)
                Manager = Group.objects.get(name='Manager')
                Manager.user_set.remove(user)
                return Response({'message': 'Remove this user from the Manager group'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Message':'This user group has unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
   
    
class DeliveryCrew(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        DeliveryCrewGroup = Group.objects.get(name='Delivery crew')
        DeliveryCrewUser = DeliveryCrewGroup.user_set.all()
        if request.user.groups.filter(name='Manager').exists():
            return Response({'Delivery crew users': [user.username for user in DeliveryCrewUser]}, status=status.HTTP_200_OK)
        return Response({'Message':'This user group has unauthorized access'})
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            username = request.data.get('username')
            if username == '':
                return Response({'Message': 'Username id required in the payload'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(username=username)
                delivery_crew_group, created = Group.objects.get_or_create(name='Delivery crew')
                delivery_crew_group.user_set.add(user)
                return Response({'Message': 'This user is assigned to the Delivery crew group'}, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'Mesage': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Message':'This user group has unauthorized access'})


class DeleteDeliveryCrew(generics.RetrieveAPIView, generics.DestroyAPIView):
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            user_id = kwargs.get('pk')
            try:
                user = User.objects.get(id=user_id)
                DeliveryCrewGroup = Group.objects.get(name='Delivery crew')
                if user in DeliveryCrewGroup.user_set.all():
                    return Response({'Delivery crew user': user.username}, status=status.HTTP_200_OK)
                return Response({'Message':'This user is not in delivery crew group'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'Message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Message':'This user group has unauthorized access'})
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            try:
                user_id = kwargs.get('pk')
                user = User.objects.get(id=user_id)
                DeliveryCrew = Group.objects.get(name='Delivery crew')
                DeliveryCrew.user_set.remove(user)
                return Response({'message': 'Remove this user from the Delivery crew group'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Message':'This user group has unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

class cart(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        user = self.request.user
        if not self.request.user.groups.exists():
            return Cart.objects.filter(user=user)
        return Cart.objects.none()
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = CartSerializer(queryset, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Message':'Please fill your menu-items into the cart. This access is for customer'}, status=status.HTTP_200_OK)       
    def post(self, request, *args, **kwargs):
        if not request.user.groups.exists():
            serialized_item = CartSerializer(data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()  
                return Response({'Message':'sucessfully adds the menu item to the cart.'}, status=status.HTTP_201_CREATED)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message":"Unauthorized, This path is for Customer"}, status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request, *args, **kwargs):
        if not request.user.groups.exists():
            cart_item = Cart.objects.filter(user=request.user)
            if cart_item.exists():
                Cart.objects.filter(user=request.user).delete()
                return Response({"Message":"All menu items in the cart from current user has been deleted"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Message":"The menu item in the cart doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Message":"Unauthorized, This path is for Customer"}, status=status.HTTP_401_UNAUTHORIZED)

class Orders(generics.ListCreateAPIView): 
    serializer_class = OrderSerializer
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Delivery Crew').exists():
            orders = Order.objects.filter(delivery_crew=request.user)
            order_items = OrderItem.objects.filter(order__user=F('order'))
        elif request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
            order_items = OrderItem.objects.all()
        elif not request.user.groups.exists(): 
            orders = Order.objects.filter(user=request.user)
            order_items = OrderItem.objects.filter(order=request.user)
        order_serializer = OrderSerializer(orders, many=True)
        order_item_serializer = OrderItemSerializer(order_items, many=True)
        data = {
            'Order' : order_serializer.data,
            'OrderItem': order_item_serializer.data
        }
        if not request.user.groups.exists(): 
            if len(order_item_serializer.data) == 0:
                return Response({'Message':'Please use POST method to move cart item to order item'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        if not request.user.groups.exists():
            user = self.request.user
            CartItem = Cart.objects.filter(user=user)
            orderitems = OrderItem.objects.filter(order=user)
            if orderitems.exists():
                orderitems.delete()
            if not CartItem:
                return Response({'Message': 'No cart items found for this user'}, status=status.HTTP_400_BAD_REQUEST)
            for cartitem in CartItem:
                OrderItemData = {
                    'order': user,
                    'menuitem': cartitem.menuitem,
                    'quantity': cartitem.quantity,
                    'unit_price': cartitem.unit_price,
                    'price': cartitem.price
                }
                order_item = OrderItem.objects.create(**OrderItemData)
            CartItem.delete()
            serialized_item = OrderSerializer(data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()  
                return Response({'Message': 'Order and Order items created and cart items are deleted successfully'}, status=status.HTTP_201_CREATED)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
             

class SingleOrder(generics.RetrieveUpdateDestroyAPIView):  
    serializer_class = OrderSerializer
    def get(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('pk')
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'Message':'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not request.user.groups.exists():
            order_id = kwargs.get('pk')
            user = self.request.user
            if Order.objects.filter(user=user, pk=order_id).exists():
                order = Order.objects.get(pk=order_id)
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            return Response({"Message":"This order ID doesn't belong to the current user"}, status=status.HTTP_403_FORBIDDEN)
        elif request.user.groups.filter(name='Manager').exists():
            order_id = kwargs.get('pk')
            order = Order.objects.get(pk=order_id)
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery crew').exists():
            order_id = kwargs.get('pk')
            user = self.request.user
            if Order.objects.filter(delivery_crew=user, pk=order_id).exists():
                order = Order.objects.get(pk=order_id)
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            return Response({"Message":"This order ID doesn't assigned to this delivery crew userid"}, status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            order_id = kwargs.get('pk')
            order = Order.objects.get(pk=order_id)
            order.delete()
            return Response({'Message':'Delete this user successfully'}, status=status.HTTP_200_OK)
        return Response({'Message':'Only Manager group can delete the order'}, status=status.HTTP_403_FORBIDDEN)
    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            order_id = kwargs.get('pk')
            item = self.get_object(pk=order_id)
            serializer_item = OrderSerializer(item, data=request.data)
            if serializer_item.is_valid():
                serializer_item.save()
                return Response(serializer_item.data, status=status.HTTP_200_OK)
            return Response(serializer_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Message':'Only Manager group can update the entire table of order'}, status=status.HTTP_403_FORBIDDEN)
    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Delivery crew').exists():
            try:
                order_id = kwargs.get('pk')
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return Response({'Message':'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderStatusSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        