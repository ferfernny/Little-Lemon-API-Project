from ..serializers import MenuItemSerializer
from ..models import MenuItem
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from ..business_logic.permission_business_logic import permission_business_logic
from ..business_logic.http_status_code_business_logic import http_status_code_business_logic

def menu(request: HttpRequest) -> HttpResponse:
    menu_data = MenuItem.objects.all()
    main_data = {"menu":menu_data}
    return render(request, 'menu.html', main_data)

class MenuItems(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get(self, request, *args, **kwargs):
        if permission_business_logic.authenticated_user_permission(request.user):
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return http_status_code_business_logic.status_403_forbidden('This user has unauthorized access.')
    def post(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            serialized_item = MenuItemSerializer(data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()  
                return http_status_code_business_logic.status_201_created('This menu-item has been created.')
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return http_status_code_business_logic.status_403_forbidden('This user has unauthorized access.')
            
            
class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get(self, request, *args, **kwargs):
        if permission_business_logic.authenticated_user_permission(request.user):
            response = super().get(request, *args, **kwargs)
            response.status_code = status.HTTP_200_OK
            return response
        return http_status_code_business_logic.status_403_forbidden('This user has unauthorized access.')
    def update(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            item = self.get_object()
            serializer_item = MenuItemSerializer(item, data=request.data)
            if serializer_item.is_valid():
                serializer_item.save()
                return Response(serializer_item.data, status=status.HTTP_200_OK)
            return Response(serializer_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return http_status_code_business_logic.status_403_forbidden('This user has unauthorized access.')
    def delete(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            item = self.get_object()
            item.delete()
            return http_status_code_business_logic.status_204_no_content('The menu-items has been deleted')
        return http_status_code_business_logic.status_403_forbidden('This user has unauthorized access.')