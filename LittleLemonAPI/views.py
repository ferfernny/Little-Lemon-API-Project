from django.shortcuts import render
from .models import MenuItem, Cart
from .serializaers import MenuItemSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group

# Create your views here.
@api_view(['GET','POST','PUT','PATCH','DELETE'])    #for customer and delivery crew
def menu_items(request):
    if request.user.groups.filter(name='Customer Crew').exist() or not request.user.groups.exist():
        if request.method == 'GET':
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)  # Use your serializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method in ['POST','PUT','PATCH','DELETE']:
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.user.groups.filter(name='Manager').exist() :
        if request.method == 'GET':
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)  # Use your serializer
            return Response(serializer.data)
        elif request.method = 'POST'
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()  #if you want to save the data
            return Response(serialized_item.validated_data, status.HTTP_201_CREATED)

    
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def singlemenu_item(request, id):
    item = MenuItem.objects.get(pk=id)
    if request.user.groups.filter(name='Customer Crew').exist() or not request.user.groups.exist():
        if request.method == 'GET':
            serialized_item = MenuItemSerializer(item) 
            return Response(serialized_item.data)
        elif request.method in ['POST','PUT','PATCH','DELETE']:
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.user.groups.filter(name='Manager').exist() :
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
                
@api_view(['GET','POST'])
def managers(request):
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

@api_view(['GET','POST','DELETE'])
def cart(request):
    if request.method == 'GET':
        cart_item = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_item, many=True)  # Use your serializer
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
    elif request.method == 'DELETE':
        
        