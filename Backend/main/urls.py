from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, health_check

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('health_check/', health_check, name='health_check'), # # Added path for health_check
]