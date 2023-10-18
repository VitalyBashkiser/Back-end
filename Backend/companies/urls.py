from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, toggle_company_visibility

router = DefaultRouter()
router.register(r'', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/toggle_visibility/', toggle_company_visibility, name='toggle-company-visibility'),
]
