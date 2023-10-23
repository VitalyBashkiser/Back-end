from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, toggle_company_visibility,\
    cancel_request, send_request, revoke_invitation,\
    decline_invitation, accept_invitation, remove_user_from_company, leave_company,\
    send_invitations, approve_request

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
    path('companies/<int:pk>/', CompanyViewSet.as_view({'get': 'retrieve'}), name='company-detail'),
    path('companies/<int:pk>/toggle_visibility/', toggle_company_visibility, name='toggle_company_visibility'),
    path('companies/<int:company_id>/send_invitations/', send_invitations, name='send_invitations'),
    path('companies/<int:company_id>/revoke_invitation/<int:invitation_id>/', revoke_invitation,
         name='revoke_invitation'),
    path('companies/<int:company_id>/send_request/', send_request, name='send_request'),
    path('companies/<int:company_id>/cancel_request/<int:request_id>/', cancel_request, name='cancel_request'),
    path('companies/<int:company_id>/decline_invitation/<int:invitation_id>/', decline_invitation,
         name='decline_invitation'),
    path('companies/<int:company_id>/accept_invitation/<int:invitation_id>/', accept_invitation,
         name='accept_invitation'),
    path('companies/<int:company_id>/remove_user/<int:user_id>/', remove_user_from_company,
         name='remove_user_from_company'),
    path('companies/<int:company_id>/leave/', leave_company, name='leave_company'),
    path('companies/<int:company_id>/approve_request/<int:request_id>/', approve_request, name='approve_request'),
]

