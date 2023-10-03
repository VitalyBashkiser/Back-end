from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def health_check(request):
    return JsonResponse({
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    })


