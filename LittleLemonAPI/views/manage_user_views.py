from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from ..serializers import UserSerializer
from rest_framework import generics
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from ..business_logic.permission_business_logic import permission_business_logic
from ..business_logic.http_status_code_business_logic import http_status_code_business_logic

def manager(request: HttpRequest) -> HttpResponse:
    manager_data = User.objects.filter(groups__name="Manager")
    delivery_crew_data = User.objects.filter(groups__name="Delivery crew")
    main_data = {"manager" : manager_data, "delivery_crew" : delivery_crew_data}
    return render(request, 'manager_view.html', main_data)

class Managers(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        ManagerGroup = Group.objects.get(name='Manager')
        ManagerUser = ManagerGroup.user_set.all()
        if permission_business_logic.has_permission(request.user, ['Manager']):
            return Response(
                {'Manager users': [user.username for user in ManagerUser]}, 
                status=status.HTTP_200_OK
                )
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access')
    def post(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            username = request.data.get('username')
            if username == '':
                return http_status_code_business_logic.status_400_bad_request('Username id required in the payload')
            try:
                user = User.objects.get(username=username)
                Manager_group, created = Group.objects.get_or_create(name='Manager')
                Manager_group.user_set.add(user)
                return http_status_code_business_logic.status_201_created('This user is assigned to the Manager group.')
            except User.DoesNotExist:
                return http_status_code_business_logic.status_404_not_found('User not found')
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access')
    
class DeleteManager(generics.RetrieveAPIView, generics.DestroyAPIView):
    def get(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            user_id = kwargs.get('pk')
            try:
                user = User.objects.get(id=user_id)
                ManagerGroup = Group.objects.get(name='Manager')
                if user in ManagerGroup.user_set.all():
                    return Response(
                        {'Manager user': user.username}, 
                        status=status.HTTP_200_OK
                        )
                return http_status_code_business_logic.status_404_not_found('This user is not in Manager group')
            except User.DoesNotExist:
                return http_status_code_business_logic.status_404_not_found('User not found')
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access')
    def delete(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            try:
                user_id = kwargs.get('pk')
                user = User.objects.get(id=user_id)
                Manager = Group.objects.get(name='Manager')
                Manager.user_set.remove(user)
                return http_status_code_business_logic.status_200_ok('Remove this user from the Manager group.')
            except User.DoesNotExist:
                return http_status_code_business_logic.status_404_not_found('User not found')
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access')
   
class DeliveryCrew(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            DeliveryCrewGroup = Group.objects.get(name='Delivery crew')
            DeliveryCrewUser = DeliveryCrewGroup.user_set.all()
            return Response(
                {'Delivery crew users': [user.username for user in DeliveryCrewUser]}, 
                status=status.HTTP_200_OK
                )
        return Response({'Message':'This user group has unauthorized access'})
    def post(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            username = request.data.get('username')
            if username == '':
                return http_status_code_business_logic.status_400_bad_request('Username id required in the payload')
            try:
                user = User.objects.get(username=username)
                delivery_crew_group, created = Group.objects.get_or_create(name='Delivery crew')
                delivery_crew_group.user_set.add(user)
                return http_status_code_business_logic.status_201_created('This user is assigned to the Delivery crew group.')
            except User.DoesNotExist:
                return http_status_code_business_logic.status_404_not_found('User not found')
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access')


class DeleteDeliveryCrew(generics.RetrieveAPIView, generics.DestroyAPIView):
    def get(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            user_id = kwargs.get('pk')
            try:
                user = User.objects.get(id=user_id)
                DeliveryCrewGroup = Group.objects.get(name='Delivery crew')
                if user in DeliveryCrewGroup.user_set.all():
                    return Response(
                        {'Delivery crew user': user.username}, 
                        status=status.HTTP_200_OK
                        )
                return http_status_code_business_logic.status_404_not_found('This user is not in Delivery crew group')
            except User.DoesNotExist:
                return http_status_code_business_logic.status_404_not_found('User not found')
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access')
    
    def delete(self, request, *args, **kwargs):
        if permission_business_logic.has_permission(request.user, ['Manager']):
            try:
                user_id = kwargs.get('pk')
                user = User.objects.get(id=user_id)
                DeliveryCrew = Group.objects.get(name='Delivery crew')
                DeliveryCrew.user_set.remove(user)
                return http_status_code_business_logic.status_200_ok('Remove this user from the Delivery crew group.')
            except User.DoesNotExist:
                return http_status_code_business_logic.status_404_not_found('User not found')
        return http_status_code_business_logic.status_403_forbidden('This user group has unauthorized access')