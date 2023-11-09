from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import Group, User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
       
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryChoiceField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return instance.categorytitle
    
class MenuitemChoiceField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return instance.title
    
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategoryChoiceField(queryset=Category.objects.all())
    class Meta:
        model = MenuItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuitemChoiceField(queryset=MenuItem.objects.all())
    class Meta:
        model = Cart
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuitemChoiceField(queryset=MenuItem.objects.all())
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']