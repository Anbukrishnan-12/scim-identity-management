from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
import uuid
import logging
from .models import SlackUser
from .serializers import SlackUserSerializer

logger = logging.getLogger(__name__)

class SCIMPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'count'
    max_page_size = 100

@api_view(['GET', 'POST'])
def user_list(request):
    try:
        if request.method == 'GET':
            filter_param = request.GET.get('filter', '')
            users = SlackUser.objects.all()
            
            if filter_param:
                if 'userName eq' in filter_param:
                    username = filter_param.split('"')[1]
                    users = users.filter(user_name=username)
                elif 'active eq' in filter_param:
                    active_val = 'true' in filter_param.lower()
                    users = users.filter(active=active_val)
            
            serializer = SlackUserSerializer(users, many=True)
            return Response({
                'schemas': ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
                'totalResults': users.count(),
                'startIndex': 1,
                'itemsPerPage': len(serializer.data),
                'Resources': serializer.data
            })
        
        elif request.method == 'POST':
            # Check if user already exists
            user_name = request.data.get('user_name')
            if user_name and SlackUser.objects.filter(user_name=user_name).exists():
                return Response(
                    {'error': f'User with username "{user_name}" already exists'}, 
                    status=status.HTTP_409_CONFLICT
                )
            
            serializer = SlackUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Error in user_list: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request, user_id):
    try:
        user = get_object_or_404(SlackUser, scim_id=user_id)
        
        if request.method == 'GET':
            serializer = SlackUserSerializer(user)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            print(f"Update request data: {request.data}")
            serializer = SlackUserSerializer(user, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        logger.error(f"Error in user_detail: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)