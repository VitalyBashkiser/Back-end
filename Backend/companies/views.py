from rest_framework import viewsets, permissions, status
from .serializers import CompanySerializer
from main.pagination import CustomPageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsCompanyOwner
from rest_framework.permissions import IsAuthenticated
from .models import Request, Invitation, User, Company
from main.serializers import UserSerializer
from .enums import RequestStatus


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Company.objects.all()
        return Company.objects.filter(owner=user)

    def perform_create(self, serializer):
        owner_id = self.request.data.get('owner')
        owner = User.objects.get(pk=owner_id)
        serializer.save(owner=owner)

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.owner:
            serializer.save()
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        if self.request.user == instance.owner:
            instance.delete()
        else:
            raise PermissionDenied()


@api_view(['POST'])
def toggle_company_visibility(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        company.is_visible = not company.is_visible
        company.save()
        return Response(status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def send_invitations(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    invited_users = request.data.get('invited_users')  # Assuming you send a list of user IDs in the request data
    for user_id in invited_users:
        user = get_object_or_404(User, id=user_id)
        Invitation.objects.create(user=user, company=company)
    return Response({'message': 'Invitations sent successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def revoke_invitation(request, company_id, invitation_id):
    company = get_object_or_404(Company, id=company_id)
    invitation = get_object_or_404(Invitation, id=invitation_id, company=company)
    invitation.delete()
    return Response({'message': 'Invitation revoked successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_request(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    Request.objects.create(user=request.user, company=company)
    return Response({'message': 'Request sent successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def cancel_request(request, company_id, request_id):
    company = get_object_or_404(Company, id=company_id)
    join_request = get_object_or_404(Request, id=request_id, company=company)
    join_request.delete()
    return Response({'message': 'Request canceled successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def decline_invitation(request, company_id, invitation_id):
    company = get_object_or_404(Company, id=company_id)
    invitation = get_object_or_404(Invitation, id=invitation_id, company=company)
    invitation.delete()
    return Response({'message': 'Invitation declined successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def accept_invitation(request, company_id, invitation_id):
    company = get_object_or_404(Company, id=company_id)
    invitation = get_object_or_404(Invitation, id=invitation_id, company=company)
    company.members.add(request.user)
    invitation.delete()
    return Response({'message': 'Invitation accepted successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCompanyOwner])
def approve_request(request, company_id, request_id):
    try:
        company = get_object_or_404(Company, id=company_id)
        request_obj = get_object_or_404(Request, id=request_id, company=company, status=Request.STATUS_CHOICES[0][0])

        # Check if the request has already been approved
        if request_obj.status != RequestStatus.PENDING.value:
            return Response({'error': 'Request cannot be approved'}, status=status.HTTP_400_BAD_REQUEST)

        request_obj.status = Request.STATUS_CHOICES[1][0]  # Assuming 'APPROVED' is the second choice
        request_obj.save()
        company.members.add(request_obj.user)

        return Response(CompanySerializer(company).data, status=status.HTTP_200_OK)

    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

    except Request.DoesNotExist:
        return Response({'error': 'Request not found or already approved'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def remove_user_from_company(request, company_id, user_id):
    company = get_object_or_404(Company, id=company_id)
    user = get_object_or_404(User, id=user_id)

    if request.user == company.owner or request.user == user:
        company.members.remove(user)
        return Response({'message': 'User removed from company successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to remove this user from the company'},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def leave_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.members.remove(request.user)
    return Response({'message': 'Left company successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCompanyOwner])
def appoint_admin(request, company_id, user_id):
    try:
        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(User, id=user_id)
        company.admins.add(user)
        return Response({'message': 'User appointed as admin successfully'}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCompanyOwner])
def remove_admin(request, company_id, user_id):
    try:
        company = get_object_or_404(Company, id=company_id)
        user = get_object_or_404(User, id=user_id)
        company.admins.remove(user)
        return Response({'message': 'User removed from admins successfully'}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCompanyOwner])
def list_admins(request, company_id):
    try:
        company = get_object_or_404(Company, id=company_id)
        admins = company.admins.all()
        serializer = UserSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
