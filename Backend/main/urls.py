from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('health_check/', views.health_check, name='health_check'),
]
