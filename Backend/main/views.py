import logging
from .pagination import CustomPageNumberPagination
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


# View class for performing CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['created_at']
    pagination_class = CustomPageNumberPagination

    # Method to retrieve an individual user by user ID
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        # Get database query
        queryset = self.filter_queryset(self.get_queryset())
        # Get the filtering arguments (in this case, the user ID)
        filter_kwargs = {'id': self.kwargs['pk']}
        # Get the user object or return a 404 error if not found
        obj = get_object_or_404(queryset, **filter_kwargs)
        # Check object permissions
        self.check_object_permissions(self.request, obj)
        return obj


# Function to get a user by his ID
@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        # Log the error and return an error response
        logger.error("User not found")
        # Return an error if there is no user with the specified ID
        return Response({'error': 'User not found'}, status=404)


# Function to check the system status
def health_check(request):
    return JsonResponse({
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    })