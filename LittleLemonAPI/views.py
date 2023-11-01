from django.shortcuts import render
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group

# Create your views here.
@api_view(['GET','POST','PUT','PATCH','DELETE'])    
def menu_items(request):
    if request.user.groups.filter(name='Customer Crew').exists() or not request.user.groups.exists():
        if request.method == 'GET':
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif rfequest.method in ['POST','PUT','PATCH','DELETE']:
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.user.groups.filter(name='Manager').exists() :
        if request.method == 'GET':
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)  
            return Response(serializer.data)
        elif request.method == 'POST':
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()  
            return Response(serialized_item.validated_data, status.HTTP_201_CREATED)

    
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def singlemenu_item(request, id):
    item = MenuItem.objects.get(pk=id)
    if request.user.groups.filter(name='Delivery Crew').exists() or not request.user.groups.exists():
        if request.method == 'GET':
            serialized_item = MenuItemSerializer(item) 
            return Response(serialized_item.data)
        elif request.method in ['POST','PUT','PATCH','DELETE']:
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.user.groups.filter(name='Manager').exists() :
        if request.method == 'GET':
            serialized_item = MenuItemSerializer(item) 
            return Response(serialized_item.data)
        elif request.method in ['PUT','PATCH']:
            serializer_item = MenuItemSerializer(item, data=request.data)
            if serializer_item.is_valid():
                serializer_item.save()
                return Response(serializer_item.data)
            return Response(serializer_item.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
                
@api_view(['GET','POST','DELETE'])
def managers(request, id):
    if request.method == 'POST':
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            managers = group.objects.get(name='Manager')
            managers.user_set.add(user)
            return Response({'message':'User add to the Manager group'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        managers = group.objects.get(name='Manager')
        manager_users = managers.user_set.all()
        return Response({'manager_users': [user.username for user in manager_users]}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id=id)
            managers = Group.objects.get(name='Manager')
            managers.user_set.remove(user)
            return Response({'message': 'Remove this userID from the Manager group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message':'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def DeliveryCrew(request, id):  #need to re-write
    if request.method == 'POST':
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            DeliveryCrew = group.objects.get(name='Derivery crew')
            DeliveryCrew.user_set.add(user)
            return Response({'message':'User add to the Delivery crew group'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        DeliveryCrew = group.objects.get(name='Delivery crew')
        DeliveryCrewUser = managers.user_set.all()
        return Response({'Delivery Crew users': [user.username for user in DeliveryCrewUser]}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id=id)
            DeliveryCrew = Group.objects.get(name='Manager')
            DeliveryCrew.user_set.remove(user)
            return Response({'message': 'Remove this userID from the Delivery crew group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message':'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','POST','DELETE'])
def cart(request):
    if not request.user.groups.exit():
        if request.method == 'GET':
            cart_item = Cart.objects.filter(user=request.user)
            serializer = CartSerializer(cart_item, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            cart_item = MenuItem.objects.filter(user=request.user)
            #Sets the authenticated user as the user id for these cart items
            return Response({'Message':'sucessfully adds the menu item to the cart.'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            cart_item = Cart.objects.filter(user=request.user)
            MenuItem.objects.filter(user=request.user).delete()
            if cart_item.exists():
                Cart.objects.filter(user=request.user).delete()
            return Response({"Message":"All cart and menu items from current user has been deleted"}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"Message":"- Unauthorized, This path is for Customer"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET','POST'])
def orders(request):
    if request.user.groups.filter(name='Delivery Crew').exists():
        if request.method == 'GET':
            order_item = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(order_item, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            order_item = Order.objects.all()
            serializer = OrderSerializer(order_item, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif not request.user.groups.exists():
        if request.method == 'GET':
            order_item = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(order_item, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            OrderItem_Serializer = OrderItemSerializer(data=request.data)
            if OrderItemSerializer.is_valid():
                OrderItem = OrderItemSerializer.save()
                CartItem = Cart.objects.filter(user=request.user).first()
                if CartItem is not None:
                    for cartItem in CartItem.all():
                        OrderItemData = {
                            'order': request.user,
                            'menuitem': cartItem.menuitem,
                            'quantity': cartItem.quantity,
                            'unit_price': cartItem.unit_price,
                            'price': cartItem.price
                        }
                        OrderItem_Serializer = OrderItemSerializer(data=OrderItemData)
                        if OrderItem_Serializer.is_valid():
                            OrderItem_Serializer.save()
                            cartItem.delete()
                        else:
                            return Response(OrderItem_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(OrderItem_Serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response("No cart found for the user", status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET','PUT','PATCH','DELETE'])
def singleorder(request, id):
    if not request.user.groups.exists():
        if request.method == 'GET':
            if Order.objects.filter(user=request.user, pk=id).exists():
                order = OrderItem.objects.get(pk=id)
                serializer = OrderItemSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Message":"This order ID doesn't belong to the current user"}, status=status.HTTP_403_FORBIDDEN)
        elif request.method in ['PUT','PATCH']:
            order = Order.objects.filter(user=request.user, pk=id)
            if order.status == 0:    
                print("I am here testing ka")
                #Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1.
                #If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery.
                #If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.
    elif request.user.groups.filter(name='Manager').exists():
        if request.method == 'DELETE':
            order = OrderItem.objects.get(pk=id)
            order.delete()
            return Response({'Message':"This order has been deleted"}, status=status.HTTP_204_NO_CONTENT)
    elif request.user.groups.filter(name='Delivery crew'):
        if request.method == 'PATCH':
            order = OrderItem.objects.get(pk=id)
            serializer = OrderSerializer(order, data=request.data, partial=True, fields=['status'])
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

        
        