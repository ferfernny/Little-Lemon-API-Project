from rest_framework import generics
from ..serializers import CartSerializer
from ..models import Cart
from rest_framework.response import Response
from rest_framework import status
from ..business_logic.http_status_code_business_logic import http_status_code_business_logic
from ..business_logic.permission_business_logic import permission_business_logic

class cart(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        user = self.request.user
        if permission_business_logic.customer_permission(user):
            return Cart.objects.filter(user=user)
        return Cart.objects.none()
    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = CartSerializer(queryset, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return http_status_code_business_logic.status_200_ok('Please fill your menu-items into the cart. This access is for customer.')
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if permission_business_logic.customer_permission(user):
            serialized_item = CartSerializer(data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()  
                return http_status_code_business_logic.status_201_created('Successfully adds the menu item to the cart.')
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return http_status_code_business_logic.status_401_unauthorized('Unauthorized, This path is for Customer.')
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if permission_business_logic.customer_permission(user):
            cart_item = Cart.objects.filter(user=request.user)
            if cart_item.exists():
                Cart.objects.filter(user=request.user).delete()
                return http_status_code_business_logic.status_204_no_content('All menu items in the cart from current user has been deleted.')
            return http_status_code_business_logic.status_404_not_found("The menu item in the cart doesn't exists.")
        return http_status_code_business_logic.status_401_unauthorized('Unauthorized, This path is for Customer.')