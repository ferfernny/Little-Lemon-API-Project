from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import Group, User

modelSerializer = serializers.ModelSerializer
primaryKeyRelatedField = serializers.PrimaryKeyRelatedField
class GroupSerializer(modelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(modelSerializer):
    class Meta:
        model = User
        fields = '__all__'
       
class CategorySerializer(modelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryChoiceField(primaryKeyRelatedField):
    def display_value(self, instance):
        return instance.categorytitle
    
class MenuitemChoiceField(primaryKeyRelatedField):
    def display_value(self, instance):
        return instance.title
    
class MenuItemSerializer(modelSerializer):
    category = CategoryChoiceField(queryset=Category.objects.all())
    class Meta:
        model = MenuItem
        fields = '__all__'

class CartSerializer(modelSerializer):
    menuitem = MenuitemChoiceField(queryset=MenuItem.objects.all())
    class Meta:
        model = Cart
        fields = '__all__'
        
class OrderSerializer(modelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderItemSerializer(modelSerializer):
    menuitem = MenuitemChoiceField(queryset=MenuItem.objects.all())
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderStatusSerializer(modelSerializer):
    class Meta:
        model = Order
        fields = ['status']